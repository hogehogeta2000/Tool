# 1. フローの目的と概要

- **目的**  
  - Power Apps から送信された「ワークフロー情報 JSON ファイルの識別子」「ワークフローのステータスコード」「JSON コンテンツ」を用いて、SharePoint 上の情報を参照・更新したり、承認フローを実行する。
  - ワークフローの状態変化にあわせてログを残し、次工程へ繋げたり、差し戻し時には申請者へ通知を行う。

- **主な機能**  
  1. Power Apps からのトリガー引数取得  
  2. JSON の解析 (`json()` 関数・または Filter Array を活用)  
  3. ステータスコードに合致する配列要素の抽出 (Filter Array)  
  4. SharePoint List アイテムの取得・内容参照  
  5. 承認アクションの実行と結果判定  
  6. 子フローを呼び出して JSON の更新・ログ追加  
  7. エラーハンドリング (スコープ) により失敗時はログ保存や通知を実行

---

# 2. フロー全体の詳細

## 2.1 Power Apps からのトリガー入力

フローのトリガーは Power Apps (V2) を想定します。  
**Power Apps から渡される引数の例:**

1. `PowerAppsTrigger_input_jsonFileIdentifier`  
   - SharePoint ドキュメントライブラリ内の JSON ファイルを特定するための識別子 (パスまたはID)
2. `PowerAppsTrigger_input_workflowStatusCode`  
   - ワークフローのステータスコード (例: "001", "002", …)
3. `PowerAppsTrigger_input_jsonContent`  
   - 該当 JSON ファイルの実体を文字列として受け取った場合  
   - Power Apps 側で取得済みの JSON 文字列を送ってくることを想定

これらは **変数の初期化は行わず**、**トリガー出力**としてフロー内で参照します。  
たとえば動的コンテンツから `triggerOutputs()?['body/PowerAppsTrigger_input_jsonContent']` のように取得できます。

---

## 2.2 JSON コンテンツを Compose アクションに格納

再代入しない値はすべて Compose で統一して保持します。

1. **アクション名:** `Compose "cmpJsonContent"`  
   - **式または動的コンテンツ:**  
     ```
     @triggerOutputs()?['body/PowerAppsTrigger_input_jsonContent']
     ```
   - **役割:** 受け取った JSON コンテンツ文字列をフロー内で扱うために保持する

2. **アクション名:** `Compose "cmpParsedJson"`  
   - **式:**  
     ```
     json(outputs('cmpJsonContent'))
     ```
   - **役割:** `json()` 関数で文字列を JSON オブジェクトとして展開  
   - **コメント:** これにより `outputs('cmpParsedJson')?['Log']` などで直接プロパティへアクセス可能になる

---

## 2.3 ステータスコードと合致する [Log] 配列要素の抽出

**[Log] は配列**で、各要素に `"StatusCd"` プロパティが含まれる想定です。  
`PowerAppsTrigger_input_workflowStatusCode` と一致する要素を抽出し、単一オブジェクトとして取り出します。

### 2.3.1 Filter Array アクション

1. **アクション名:** `Filter array "fltLogByStatusCd"`  
   - **From:** `@outputs('cmpParsedJson')?['Log']`  
   - **Filter condition:**  
     - `item()?['StatusCd']` **Equals** `@triggerOutputs()?['body/PowerAppsTrigger_input_workflowStatusCode']`
   - **コメント:**  
     - `item()?['StatusCd']` がステータスコードと同じ要素を抽出  
     - 結果は配列になる

2. **アクション名:** `Compose "cmpLogObjectForStatus"`  
   - **式:**  
     ```
     first(body('Filter_array_fltLogByStatusCd'))
     ```
     もしくは  
     ```
     first(outputs('Filter_array_fltLogByStatusCd'))
     ```
   - **役割:** Filter で抽出された配列の先頭要素を取り出し、単一オブジェクトとして扱う  
   - **コメント:** もし常に1件だけ該当すると想定している場合は `first()` で問題ありません

