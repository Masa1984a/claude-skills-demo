"""
MemberList ルックアップ
使い方: python scripts/03_memberLookup.py --id D001
        python scripts/03_memberLookup.py --id D001 --fields name_ja location
"""

import json
import argparse
import sys
from pathlib import Path

# Claude Code（WSL環境）での文字化け防止
sys.stdout.reconfigure(encoding="utf-8")

# =============================================
# .envファイルの読み込み（ルートから実行想定）
# =============================================

def load_env(env_path: Path) -> dict:
    if not env_path.exists():
        raise FileNotFoundError(f".envファイルが見つかりません: {env_path}")
    env = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        key, _, val = line.partition("=")
        env[key.strip()] = val.strip()
    return env

env = load_env(Path(".env"))

# =============================================
# 設定
# =============================================
BASE_DIR  = Path(env["BASE_DIR"])
JSON_PATH = BASE_DIR / env["OUTPUT_FILE"]

# フィールドエイリアス（将来的に追加しやすいよう定義）
FIELD_MAP = {
    "name_ja":      "Name in Japanese",
    "location":     "Location",
    "id":          "ID",
}

DEFAULT_FIELDS = ["name_ja"]  # デフォルトで返すフィールド

# =============================================
# コア処理
# =============================================

def load_members(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def find_member(members: list[dict], id: str) -> dict | None:
    return next((m for m in members if m.get("ID", "").lower() == id.lower()), None)


def build_response(member: dict | None, id: str, fields: list[str]) -> dict:
    if member is None:
        return {
            "status": "not_found",
            "id": id,
            "message": f"ID '{id}' が見つかりませんでした。",
            "data": {}
        }

    data = {}
    for alias in fields:
        col = FIELD_MAP.get(alias)
        if col:
            data[alias] = member.get(col, "")
        else:
            data[alias] = f"[unknown field: {alias}]"

    return {
        "status": "ok",
        "id": member.get("ID", id),
        "data": data
    }

# =============================================
# エントリーポイント
# =============================================

def main():
    parser = argparse.ArgumentParser(description="MemberList ID ルックアップ")
    parser.add_argument("--id",    required=True, help="検索するID")
    parser.add_argument("--fields", nargs="*",     help=f"取得フィールド ({', '.join(FIELD_MAP.keys())})")
    args = parser.parse_args()

    fields = args.fields if args.fields else DEFAULT_FIELDS

    try:
        members = load_members(JSON_PATH)
    except FileNotFoundError:
        result = {
            "status": "error",
            "message": f"JSONファイルが見つかりません: {JSON_PATH}"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    member = find_member(members, args.id)
    result = build_response(member, args.id, fields)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()