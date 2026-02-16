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
        self.dupes_folder = dupes_folder
        self.min_size = min_size
        self.max_size = max_size
        self.include_ext = include_ext
        self.exclude_ext = exclude_ext
        self.threads = threads
        self.is_running = True

    def stop(self):
        self.is_running = False

    def _should_process_file(self, path):
        if path.startswith(self.dupes_folder):
            return False

        ext = os.path.splitext(path)[1].lower()

        if self.include_ext:
            include_list = [e.strip().lower() for e in self.include_ext.split(',')]
            if ext not in include_list:
                return False

        if self.exclude_ext:
            exclude_list = [e.strip().lower() for e in self.exclude_ext.split(',')]
            if ext in exclude_list:
                return False

        return True

    def _hash_file(self, path):
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
        except (IOError, OSError):
            return None

    def run(self):
        start_time = time.time()
        files_by_size = {}
        file_mod_times = {}
        total_files = 0

        try:
            for root, dirs, files in os.walk(self.root_path):
                if not self.is_running:
                    return

                if root.startswith(self.dupes_folder):
                    continue

                for file in files:
                    if not self.is_running:
                        return

                    path = os.path.join(root, file)

                    if not self._should_process_file(path):
                        continue

                    try:
                        stat = os.stat(path)
                        size = stat.st_size

                        if size < self.min_size or size > self.max_size:
                            continue

                        files_by_size.setdefault(size, []).append(path)
                        file_mod_times[path] = stat.st_mtime
                        total_files += 1

                        if total_files % 100 == 0:
                            self.progress_updated.emit(total_files, 0, f"Found {total_files} files")

                    except (OSError, IOError):
                        continue

            total_to_hash = sum(len(paths) for paths in files_by_size.values() if len(paths) > 1)

            if total_to_hash == 0:
                self.scan_finished.emit({}, time.time() - start_time)
                return

            self.progress_updated.emit(0, total_to_hash, f"Hashing {total_to_hash} files...")

            hash_jobs = []
            for size, paths in files_by_size.items():
                if len(paths) > 1:
                    for path in paths:
                        hash_jobs.append((size, path, file_mod_times.get(path, 0)))

            results = {}
            processed = 0

            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                future_to_path = {
                    executor.submit(self._hash_file, path): (size, path, mod_time)
                    for size, path, mod_time in hash_jobs
                }

                for future in as_completed(future_to_path):
                    if not self.is_running:
                        executor.shutdown(wait=False, cancel_futures=True)
                        return

                    size, path, mod_time = future_to_path[future]
                    hash_value = future.result()

                    if hash_value:
                        results.setdefault(hash_value, []).append((path, size, mod_time))

                    processed += 1
                    if processed % 10 == 0:
                        self.progress_updated.emit(processed, total_to_hash, f"Hashing: {processed}/{total_to_hash}")

            if self.is_running:
                self.scan_finished.emit(results, time.time() - start_time)

        except Exception as e:
            self.scan_error.emit(str(e))
