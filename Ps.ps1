# Accessアプリケーションを作成
$accessApp = New-Object -ComObject Access.Application
$databasePath = "C:\path\to\your\database.accdb"  # Accessファイルのパスを指定
$accessApp.OpenCurrentDatabase($databasePath)

# リンクテーブルの情報取得
Write-Output "リンクテーブル情報:"
foreach ($table in $accessApp.CurrentDb.TableDefs) {
    if ($table.Connect -ne "") {
        Write-Output "テーブル名: $($table.Name)"
        Write-Output "接続情報: $($table.Connect)"
        Write-Output ""
    }
}

# クエリの情報取得
Write-Output "クエリ情報:"
foreach ($query in $accessApp.CurrentDb.QueryDefs) {
    Write-Output "クエリ名: $($query.Name)"
    Write-Output "SQL: $($query.SQL)"
    Write-Output ""
}

# Accessアプリケーションを閉じる
$accessApp.CloseCurrentDatabase()
$accessApp.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($accessApp) | Out-Null
