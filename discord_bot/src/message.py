import os

from dotenv import load_dotenv

load_dotenv()
port = os.environ.get("CLIENT_PORT")
message = f"""
アクセス方法
初回のみ
1. cloudflareアプリのインストール
Windowsの場合は、以下のコマンドをコマンドプロンプトで実行して、cloudflareアプリをインストールしてください。
LinuxやMacの場合は以下を参考にしてください。
[参考](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/)
```
winget install --id Cloudflare.cloudflared
```
2. cloudflareの認証情報の追加
サーバー管理者に依頼して、cloudflare accessのアプリケーションで認証が行えるように依頼してください。

2回目以降
1. バッチファイルの入手
添付のaccess.batファイルをダウンロードしてください。
このファイルは接続先のサーバーごとに異なります。

2. バッチファイルの実行
ダウンロードしたaccess.batファイルをダブルクリックして実行してください。

3. ゲームからサーバーへの接続
ゲームのサーバーで、以下へアクセスしてください。
```
localhost:{port}
```
Cloudflare accessの認証が求められた場合は、認証を行ってください。
これでcloudflare accessを通じてサーバーに接続できます。
"""
