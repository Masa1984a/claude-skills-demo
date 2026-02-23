# UTF-8 BOM付きで保存すること
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Import-Module PnP.PowerShell

# .envファイルの読み込み（ルート(/)からの実行を想定）
$envPath = Join-Path (Get-Location) ".env"
if (-not (Test-Path $envPath)) {
    Write-Error ".envファイルが見つかりません: $envPath"
    exit 1
}

foreach ($line in Get-Content $envPath -Encoding UTF8) {
    # 空行・コメント行をスキップ
    if ($line -match "^\s*$" -or $line -match "^\s*#") { continue }
    $key, $val = $line -split "=", 2
    Set-Variable -Name $key.Trim() -Value $val.Trim()
}

Write-Host "接続先: $SITE_URL"
Write-Host "ファイルURL: $FILE_URL"

Connect-PnPOnline -Url $SITE_URL -UseWebLogin

Get-PnPFile -Url $FILE_URL `
            -Path $LOCAL_PATH `
            -Filename $LOCAL_FILE `
            -AsFile `
            -Force

Write-Host "ダウンロード完了: $LOCAL_PATH$LOCAL_FILE"