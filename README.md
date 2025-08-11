# ETF Pricing Monitor

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![AWS SAM](https://img.shields.io/badge/AWS-SAM-blueviolet.svg)](https://aws.amazon.com/serverless/sam/)
[![AWS EventBridge](https://img.shields.io/badge/AWS-EventBridge-blue.svg)](https://aws.amazon.com/eventbridge/)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)

[English](#english) | [日本語](#japanese)

---

## 日本語 {#japanese}

### 概要

VT、VOO、QQQなどの人気ETFの株価を自動監視し、設定した閾値を下回った場合にLINE通知を送信するAWS Lambdaベースのシステムです。

### 使用技術
- AWS Lambda
- Python 3.13
- AWS EventBridge
- AWS SAM
- yfinance
- LINE Messaging API


### 監視対象ETF

| シンボル | 正式名称 | 説明 |
|----------|----------|------|
| VT | バンガード・トータルワールドストック | 世界株式市場全体を対象としたETF |
| VOO | バンガード・S&P500 | S&P500指数 |
| QQQ | インベスコQQQトラスト | NASDAQ100指数 |


### 環境構築手順

#### Python仮想環境の作成

```bash
python -m venv .venv
source .venv/bin/activates
```

#### 依存関係のインストール

```bash
pip install -r requirements.txt
```

### ローカル開発

#### ローカル実行

```bash
# 関数の実行
sam local invoke StockAlertFunction

# APIの起動（開発用）
sam local start-api
```

#### テスト実行

```bash
python -m pytest tests/
```
