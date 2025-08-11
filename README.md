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

VT、VOO、QQQの人気ETFの価格を監視し、設定した割合よりも下落した場合にLINE通知する AWS Lambda ベースのアプリケーションです。

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

### LINE 通知メッセージの例
例1:
```
⚠️株価下落アラート　2025-04-03

【VT】
現在値: $100.20
前日比: -3.8%
前週比: -9.2%

【VOO】
現在値: $390.50
前日比: -3.1%
前週比: -10.0%

【QQQ】
現在値: $352.10
前日比: -5.97%
前週比: -8.5%
```

例2:
```
⚠️株価下落アラート　2020-03-16

【VT】
現在値: $61.30
前日比: -12.0%
前週比: -17.4%

【VOO】
現在値: $220.00
前日比: -11.3%
前週比: -16.2%

【QQQ】
現在値: $170.40
前日比: -11.7%
前週比: -15.3%
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

Example 1:
```
⚠️株価下落アラート　2025-04-03

【VT】
現在値: $100.20
前日比: -3.8%
前週比: -9.2%

【VOO】
現在値: $390.50
前日比: -3.1%
前週比: -10.0%

【QQQ】
現在値: $352.10
前日比: -5.97%
前週比: -8.5%
```

Example 2:
```
⚠️株価下落アラート　2020-03-16

【VT】
現在値: $61.30
前日比: -12.0%
前週比: -17.4%

【VOO】
現在値: $220.00
前日比: -11.3%
前週比: -16.2%

【QQQ】
現在値: $170.40
前日比: -11.7%
前週比: -15.3%
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

#### Run Tests

```bash
python -m pytest tests/
```

### CI/CD
Automated deployment of serverless applications with GitHub Actions and AWS SAM

- Automatically run tests and deploy on every push to the main branch.
- Execute unit tests with pytest, then package and deploy AWS Lambda functions using AWS SAM.
- Manage infrastructure as code with SAM templates, including IAM roles, APIs, and other AWS resources.