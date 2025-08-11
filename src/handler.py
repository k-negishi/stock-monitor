import datetime
from typing import List, Dict

import pandas as pd
import yfinance as yf

from src.line_notifier import LineMessagingNotifier

def is_below_threshold(change: float, threshold: float) -> bool:
    return change <= threshold

def calculate_daily_change(stock_data: pd.DataFrame):
    """
    前日比の変動率を計算

    Args:
        stock_data (pd.DataFrame): 株価データ

    Returns:
        float: 前日比変動率（%、小数点以下2桁）
    """
    latest = stock_data['Close'].iloc[-1]
    previous = stock_data['Close'].iloc[-2]
    change = ((latest - previous) / previous) * 100
    return round(change, 2)

def calculate_weekly_change(stock_data: pd.DataFrame):
    """
    1週間前比の変動率を計算

    Args:
        stock_data (pd.DataFrame): 株価データ

    Returns:
        float: 変動率（%）
    """
    oldest_price = stock_data['Close'].iloc[-5]
    current_price = stock_data['Close'].iloc[-1]
    change_pct = ((current_price - oldest_price) / oldest_price) * 100
    return round(change_pct, 2)


def check_and_notify_all_tickers(
        ticker_data_list: List[Dict[str, float]],
        daily_threshold: float,
        weekly_threshold: float
) -> bool:
    """
    Args:
        ticker_data_list (list): ティッカーデータのリスト
            [{'name': str, 'daily_change': float, 'weekly_change': float, 'current_price': float}, ...]
        daily_threshold (float): 日次変動の閾値
        weekly_threshold (float): 週次変動の閾値
    
    Returns:
        bool: 通知が必要かどうか（1つでも閾値を下回っていればTrue）
    """
    # 各ティッカーの閾値判定
    return any(
        is_below_threshold(ticker['daily_change'], daily_threshold) or
        is_below_threshold(ticker['weekly_change'], weekly_threshold)
        for ticker in ticker_data_list
    )

def format_notification_message(ticker_data_list: List[Dict[str, float]]) -> str:
    """
    LINE通知用のメッセージを整形

    Args:
        ticker_data_list (List[Dict[str, float]]): ティッカーデータのリスト
            [{'name': str, 'daily_change': float, 'weekly_change': float, 'current_price': float}, ...]

      Returns:
        str: 整形されたメッセージ文字列
    """
    alert_message = "📊 株価下落アラート\n\n"
    for ticker in ticker_data_list:
        alert_message += f"【{ticker['name']}】\n"
        alert_message += f"現在値: ${ticker['current_price']:.2f}\n"
        alert_message += f"前日比: {ticker['daily_change']}%\n"
        alert_message += f"前週比: {ticker['weekly_change']}%\n\n"
    return alert_message.strip()


def lambda_handler(event, context):
    targets = ['VT', 'VOO', 'QQQ']
    all_data = yf.download(targets, period='1mo', group_by='ticker', auto_adjust=True)

    # TODO パイロット用にコメントアウト
    # 直近の日付が現在日付-1ではない場合は、処理をスキップ(米国市場の休場日を判定)
    # if all_data.index[-1].date() != datetime.datetime.now().date() - datetime.timedelta(days=1):
    #     return {
    #         'statusCode': 200,
    #         'body': {
    #             'notification_sent': False,
    #             'ticker_count': 0,
    #             'message': 'Market is closed today'
    #         }
    #     }

    # 各ティッカーのデータを個別の変数に格納
    vt_data = all_data['VT']
    voo_data = all_data['VOO']
    qqq_data = all_data['QQQ']

    # 前日との計算
    vt_daily_change = calculate_daily_change(vt_data)
    voo_daily_change = calculate_daily_change(voo_data)
    qqq_daily_change = calculate_daily_change(qqq_data)

    # 1週間前との計算
    vt_1wk_change = calculate_weekly_change(vt_data)
    voo_1wk_change = calculate_weekly_change(voo_data)
    qqq_1wk_change = calculate_weekly_change(qqq_data)

    # 閾値の設定
    DAILY_THRESHOLD = 999
    WEEKLY_THRESHOLD = 999

    ticker_data_for_check = [
        {
            'name': 'VT',
            'daily_change': vt_daily_change,
            'weekly_change': vt_1wk_change,
            'current_price': vt_data['Close'].iloc[-1]
        },
        {
            'name': 'VOO',
            'daily_change': voo_daily_change,
            'weekly_change': voo_1wk_change,
            'current_price': voo_data['Close'].iloc[-1]
        },
        {
            'name': 'QQQ',
            'daily_change': qqq_daily_change,
            'weekly_change': qqq_1wk_change,
            'current_price': qqq_data['Close'].iloc[-1]
        }
    ]

    # TODO パイロット用にコメントアウト
    # notification_needed = check_and_notify_all_tickers(ticker_data_for_check, DAILY_THRESHOLD, WEEKLY_THRESHOLD)
    notification_needed = True

    # 閾値を下回るETFが1つでも存在する場合、LINE通知を送信
    if notification_needed:
        line_notifier = LineMessagingNotifier()
        message = format_notification_message(ticker_data_for_check)
        line_notifier.send_message(message)

    # Lambda用のレスポンス
    return {
        'statusCode': 200,
        'body': {
            'notification_sent': notification_needed,
            'ticker_count': len(ticker_data_for_check),
            'message': 'Stock monitoring completed successfully'
        }
    }


# スクリプトとして実行された場合のみメイン処理を実行
if __name__ == "__main__":
    lambda_handler(None, None)
