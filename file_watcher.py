#!/usr/bin/env python3

import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
print("Started Checking The Folder")
# Log dosyasının yolu
LOG_FILE = "/home/debian/bsm/logs/changes.json"

class Watcher:
    def __init__(self, directory_to_watch):
        self.directory_to_watch = directory_to_watch
        self.event_handler = Handler()
        self.observer = Observer()

    def run(self):
        self.observer.schedule(self.event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
                print("Checking...")
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        data = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "is_directory": event.is_directory,
            "timestamp": time.ctime(),
        }
        print(data)  # Konsola yazdırmak için
        self.log_event(data)

    @staticmethod
    def log_event(data):
        try:
            with open(LOG_FILE, "a") as f:
                f.write(json.dumps(data) + "\n")
        except Exception as e:
            print(f"Log yazarken hata: {e}")

if __name__ == "__main__":
    path_to_watch = "/home/debian/bsm/test"
    watcher = Watcher(path_to_watch)
    watcher.run()
