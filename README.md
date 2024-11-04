
Access Database Analysis Tool

This project provides scripts to extract linked table and query information from a Microsoft Access database. Using both VBA and PowerShell, users can analyze Access databases by retrieving connection details for linked tables and SQL queries for queries within the database.

Features

	•	Linked Table Extraction: Retrieves names and connection strings for all linked tables in the database.
	•	Query Extraction: Extracts SQL statements for each query in the database.

Requirements

	•	VBA Script: Requires Microsoft Access to run directly within the Access application.
	•	PowerShell Script: Requires Microsoft Access installed on the machine to use PowerShell’s COM object for automation.

Setup Instructions

1. VBA Script Setup

	1.	Open your Access database in Microsoft Access.
	2.	Press ALT + F11 to open the VBA editor.
	3.	Insert a new module by selecting Insert > Module.
	4.	Copy and paste the VBA code provided below into the new module.

Sub ExtractLinkedTablesAndQueries()
    Dim db As Database
    Dim tbl As TableDef
    Dim qry As QueryDef
    Dim output As String
    
    ' 現在のデータベースを開く
    Set db = CurrentDb()
    
    ' リンクテーブル情報の抽出
    output = "リンクテーブル情報:" & vbCrLf
    For Each tbl In db.TableDefs
        If tbl.Connect <> "" Then
            output = output & "テーブル名: " & tbl.Name & vbCrLf
            output = output & "接続情報: " & tbl.Connect & vbCrLf & vbCrLf
        End If
    Next tbl
    
    ' クエリ情報の抽出
    output = output & "クエリ情報:" & vbCrLf
    For Each qry In db.QueryDefs
        output = output & "クエリ名: " & qry.Name & vbCrLf
        output = output & "SQL: " & qry.SQL & vbCrLf & vbCrLf
    Next qry
    
    ' 結果を表示
    MsgBox output
End Sub


	5.	Save and close the VBA editor.
	6.	Run the script by going to Developer > Macros, selecting ExtractLinkedTablesAndQueries, and clicking Run.
	7.	The script will display the extracted information in a message box.

2. PowerShell Script Setup

	1.	Open PowerShell on your computer.
	2.	Copy and paste the following script into PowerShell:

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


	3.	Modify $databasePath to point to the location of your Access .accdb file.
	4.	Run the script by pressing Enter.
	5.	The script will output the extracted information directly in the PowerShell console.

Notes

	•	Compatibility: Ensure that your version of PowerShell matches the bitness (32-bit or 64-bit) of Microsoft Access.
	•	Error Handling: If Access is not installed, or if the file path is incorrect, the PowerShell script may throw an error. Confirm the database path and Access installation before running the script.

License

This project is licensed under the MIT License. See the LICENSE file for details.

