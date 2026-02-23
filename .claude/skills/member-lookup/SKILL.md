---
name: member-lookup
description: IDを指定してメンバー情報を検索する。名前・チーム・CLなど各種情報を取得できる。
---

# Member Lookup Skill

IDを指定してMemberListからメンバー情報を取得する。

## 手順

### STEP 1: IDを確認する
ユーザーにIDを質問する:
```
検索したいメンバーのIDを入力してください。
例: D001
```

### STEP 2: 取得フィールドを確認する
ユーザーに取得内容を質問する:
```
取得する情報を選んでください:
1. 日本語名のみ（デフォルト）
2. 基本情報（日本語名・拠点）
```

カスタム指定の場合は取得可能なフィールド一覧を提示してフィールド名を入力してもらう。

### STEP 3: コマンドを実行する

選択に応じて以下のコマンドを実行する:

**1. 日本語名のみ:**
```
python "./scripts/03_member_lookup.py" --id {ID}
```

**2. 基本情報:**
```
python "./scripts/03_member_lookup.py" --id {ID} --fields name_ja location
```

### STEP 4: 結果を伝える
- `status: ok` の場合: 取得した情報をわかりやすく整形して伝える
- `status: not_found` の場合: IDが見つからなかった旨を伝え、IDの入力ミスがないか確認を促す
- `status: error` の場合: エラー内容を伝える

## 取得できるフィールド一覧

| エイリアス     | Excelの列名          |
|------------|------------------|
| name_ja    | Name in Japanese |
| location   | Location         |
