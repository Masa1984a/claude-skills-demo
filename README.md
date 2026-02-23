# Claude Code Skills Demo

Claude Code の **Skills** 機能を活用して、PowerShell・Python・Playwright を組み合わせた業務自動化のデモプロジェクトです。

SharePoint からのファイル取得・Excel 操作・データ検索・ブラウザ操作を、自然言語スラッシュコマンドで実行できます。

---

## デモで実行できること

| スキル | コマンド | 内容 |
|--------|----------|------|
| SharePoint ダウンロード | `/download-sharepoint` | SharePoint から Excel ファイルを取得し `botwork/` に保存 |
| Excel → JSON 変換 | `/excel-to-json` | ダウンロードした Excel を JSON に変換 |
| メンバー検索 | `/member-lookup` | ID を指定して JSON からメンバー情報を取得 |
| ロケーション検索 | `/search-location` | 都道府県名を指定し Playwright で Wikipedia を検索 |

---

## ディレクトリ構成

```
.
├── .claude/
│   └── skills/                   # Claude Code スキル定義
│       ├── download-sharepoint/
│       ├── excel-to-json/
│       ├── member-lookup/
│       └── search-location/
├── scripts/
│   ├── 01_downloadExcelFromSharepoint.ps1  # SharePoint ダウンロード（PowerShell）
│   ├── 02_excel_to_json_python.py          # Excel → JSON 変換（Python）
│   ├── 03_member_lookup.py                  # メンバー ID 検索（Python）
│   └── 04_search_location.py               # Wikipedia 検索（Playwright）
├── botwork/                      # スクリプトの出力先（.gitignore 対象）
├── .env                          # 環境変数（.gitignore 対象）
├── .env.example                  # 環境変数のテンプレート
└── README.md
```

---

## セットアップ

### 前提条件

- Windows 11
- [Claude Code](https://claude.ai/claude-code) インストール済み
- PowerShell 5.1 以上
- Python 3.11 以上

### 1. リポジトリのクローン

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. 環境変数の設定

`.env.example` をコピーして `.env` を作成し、自分の環境に合わせて編集してください。

```bash
cp .env.example .env
```

```env
SITE_URL=https://your-tenant.sharepoint.com/sites/YourSite
LOCAL_PATH=.\botwork\
LOCAL_FILE=your-file_local.xlsx
FILE_URL=/sites/YourSite/Shared Documents/General/your-file.xlsx

BASE_DIR=botwork
EXCEL_FILE=your-file_local.xlsx
OUTPUT_FILE=MemberList.json
SHEET_NAME=Sheet1
```

### 3. 出力ディレクトリの作成

```bash
mkdir botwork
```

### 4. Python ライブラリのインストール

```bash
pip install openpyxl playwright
python -m playwright install chromium
```

### 5. PowerShell モジュールのインストール（SharePoint スキル用）

PowerShell を**管理者権限**で開いて実行してください。

```powershell
Install-Module -Name PnP.PowerShell -Scope CurrentUser -Force
```

---

## 使い方

Claude Code を起動して、以下のスラッシュコマンドを入力するだけです。

```
/download-sharepoint   # SharePoint から Excel をダウンロード
/excel-to-json         # Excel を JSON に変換
/member-lookup         # ID でメンバーを検索
/search-location       # 都道府県の Wikipedia 情報を取得
```

各スキルは対話形式で必要な情報を質問しながら処理を進めます。

---

## 動作フロー

```
[SharePoint]
     │  /download-sharepoint (PowerShell + PnP.PowerShell)
     ▼
[botwork/所属メンバー一覧_local.xlsx]
     │  /excel-to-json (Python + openpyxl)
     ▼
[botwork/MemberList.json]
     │  /member-lookup (Python)
     ▼
[メンバー情報の表示]

[Wikipedia]
     │  /search-location (Python + Playwright)
     ▼
[都道府県の概要・目次の表示]
```

---

## スキルとスクリプトの配置について

### 2つのアプローチ

Claude Code Skills においてスクリプトの配置には、主に2つのパターンがあります。

**パターン A: スキルディレクトリ内に配置（推奨）**

```
.claude/skills/
└── download-sharepoint/
    ├── SKILL.md
    └── scripts/
        └── 01_downloadExcelFromSharepoint.ps1
```

スキルが自己完結するため、他のプロジェクトへの移植や配布がしやすくなります。スキル単位での独立性を重視する場合に適しています。

**パターン B: プロジェクトルートに `scripts/` を配置（本プロジェクトの構成）**

```
.claude/skills/        # SKILL.md のみ
scripts/               # 実装スクリプトをまとめて管理
```

### 本プロジェクトがパターン B を採用した理由

本プロジェクトのスクリプトは、番号順にパイプラインとして連携する設計になっています。

```
01_download → 02_excel_to_json → 03_member_lookup
```

`02_excel_to_json` が生成した `MemberList.json` を `03_member_lookup` が参照するように、スクリプト間に依存関係があります。このような場合、スクリプトを一箇所にまとめて管理するパターン B の方が見通しがよく、合理的です。

### 使い分けの指針

| 状況 | 推奨パターン |
|------|-------------|
| スキルを独立して配布・再利用したい | A（スキル内に配置） |
| スクリプトが複数スキル間で依存・共有している | B（プロジェクトルートに配置） |
| パイプライン的な処理フローがある | B（プロジェクトルートに配置） |

---

## 注意事項

- `.env` ファイルには SharePoint の URL などの機密情報が含まれるため、**絶対に Git にコミットしないでください**（`.gitignore` で除外済み）。
- SharePoint への接続には社内ネットワークまたは VPN が必要な場合があります。
- `/download-sharepoint` 実行時にブラウザ認証ダイアログが表示されます。
