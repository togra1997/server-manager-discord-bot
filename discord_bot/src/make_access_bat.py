"""サーバーアクセス用のbatファイル作成処理"""

from dataclasses import dataclass


@dataclass
class BatMaker:
    access_url: str
    port: int

    def make_command(self):
        return f"cloudflared access tcp --hostname {self.access_url} --url localhost:{self.port}"

    def make_file(self):
        command = self.make_command()

        with open("access.bat", "w") as file:
            file.write("@echo off\n")
            file.write(command)
