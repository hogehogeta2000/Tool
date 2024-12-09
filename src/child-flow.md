# エラーログ作成子フロー詳細設計

## 1. トリガー設定
- トリガータイプ: 手動トリガー
- 入力パラメータ:
```json
{
    "sourceFlow": "string（必須）",
    "errorStep": "string（必須）",
    "errorType": "string（必須）",
    "errorMessage": "string（必須）",
    "errorDetails": "string（オプション）",
    "contextParameters": "object（オプション）"
}
```

## 2. 変数初期化アクション
```
アクション: 変数の初期化
変数名: varTimestamp
型: 文字列
値: formatDateTime(utcNow(), 'yyyy-MM-dd HH:mm:ss')

アクション: 変数の初期化
変数名: varFileName
型: 文字列
値: formatDateTime(utcNow(), 'yyyy-MM-dd-HH-mm-ss')_error.json
```

## 3. ログJSON作成アクション
```
アクション: JSONの作成
入力値:
{
    "metadata": {
        "timestamp": "@{variables('varTimestamp')}",
        "sourceFlow": "@{triggerBody()?['sourceFlow']}",
        "flowRunId": "@{workflow()?['run']?['name']}",
        "environment": "@{environment()?['name']}"
    },
    "error": {
        "step": "@{triggerBody()?['errorStep']}",
        "type": "@{triggerBody()?['errorType']}",
        "message": "@{triggerBody()?['errorMessage']}",
        "details": "@{coalesce(triggerBody()?['errorDetails'], '')}"
    },
    "context": {
        "parameters": "@{coalesce(triggerBody()?['contextParameters'], null)}"
    }
}
```

## 4. SharePointファイル作成アクション
```
アクション: SharePointファイル作成
入力:
  サイトアドレス: {環境変数から取得}
  ライブラリ名: "ErrorLogs"
  ファイル名: "@{variables('varFileName')}"
  ファイルコンテンツ: {JSONの作成アクションの出力}
```

## 5. レスポンス設定アクション
```
アクション: レスポンスの設定
ステータスコード: 200
本文:
{
    "status": "success",
    "logFileUrl": "@{body('SharePointファイル作成')?['webUrl']}",
    "timestamp": "@{variables('varTimestamp')}"
}
```

## 6. エラーハンドリング
```
スコープ: エラー処理
条件: いずれかのアクションが失敗した場合
アクション: レスポンスの設定
ステータスコード: 500
本文:
{
    "status": "error",
    "error": {
        "type": "LoggingError",
        "message": "エラーログの作成に失敗しました",
        "details": "@{result('失敗したアクション')}"
    },
    "timestamp": "@{variables('varTimestamp')}"
}
```

## 7. 式の説明

### 7.1 タイムスタンプ生成
```
formatDateTime(utcNow(), 'yyyy-MM-dd HH:mm:ss')
```
- UTC時間でタイムスタンプを生成
- 一貫性のある日時形式を保証

### 7.2 ファイル名生成
```
formatDateTime(utcNow(), 'yyyy-MM-dd-HH-mm-ss')_error.json
```
- 一意のファイル名を保証
- 時系列での整理が容易

### 7.3 Null値の処理
```
coalesce(triggerBody()?['errorDetails'], '')
```
- オプションパラメータのNull安全な処理
- デフォルト値の設定
