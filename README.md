# ETF Pricing Monitor

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![AWS SAM](https://img.shields.io/badge/AWS-SAM-blueviolet.svg)](https://aws.amazon.com/serverless/sam/)
[![AWS EventBridge](https://img.shields.io/badge/AWS-EventBridge-blue.svg)](https://aws.amazon.com/eventbridge/)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)

<table>
    <thead>
        <tr>
           <th style="text-align:center"><a href="#日本語版">日本語版</a></th>
           <th style="text-align:center"><a href="#english-version">English Version</a></th>     
        </tr>
    </thead>
</table>

---

## 日本語版

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

### Line 通知メッセージの例
```
⚠️株価下落アラート

【VT】 
現在値: $98.75
前日比: -2.5%
前週比: -4.2%

【VOO】
現在値: $385.20
前日比: -1.8%
前週比: -3.1%

【QQQ】
現在値: $350.45
前日比: 0.5%
前週比: -1.2%
```

### 環境構築手順

#### Python仮想環境の作成

```bash
python -m venv .venv
source .venv/bin/activate
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

### CI/CD
GitHub Actions と AWS SAM を使用したサーバーレスアプリケーションの自動デプロイメントを実装しています。

- mainブランチへのプッシュ時に自動テスト・デプロイ実行
- pytestによるテスト実行後、AWS SAMでLambda関数をデプロイ
- AWS SAMテンプレートによるインフラストラクチャ管理（Lambda関数、EventBridge）

---

## English Version

### Overview

An AWS Lambda–based system that automatically monitors the stock prices of popular ETFs such as VT, VOO, and QQQ, and sends LINE notifications when the prices fall below predefined thresholds.

### Technologies Used
- AWS Lambda
- Python 3.13
- AWS EventBridge
- AWS SAM
- yfinance
- LINE Messaging API

### Monitored ETFs

| Symbol | Official Name | Description |
|--------|---------------|-------------|
| VT  | Vanguard Total World Stock ETF | Tracks the performance of the entire global stock market |
| VOO | Vanguard S&P 500 ETF           | Tracks the S&P 500 Index |
| QQQ | Invesco QQQ Trust              | Tracks the NASDAQ-100 Index |

### Example LINE Notification Message
Note: Notification messages are only available in Japanese.
```
⚠️株価下落アラート

【VT】 
現在値: $98.75
前日比: -2.5%
前週比: -4.2%

【VOO】
現在値: $385.20
前日比: -1.8%
前週比: -3.1%

【QQQ】現在値: $350.45
前日比: 0.5%
前週比: -1.2%
```

### Environment Setup

#### Create Python Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

### Local Development

#### Local Execution

```bash
# Execute function
sam local invoke StockAlertFunction

# Start API (for development)
sam local start-api
```

#### Run Tests

```bash
python -m pytest tests/
```

### CI/CD
Automated deployment of serverless applications with GitHub Actions and AWS SAM

- Automatically run tests and deploy on every push to the main branch.
- Execute unit tests with pytest, then package and deploy AWS Lambda functions using AWS SAM.
- Manage infrastructure as code with SAM templates, including IAM roles, APIs, and other AWS resources.