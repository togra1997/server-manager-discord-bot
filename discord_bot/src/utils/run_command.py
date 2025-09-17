import signal
import subprocess
from typing import Optional

start_message = "Server start"
stop_message = "Server stop"
status_running_message = "Server is running"
status_not_running_message = "Server is not running"
status_already_running_message = "Server is already running"


class ServerManager:
    """
    サーバープロセスの起動・停止・状態確認を管理するクラス。
    指定したbashスクリプトをサブプロセスとして実行します。
    """

    def __init__(self, bash_path: str):
        """
        Args:
            bash_path (str): 実行するbashスクリプトのパス
        """
        self.process: Optional[subprocess.Popen] = None
        self.bash_path: str = bash_path

    def start(self) -> str:
        """
        サーバープロセスを開始します。

        Returns:
            str: サーバーの起動状態メッセージ
        """
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(
                ["bash", self.bash_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return start_message
        else:
            return status_already_running_message

    def stop(self) -> str:
        """
        サーバープロセスを停止します。

        Returns:
            str: サーバーの停止状態メッセージ
        """
        if self.process is not None and self.process.poll() is None:
            self.process.send_signal(signal.SIGINT)
            self.process.terminate()
            try:
                self.process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            return stop_message
        else:
            return status_not_running_message

    def status(self) -> str:
        """
        サーバープロセスの稼働状態を確認します。

        Returns:
            str: サーバーの状態メッセージ
        """
        if self.process is not None and self.process.poll() is None:
            return status_running_message
        else:
            return status_not_running_message
