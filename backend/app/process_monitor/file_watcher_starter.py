"""
Phase 1 starter script — the simplest possible file watcher.

What it does:
- Watches a folder you choose.
- Prints a line every time a file is created, changed, renamed, or deleted.

Run it with:
    python file_watcher_starter.py /path/to/test/folder

Try it:
1. Run this script pointing at an empty test folder.
2. In another window, create a new file in that folder, then rename it, then edit it.
3. Watch this script print out what it saw.

Once this works, move on to Phase 2 in the README: save these events to a database
instead of just printing them.
"""

import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class SimplePrintHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"[CREATED]  {event.src_path}")

    def on_modified(self, event):
        print(f"[MODIFIED] {event.src_path}")

    def on_deleted(self, event):
        print(f"[DELETED]  {event.src_path}")

    def on_moved(self, event):
        print(f"[RENAMED]  {event.src_path} -> {event.dest_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python file_watcher_starter.py /path/to/folder")
        sys.exit(1)

    watch_path = sys.argv[1]
    print(f"Watching: {watch_path}  (press Ctrl+C to stop)")

    handler = SimplePrintHandler()
    observer = Observer()
    observer.schedule(handler, watch_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
