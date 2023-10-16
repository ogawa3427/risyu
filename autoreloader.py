import sys
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:

    def __init__(self, directory_to_watch):
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.observer = Observer()
        self.flask_process = None

    def run(self):
        event_handler = Handler()
        event_handler.set_flask_runner(self.run_flask)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.run_flask()
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

    def run_flask(self):
        if self.flask_process:
            self.flask_process.terminate()
        self.flask_process = subprocess.Popen(["flask", "run"])

class Handler(FileSystemEventHandler):

    def set_flask_runner(self, runner):
        self.flask_runner = runner

    def on_modified(self, event):
        if event.is_directory:
            return None
        else:
            print(f"Re-running Flask due to: {event.src_path}")
            self.flask_runner()

if __name__ == '__main__':
    directory_to_watch = os.path.expanduser('~/risyu/templates')  # デフォルトの監視ディレクトリを指定
    if len(sys.argv) > 1:
        directory_to_watch = sys.argv[1]  # コマンドライン引数が指定されていれば、それを使用
    w = Watcher(directory_to_watch)
    w.run()

