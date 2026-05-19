# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from PyQt6.QtCore import QThread, pyqtSignal


class ScanWorker(QThread):
    progress_updated = pyqtSignal(int, int, str)
    scan_finished = pyqtSignal(dict, float)
    scan_error = pyqtSignal(str)

    def __init__(self, root_path, dupes_folder, min_size, max_size,
                 include_ext, exclude_ext, threads):
        super().__init__()
        self.root_path = root_path
        self.dupes_folder = dupes_folder.rstrip('/\\') + os.sep
        self.min_size = min_size
        self.max_size = max_size
        self.threads = threads
        self.is_running = True
        self.last_update_time = time.time()

        self.include_ext_set = None
        if include_ext and include_ext.strip():
            self.include_ext_set = set(e.strip().lower() for e in include_ext.split(','))

        self.exclude_ext_set = None
        if exclude_ext and exclude_ext.strip():
            self.exclude_ext_set = set(e.strip().lower() for e in exclude_ext.split(','))

    def stop(self):
        self.is_running = False

    def _should_process_file(self, path, ext):
        path_norm = os.path.normpath(path)
        dupes_norm = os.path.normpath(self.dupes_folder.rstrip('/\\'))

        if path_norm.startswith(dupes_norm + os.sep) or path_norm == dupes_norm:
            return False

        if self.include_ext_set and ext not in self.include_ext_set:
            return False
        if self.exclude_ext_set and ext in self.exclude_ext_set:
            return False
        return True

    def _quick_hash(self, path):
        try:
            with open(path, 'rb') as f:
                first_bytes = f.read(1024)
                return hashlib.md5(first_bytes).hexdigest()
        except:
            return None

    def _full_hash(self, path):
        try:
            import xxhash
            hasher = xxhash.xxh64()
            use_xxhash = True
        except ImportError:
            hasher = hashlib.md5()
            use_xxhash = False
        try:
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(128 * 1024), b''):
                    if not self.is_running:
                        return None
                    hasher.update(chunk)
            if use_xxhash:
                return f"{hasher.intdigest():016x}"
            return hasher.hexdigest()
        except:
            return None

    def run(self):
        start_time = time.time()
        files_by_size = {}
        file_mod_times = {}
        total_files = 0
        self.last_update_time = time.time()
        last_total_files = 0

        try:
            self.progress_updated.emit(0, 0, "Scanning directory structure...")

            for root, dirs, files in os.walk(self.root_path):
                if not self.is_running:
                    return

                root_norm = os.path.normpath(root)
                dupes_norm = os.path.normpath(self.dupes_folder.rstrip('/\\'))
                if root_norm.startswith(dupes_norm + os.sep) or root_norm == dupes_norm:
                    continue

                for file in files:
                    if not self.is_running:
                        return

                    ext = os.path.splitext(file)[1].lower()
                    path = os.path.join(root, file)

                    if not self._should_process_file(path, ext):
                        continue

                    try:
                        stat = os.stat(path)
                        size = stat.st_size

                        if size < self.min_size or size > self.max_size:
                            continue
                        if size == 0:
                            continue

                        files_by_size.setdefault(size, []).append(path)
                        file_mod_times[path] = stat.st_mtime
                        total_files += 1

                        current_time = time.time()
                        if total_files - last_total_files >= 100 or current_time - self.last_update_time > 0.2:
                            self.progress_updated.emit(total_files, 0, f"Scanning... {total_files} files found")
                            last_total_files = total_files
                            self.last_update_time = current_time

                    except:
                        continue

            self.progress_updated.emit(total_files, total_files, f"Scan complete. Found {total_files} files")

            potential_dupes = []
            for size, paths in files_by_size.items():
                if len(paths) > 1:
                    for path in paths:
                        potential_dupes.append((size, path, file_mod_times.get(path, 0)))

            if not potential_dupes:
                self.scan_finished.emit({}, time.time() - start_time)
                return

            self.progress_updated.emit(0, len(potential_dupes),
                                       f"Quick hashing {len(potential_dupes)} potential duplicates (1KB each)...")

            quick_groups = {}
            processed = 0
            self.last_update_time = time.time()
            last_processed = 0

            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                future_to_data = {executor.submit(self._quick_hash, path): (size, path, mod_time) for
                                  size, path, mod_time in potential_dupes}
                for future in as_completed(future_to_data):
                    if not self.is_running:
                        executor.shutdown(wait=False, cancel_futures=True)
                        return
                    size, path, mod_time = future_to_data[future]
                    quick_hash = future.result()
                    if quick_hash:
                        quick_groups.setdefault(quick_hash, []).append((size, path, mod_time))
                    processed += 1
                    current_time = time.time()
                    if processed - last_processed >= 20 or current_time - self.last_update_time > 0.1:
                        percent = int(processed * 100 / len(potential_dupes))
                        self.progress_updated.emit(processed, len(potential_dupes),
                                                   f"Quick hashing: {processed}/{len(potential_dupes)} ({percent}%)")
                        last_processed = processed
                        self.last_update_time = current_time

            candidates = {}
            for quick_hash, files in quick_groups.items():
                size_map = {}
                for size, path, mod_time in files:
                    size_map.setdefault(size, []).append((path, mod_time))
                for size, sized_files in size_map.items():
                    if len(sized_files) > 1:
                        candidates[(size, quick_hash)] = sized_files

            total_to_full_hash = sum(len(files) for files in candidates.values())
            if total_to_full_hash == 0:
                self.scan_finished.emit({}, time.time() - start_time)
                return

            self.progress_updated.emit(0, total_to_full_hash, f"Full hashing {total_to_full_hash} real candidates...")

            results = {}
            processed = 0
            self.last_update_time = time.time()
            last_processed = 0

            full_hash_jobs = []
            for files in candidates.values():
                for path, mod_time in files:
                    full_hash_jobs.append((path, mod_time))

            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                future_to_path = {executor.submit(self._full_hash, path): (path, mod_time) for path, mod_time in
                                  full_hash_jobs}
                for future in as_completed(future_to_path):
                    if not self.is_running:
                        executor.shutdown(wait=False, cancel_futures=True)
                        return
                    path, mod_time = future_to_path[future]
                    full_hash = future.result()
                    if full_hash:
                        try:
                            size = os.path.getsize(path)
                            results.setdefault(full_hash, []).append((path, size, mod_time))
                        except:
                            pass
                    processed += 1
                    current_time = time.time()
                    if processed - last_processed >= 5 or current_time - self.last_update_time > 0.1:
                        percent = int(processed * 100 / total_to_full_hash)
                        self.progress_updated.emit(processed, total_to_full_hash,
                                                   f"Full hashing: {processed}/{total_to_full_hash} ({percent}%)")
                        last_processed = processed
                        self.last_update_time = current_time

            final_results = {hash_val: files for hash_val, files in results.items() if len(files) > 1}
            if self.is_running:
                self.scan_finished.emit(final_results, time.time() - start_time)

        except Exception as e:
            self.scan_error.emit(str(e))
