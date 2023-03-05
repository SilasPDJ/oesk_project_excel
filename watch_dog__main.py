
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'modified' and event.src_path.endswith('.py'):
            # main_on_change()
            print(
                f"Detected change to {event.src_path}, restarting Streamlit...")
            subprocess.call("streamlit run app.py", shell=True)


if __name__ == "__main__":
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()
    print("Watching for changes to app.py...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
