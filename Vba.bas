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