> これで `cmpLogObjectForStatus` が、該当ステータスコードに対応するワークフローのログ情報 (タイトル・担当者・回答オプションなど) を保持できます。

---

## 2.4 SharePoint List アイテム取得

トランザクション対象の SharePoint List アイテムを、**ワークフロー ステータスコードとは別**のIDやキーで取得するケースを想定します。

1. **アクション名:** `Get items "getTransactionItem"`  
   - **サイトアドレス:** (対象サイトURL)  
   - **リスト名:** (対象リスト名)  
   - **Filter Query:** `ID eq @{triggerOutputs()?['body/PowerAppsTrigger_input_jsonFileIdentifier']}` など、必要に応じて  
   - **トップカウント:** 1  
   - **コメント:** 1件だけ返る想定でフィルタ

2. 必要に応じて、**Compose** などで取り出し  
   - `Compose "cmpTransactionItem"`  
   - `first(outputs('getTransactionItem')?['body/value'])` など

---

## 2.5 HTML 文面作成 (Compose)

1. **アクション名:** `Compose "cmpHtmlBody"`  
   - **内容(例):**  
     ```html
     <p>以下の申請が届いております。</p>
     <ul>
       <li>申請番号: @{outputs('cmpTransactionItem')?['ID']}</li>
       <li>申請者: @{outputs('cmpTransactionItem')?['Author']}</li>
       <li>内容: @{outputs('cmpTransactionItem')?['Description']}</li>
     </ul>
     <p>詳細は下記リンクよりご確認ください。</p>
     ```
   - **コメント:** `cmpLogObjectForStatus` 内のプロパティ(たとえばタイトル・詳細情報)を混在させてもOK

---

## 2.6 承認コネクタ実行

1. **アクション名:** `Start an approval "approvalStart"`  
   - **タイトル:** `@{outputs('cmpLogObjectForStatus')?['Title']}` など  
   - **割り当て先(承認者):** `@{outputs('cmpLogObjectForStatus')?['AssignedTo']}`  
   - **承認の種類:** カスタム応答 or 承認/却下  
   - **詳細:** `@{outputs('cmpHtmlBody')}` とか、`@{outputs('cmpLogObjectForStatus')?['Detail']}` など  
   - **選択肢:** もしカスタム応答で「承認/差し戻し/却下」など複数を使うなら設定

2. **アクション名:** `Wait for an approval "approvalWait"`  
   - **コメント:** 前のステップで開始した承認の応答結果を待つ

---

## 2.7 承認結果の分岐

1. **アクション名:** `Condition "condApprovalOutcome"`  
   - **条件:** `@equals(outputs('approvalWait')?['body/outcome'], '差し戻し')` (例)  
     - カスタム応答を使用している場合は `"Return to applicant"` など実際の文字列を比較  
   - **Yes** → 差し戻し処理  
   - **No** → 承認 (または却下) 処理

### 2.7.1 差し戻し処理

- **子フロー呼び出し**  
  - JSONファイルに差し戻しログを追加、メタデータを更新する  
- **申請者へメール通知**  
  - 差し戻し理由や修正依頼などを案内

### 2.7.2 承認/却下の場合の処理

- **子フロー呼び出し**  
  - JSONファイルに承認履歴を追加、メタデータを更新  
- **次ステータスがある場合**  
  - 別フローを呼び出す/トリガーを呼ぶ など

---

## 2.8 エラーハンドリング (スコープ)

フローの中核となる処理(メインプロセス)を**スコープ**でまとめ、そのスコープが失敗 (Fail)・タイムアウトなどを起こしたときにのみ実行される**「エラー処理用スコープ」**を配置します。

1. **アクション名:** `Scope "scpMainProcess"`  
   - **中身:**  
     - JSON解析、Filter Array、SharePoint 取得、承認、子フロー呼び出し等  
   - 正常に終わればフロー終了

