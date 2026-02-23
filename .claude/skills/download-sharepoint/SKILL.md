---
name: download-sharepoint
description: SharePointからExcelファイルをダウンロードする
disable-model-invocation: false
---

SharePointからExcelファイルをダウンロードする:

1. 以下のPowerShellスクリプトを実行する:
```
   powershell -ExecutionPolicy Bypass -File "./scripts/01_downloadExcelFromSharepoint.ps1"
```
2. ダウンロード完了を確認する
3. ファイルが `botwork` に保存されたことを報告する
```

---

## 使い方

Claude Code上で以下を入力するだけで実行されます。
```
/download-sharepoint