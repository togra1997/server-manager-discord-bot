import requests

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

    def __init__(self, host: str, api_key: str, port: str, projet_name: str):
        self.host = host
        self.api_key = api_key
        self.port = port
        response = self._get_requests(host, "/environments", api_key)
        self.environment = response.get("data", [])[0].get("id", None)
        response = self._get_requests(
            host, f"/environments/{self.environment}/projects", api_key
        )

        self.projet_id = self._get_projetid(response, projet_name)

    def _get_projetid(self, response, target_name):
        for project in response.get("data", []):
            if project.get("name") == target_name:
                return project.get("id")
        return None

    def _get_requests(self, host, endpoint, api_key):
        url = f"http://{host}:{self.port}/api{endpoint}"
        headers = {"X-API-Key": api_key}
        response = requests.get(url, headers=headers)
        return response.json()

    def _post_requests(self, host, endpoint, api_key):
        url = f"http://{host}:{self.port}/api{endpoint}"
        headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
        json_data = {
            "forceRecreate": True,
            "pullPolicy": "",
            "recreateVolumes": True,
            "removeOrphans": True,
        }
        response = requests.post(url, headers=headers, json=json_data)
        return response

    def start(self) -> str:
        """
        サーバープロセスを開始します。

        Returns:
            str: サーバーの起動状態メッセージ
        """

        res = self._post_requests(
            self.host,
            f"/environments/{self.environment}/projects/{self.projet_id}/up",
            self.api_key,
        )
        if res.status_code == 200:
            return start_message
        else:
            return f"Failed to start server: {res.status_code}"

    def stop(self) -> str:
        """
        サーバープロセスを停止します。

        Returns:
            str: サーバーの停止状態メッセージ
        """

        res = self._post_requests(
            self.host,
            f"/environments/{self.environment}/projects/{self.projet_id}/down",
            self.api_key,
        )
        if res.status_code == 200:
            return stop_message
        else:
            return f"Failed to stop server: {res.status_code}"

    def status(self) -> str:
        """
        サーバープロセスの稼働状態を確認します。

        Returns:
            str: サーバーの状態メッセージ
        """

        res = self._get_requests(
            self.host,
            f"/environments/{self.environment}/projects/{self.projet_id}/runtime",
            self.api_key,
        )
        if res.get("status_code", 200) == 200:
            return f"Server status: {res.get('data', {}).get('status', 'unknown')}"
        else:
            return f"Failed to get server status: {res.get('status_code', 'unknown')}"
