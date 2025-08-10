import datetime
from typing import List, Dict

import pandas as pd
import yfinance as yf

from src.line_notifier import LineMessagingNotifier

# 前日比が指定%よりも下回っているかを判定する関数
def is_below_threshold(change: float, threshold: float) -> bool:
    return change <= threshold

def calculate_daily_change(stock_data: pd.DataFrame):
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
    純粋関数：閾値判定を行い、通知が必要かを判定
    
    Args:
        ticker_data_list (list): ティッカーデータのリスト
            [{'name': str, 'daily_change': float, 'weekly_change': float, 'current_price': float}, ...]
        daily_threshold (float): 日次変動の閾値
        weekly_threshold (float): 週次変動の閾値
    
    Returns:
        bool: 通知が必要かどうか（1つでも閾値を下回っていればTrue）
    """
    # 各ティッカーの閾値判定
    for ticker in ticker_data_list:
        daily_alert = is_below_threshold(ticker['daily_change'], daily_threshold)
        weekly_alert = is_below_threshold(ticker['weekly_change'], weekly_threshold)

        # 1つでも閾値を下回っていればTrueを返す
        if daily_alert or weekly_alert:
            return True

    # すべて正常範囲内
    return False


print("データ取得開始...")

targets = ['VT', 'VOO', 'QQQ']
all_data = yf.download(targets, period='1mo', group_by='ticker', auto_adjust=True)
print(all_data.index[-1].date())

# 直近の日付が現在日付-1ではない場合は、処理をスキップ
# (米国市場の休場日を判定)
# if all_data.index[-1].date() != datetime.datetime.now().date() - datetime.timedelta(days=1):
#     exit(-1)

# 各ティッカーのデータを個別の変数に格納
vt_data = all_data['VT']
voo_data = all_data['VOO']
qqq_data = all_data['QQQ']

# 個別変数を使った計算例
print(f"\n=== 個別変数を使った分析例 ===")

vt_daily_change = calculate_daily_change(vt_data)
voo_daily_change = calculate_daily_change(voo_data)
qqq_daily_change = calculate_daily_change(qqq_data)

# 1週間前との計算
vt_1wk_change = calculate_weekly_change(vt_data)
voo_1wk_change = calculate_weekly_change(voo_data)
qqq_1wk_change = calculate_weekly_change(qqq_data)

print(f"VT - 日次: {vt_daily_change}%, 週次: {vt_1wk_change}%")
print(f"VOO - 日次: {voo_daily_change}%, 週次: {voo_1wk_change}%")
print(f"QQQ - 日次: {qqq_daily_change}%, 週次: {qqq_1wk_change}%")

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

notification_needed = check_and_notify_all_tickers(ticker_data_for_check, DAILY_THRESHOLD, WEEKLY_THRESHOLD)

if notification_needed:
    def format_notification_message(ticker_data_list: List[Dict[str, float]]) -> str:
        alert_message = "📊 株価下落アラート\n\n"
        for ticker in ticker_data_list:
            alert_message += f"【{ticker['name']}】\n"
            alert_message += f"現在値: ${ticker['current_price']:.2f}\n"
            alert_message += f"前日比: {ticker['daily_change']}%\n"
            alert_message += f"前週比: {ticker['weekly_change']}%\n\n"
        return alert_message.strip()


    # LINE通知
    line_notifier = LineMessagingNotifier()
    message = format_notification_message(ticker_data_for_check)
    line_notifier.send_message(message)
