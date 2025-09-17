import os

import discord
from discord import Intents
from dotenv import load_dotenv
from src.utils.run_command import ServerManager

load_dotenv()
intents = Intents.default()
# Discordのトークンを取得(.envからとる)
TOKEN = os.environ.get("TOKEN")
client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)
# bashスクリプトのパスを指定
# bashスクリプトはexecをつけること(バッシュスクリプト内でプロセスを置き換えるため)
runner = ServerManager(bash_path="./run-server.sh")


@tree.command(name="start", description="サーバーを起動します")
async def start_server(interaction: discord.Interaction):
    await interaction.response.defer()
    runner.start()
    await interaction.followup.send("サーバーを起動しました")


@tree.command(name="stop", description="サーバーを停止します")
async def stop_server(interaction: discord.Interaction):
    await interaction.response.defer()
    runner.stop()
    await interaction.followup.send("サーバーを停止しました")


@tree.command(name="status", description="サーバーの状態を確認します")
async def status_server(interaction: discord.Interaction):
    await interaction.response.defer()
    response = runner.status()
    await interaction.followup.send(f"サーバーの状態:\n```\n{response}\n```")


@client.event
async def on_ready():
    print("Bot is ready!")
    await tree.sync()


client.run(TOKEN)