2. **アクション名:** `Scope "scpErrorHandling"`  
   - **実行条件 (Run after):**  
     - `scpMainProcess` が **失敗** または **タイムアウト**  
   - **中身:**  
     1. **Compose "cmpErrorInfo"**  
        - `@actions('scpMainProcess')?['error']` を参照し、エラーコードやメッセージを抽出  
     2. **ログ保存**  
        - たとえば SharePoint ドキュメントライブラリ「エラーログ用」に JSON 形式で書き込み  
     3. **通知**  
        - 管理者・申請者に「フロー失敗」の旨をメール (あるいは Teams) で送信

---

# 3. マーメイド図による全体イメージ

下記は、**Log 配列の Filter Array → first() でオブジェクトを抽出**する流れ、**エラースコープ**を含む構成例のマーメイド図です。

```mermaid
flowchart TB
    A[Power Apps Trigger<br>
      (jsonFileIdentifier,<br>
       workflowStatusCode,<br>
       jsonContent)] --> SCOPE_MAIN

    subgraph SCOPE_MAIN[Scope: Main Process]
      direction TB
      M1[Compose<br>"cmpJsonContent"<br>
         @triggerOutputs()['…jsonContent']] --> M2
      M2[Compose<br>"cmpParsedJson"<br>
         = json(cmpJsonContent)] --> M3
      M3[Filter array<br>"fltLogByStatusCd"<br>
         From: outputs('cmpParsedJson')?['Log']<br>
         Condition: item()['StatusCd'] = workflowStatusCode] --> M4
      M4[Compose<br>"cmpLogObjectForStatus"<br>
         = first(body('fltLogByStatusCd'))] --> M5
      M5[SP Get items<br>
         "getTransactionItem"] --> M6
      M6[Compose<br>"cmpHtmlBody"] --> M7[Start an approval<br>
         "approvalStart"]
      M7 --> M8[Wait for an approval<br>"approvalWait"]
      M8 --> M9{condApprovalOutcome<br>
         outcome = 差し戻し?}
      M9 --Yes--> M10[子フロー: 差し戻し処理<br>
         (JSON 更新, メール通知)]
      M9 --No--> M11[子フロー: 承認/却下処理<br>
         (ログ追加, 次工程)]
    end

    SCOPE_MAIN -->|Success| END[End]

    SCOPE_MAIN -->|Fail/Timeout| SCOPE_ERROR

    subgraph SCOPE_ERROR[Scope: Error Handling<br>(Run After SCOPE_MAIN fails)]
      direction TB
      E1[Compose<br>"cmpErrorInfo"<br>
         @actions('scpMainProcess')['error']] --> E2
      E2[ログ書き込み<br>(エラーファイル)] --> E3[メール通知<br>(管理者・申請者)]
    end

    SCOPE_ERROR --> END
```

- **M3 → M4** がポイントで、**[Log] 配列**から**ステータスコードに合致**する要素をFilterし、**first()** で1件目を取得する流れを示しています。  
- **SCOPE_MAIN** が失敗すると **SCOPE_ERROR** が動き、エラー情報取得 → ログ保存 → 通知、となります。

---

# 4. まとめ

1. **Power Apps トリガーの引数**  
   - 変数の初期化アクションは使わず、トリガー出力(動的コンテンツ)を直接参照

2. **JSON の解析**  
   - `json()` 関数によりシンプルにオブジェクト化  
   - [Log] が配列の場合は **Filter Array** で条件抽出 → `first()` で単一要素に変換

3. **承認フロー**  
   - 単一要素化したオブジェクト (`cmpLogObjectForStatus`) のタイトルや担当者、選択肢などを承認コネクタに渡す  
   - 結果によって差し戻し or 次工程を実行

4. **エラーハンドリング スコープ**  
   - メイン処理スコープが失敗した場合のみ起動  
   - エラー情報をまとめて取得してログ化し、通知

5. **子フローの呼び出し**  
   - JSON の更新や編集履歴追加など、複数分岐で使う共通処理を一元化
