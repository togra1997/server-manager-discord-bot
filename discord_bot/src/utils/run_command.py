import signal
import subprocess


class ServerManager:
    def __init__(self, bash_path: str):
        self.process = None
        self.bash_path = bash_path

    def start(self):
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(
                ["bash", self.bash_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return "Server start"
        else:
            return "Server is already running"

    def stop(self):
        if self.process is not None and self.process.poll() is None:
            self.process.send_signal(signal.SIGINT)
            self.process.terminate()
            try:
                self.process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            return "Server stop"
        else:
            return "Server is not running"

    def status(self):
        if self.process is not None and self.process.poll() is None:
            return "Server is running"
        else:
            return "Server is not running"

