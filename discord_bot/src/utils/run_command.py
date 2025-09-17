import shlex
import subprocess


class CommandRunner:
    def __init__(self):
        self.commands = {}

    def add_command(self, command_name: str, command: str):
        self.commands[command_name] = command

    def run_command(self, command_name: str) -> str:
        """
        指定したコマンドをシェルで実行し、標準出力を返す。
        標準エラー出力もキャプチャし、エラー時は例外を投げる。
        """
        try:
            command = self.commands[command_name]
        except KeyError:
            raise ValueError(f"unknown command: {command_name}")

        try:
            result = subprocess.run(
                shlex.split(command),
                check=False,
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"command execution error: {e.stderr.strip()}") from e
        except Exception as e:
            raise RuntimeError(f"unexpected error: {str(e)}") from e
