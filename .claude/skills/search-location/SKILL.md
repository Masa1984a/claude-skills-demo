---
name: search-location
description: 都道府県名を指定してPlaywright（Chromium）でWikipediaを検索し、概要と目次を返す
---

# Search Location Skill

都道府県を指定してWikipediaを検索し、概要と目次を取得する。

## 手順

### STEP 1: 都道府県を確認する

ユーザーに調べたい都道府県を質問する:
```
調べたい都道府県を入力してください。
例: 東京都 / 大阪府 / 北海道
```

### STEP 2: Pythonスクリプトを実行する

```
python scripts/04_search_location.py --location "{都道府県}"
```

### STEP 3: 結果を伝える

- `status: ok` の場合: タイトル・概要・目次セクションをわかりやすく整形して伝える
- `status: error` の場合: エラー内容を伝え、Playwrightのインストール状況を確認するよう促す

## 初回セットアップ（必要な場合）

Playwrightが未インストールの場合は以下を実行:
```
pip install playwright
python -m playwright install chromium
```