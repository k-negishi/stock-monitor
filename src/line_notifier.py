import os
import requests
from functools import wraps


def retry_notification(max_retries=3, delay=10):
    """
    通知送信用リトライデコレータ

    Args:
        max_retries (int): 最大リトライ回数
        delay (int): リトライ間隔（秒）
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    last_exception = e

                    if attempt < max_retries - 1:
                        import time
                        time.sleep(delay)

            raise last_exception if last_exception else Exception("通知送信失敗")

        return wrapper

    return decorator


class LineMessagingNotifier:
    """
    LINE Messaging APIを使用した簡易通知サービス
    """

    def __init__(self):
        """
        初期化
        """
        # 環境変数から値を取得
        self.channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        self.user_id = os.getenv('LINE_USER_ID')

        # API設定
        self.api_url = 'https://api.line.me/v2/bot/message/push'
        self.timeout = 10  # タイムアウト設定（秒）

        # ヘッダー設定
        self.headers = {
            'Authorization': f'Bearer {self.channel_access_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'StockAlertBot/2.0'
        }

    @retry_notification(max_retries=3, delay=10)
    def send_message(self, message: str) -> dict:
        """
        LINE通知メッセージを送信（リトライ機能付き）

        Args:
            message (str): 送信するメッセージ

        Returns:
            dict: API レスポンス
        """
        # リクエストボディ作成
        payload = {
            "to": self.user_id,
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }

        # API リクエスト送信
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload,
            timeout=self.timeout
        )

        if response.status_code == 200:
            return {"status": "success"}
        else:
            raise Exception(f"LINE API エラー: HTTP {response.status_code}, Message: {response.text}")
