import os

import discord
from discord import Intents
from dotenv import load_dotenv
from src.make_access_bat import BatMaker
from src.message import message
from src.run_command import ServerManager

load_dotenv()
intents: Intents = Intents.default()
# Discordのトークンを取得(.envから取得する)
TOKEN: str | None = os.environ.get("TOKEN")
client: discord.Client = discord.Client(intents=intents)

tree: discord.app_commands.CommandTree = discord.app_commands.CommandTree(client)
# bashスクリプトのパスを指定
# bashスクリプトはexecをつけること(バッシュスクリプト内でプロセスを置き換えるため)
runner: ServerManager = ServerManager(bash_path="./run-server.sh")


@tree.command(name="start", description="サーバーを起動します")
async def start_server(interaction: discord.Interaction) -> None:
    """
    サーバーを起動するコマンド。

    Args:
        interaction (discord.Interaction): Discordのインタラクションオブジェクト
    """
    await interaction.response.defer()
    runner.start()
    await interaction.followup.send("サーバーを起動しました")


@tree.command(name="stop", description="サーバーを停止します")
async def stop_server(interaction: discord.Interaction) -> None:
    """
    サーバーを停止するコマンド。

    Args:
        interaction (discord.Interaction): Discordのインタラクションオブジェクト
    """
    await interaction.response.defer()
    runner.stop()
    await interaction.followup.send("サーバーを停止しました")


@tree.command(name="status", description="サーバーの状態を確認します")
async def status_server(interaction: discord.Interaction) -> None:
    """
    サーバーの状態を確認するコマンド。

    Args:
        interaction (discord.Interaction): Discordのインタラクションオブジェクト
    """
    await interaction.response.defer()
    response: str = runner.status()
    await interaction.followup.send(f"サーバーの状態:\n```\n{response}\n```")


@tree.command(
    name="access", description="サーバーのアクセス用ファイルと、接続方法を送信します"
)
async def access(interaction: discord.Interaction) -> None:
    """
    access.batファイルを送信するコマンド。

    Args:
        interaction (discord.Interaction): Discordのインタラクションオブジェクト
    """

    from pathlib import Path

    url = os.environ.get("SERVER_URL")
    port = os.environ.get("CLIENT_PORT")

    maker = BatMaker(url, port)
    maker.make_file()
    path = Path("access.bat")

    await interaction.response.defer()
    await interaction.followup.send(
        message, file=discord.File(fp=str(path), filename="access.bat")
    )


@client.event
async def on_ready() -> None:
    """
    Botが起動したときに呼ばれるイベントハンドラ。
    """
    print("Bot is ready!")
    await tree.sync()


client.run(TOKEN)
