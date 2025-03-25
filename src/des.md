Option Public
Option Declare

Use "NotesUIWorkspace"

' 添付ファイル一括エクスポート用のメイン関数
Sub Initialize
    Dim session As New NotesSession
    Dim db As NotesDatabase
    Dim dc As NotesDocumentCollection
    Dim doc As NotesDocument
    Dim item As NotesItem
    Dim rtitem As NotesRichTextItem
    Dim object As NotesEmbeddedObject
    Dim exportDir As String
    Dim fileName As String
    Dim count As Integer
    
    On Error Goto ErrorHandler
    
    ' エクスポート先ディレクトリの設定
    exportDir = "C:\ExportedAttachments\"
    
    ' ディレクトリが存在しない場合は作成する
    If Not DirectoryExists(exportDir) Then
        Call CreateDirectory(exportDir)
    End If
    
    ' 現在のデータベースを取得
    Set db = session.CurrentDatabase
    
    ' 対象となる文書のコレクションを取得
    ' 必要に応じてクエリ条件を変更してください
    Set dc = db.AllDocuments
    
    Print "添付ファイルのエクスポートを開始します..."
    Print "対象文書数: " & dc.Count
    
    count = 0
    
    ' 各文書をループ処理
    Set doc = dc.GetFirstDocument
    While Not doc Is Nothing
        ' 文書のUniversal IDを取得（ファイル名の一部として使用）
        Dim unid As String
        unid = doc.UniversalID
        
        ' すべての項目を処理
        Forall item In doc.Items
            ' リッチテキスト項目のみを処理
            If item.Type = RICHTEXT Then
                Set rtitem = doc.GetFirstItem(item.Name)
                
                ' 埋め込みオブジェクト（添付ファイル）を処理
                Forall object In rtitem.EmbeddedObjects
                    If object.Type = EMBED_ATTACHMENT Then
                        ' 添付ファイル名を取得
                        fileName = object.Name
                        
                        ' ファイル名にドキュメントUNIDを付加して一意にする
                        Dim exportPath As String
                        exportPath = exportDir & unid & "_" & fileName
                        
                        ' ファイルをエクスポート
                        Call object.ExtractFile(exportPath)
                        
                        ' 追加情報（オプション）を別ファイルに保存
                        ' 例: 文書のタイトルやその他のフィールド情報
                        Call SaveMetadata(exportPath & ".meta", doc, fileName)
                        
                        count = count + 1
                        Print count & ": " & fileName & " をエクスポートしました。"
                    End If
                End Forall
            End If
        End Forall
        
        ' 次の文書に進む
        Set doc = dc.GetNextDocument(doc)
    Wend
    
    Print "エクスポート完了。合計 " & count & " 個の添付ファイルをエクスポートしました。"
    Print "エクスポート先: " & exportDir
    
    Exit Sub
    
ErrorHandler:
    Print "エラーが発生しました: " & Error$ & " (エラーコード: " & Err & ")"
    Print "処理を中断します。"
    Exit Sub
End Sub

' メタデータを保存する補助関数
Function SaveMetadata(filePath As String, doc As NotesDocument, attachmentName As String) As Boolean
    Dim fileNum As Integer
    
    On Error Goto MetadataError
    
    fileNum = FreeFile()
    Open filePath For Output As fileNum
    
    ' 文書に関するメタデータを書き込む
    Print #fileNum, "Original Document UNID: " & doc.UniversalID
    Print #fileNum, "Attachment Name: " & attachmentName
    Print #fileNum, "Export Date: " & Format(Now, "yyyy-MM-dd HH:mm:ss")
    
    ' 任意のフィールドを追加（例）
    If Not doc.GetItemValue("Subject")(0) = "" Then
        Print #fileNum, "Subject: " & doc.GetItemValue("Subject")(0)
    End If
    
    If Not doc.GetItemValue("Author")(0) = "" Then
        Print #fileNum, "Author: " & doc.GetItemValue("Author")(0)
    End If
    
    ' 文書の作成日時
    Print #fileNum, "Created: " & Format$(doc.Created, "yyyy-MM-dd HH:mm:ss")
    
    Close fileNum
    SaveMetadata = True
    Exit Function
    
MetadataError:
    Print "メタデータの保存中にエラーが発生しました: " & Error$
    SaveMetadata = False
    Exit Function
End Function

' ディレクトリの存在確認
Function DirectoryExists(dirPath As String) As Boolean
    On Error Goto DirError
    
    Dim fileNum As Integer
    Dim tempFile As String
    
    If Right(dirPath, 1) <> "\" Then
        dirPath = dirPath & "\"
    End If
    
    tempFile = dirPath & "tempfile.tmp"
    fileNum = FreeFile()
    
    Open tempFile For Output As fileNum
    Close fileNum
    Kill tempFile
    
    DirectoryExists = True
    Exit Function
    
DirError:
    DirectoryExists = False
    Exit Function
End Function

' ディレクトリ作成
Sub CreateDirectory(dirPath As String)
    Dim cmd As String
    cmd = "CMD.EXE /C MKDIR """ & dirPath & """"
    Shell(cmd)
End Sub
