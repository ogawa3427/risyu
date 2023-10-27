import sys
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:

    def __init__(self, directory_to_watch, virtualenv_path):
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.virtualenv_path = virtualenv_path
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
        env = os.environ.copy()
        env['PATH'] = self.virtualenv_path + "/bin:" + env['PATH']
        self.flask_process = subprocess.Popen(["flask", "run"], env=env)

class Handler(FileSystemEventHandler):

    def set_flask_runner(self, runner):
        self.flask_runner = runner

    def on_modified(self, event):
        if event.is_directory:
            return None

        # counter.txt ファイルを無視する
        if os.path.basename(event.src_path) == "counter.txt":
            print("Ignoring changes in counter.txt")
            return None

        if os.path.basename(event.src_path) == "app.py":
            # Copy the contents of app.py to main.py
            with open("app.py", "r") as source, open("main.py", "w") as dest:
                dest.write(source.read())
            print("Updated main.py with the content of app.py")

        print(f"Re-running Flask due to: {event.src_path}")
        self.flask_runner()


if __name__ == '__main__':
    directory_to_watch = os.path.expanduser('~/risyu')  # デフォルトの監視ディレクトリを指定
    virtualenv_path = os.path.expanduser('~/risyu/risyu')  # デフォルトのvirtualenvのパスを指定

    if len(sys.argv) > 1:
        directory_to_watch = sys.argv[1]  # コマンドライン引数が指定されていれば、それを使用
    w = Watcher(directory_to_watch, virtualenv_path)
    w.run()
