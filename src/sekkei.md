以下では、前回ご提案したフロー構成をベースに、**依頼事項**に沿って修正・補足した内容をまとめます。  
加えて、マーメイド図による簡易的なフロー図を提示しています。

---

## 1. Power Apps トリガー入力と引数の命名

### 1.1 Power Apps トリガーで取得する引数

- **`PowerAppsTrigger_input_jsonFileIdentifier`**  
  - **役割:** SharePoint ドキュメント ライブラリ内のワークフロー情報 JSON ファイルの識別子  
- **`PowerAppsTrigger_input_workflowStatusCode`**  
  - **役割:** ワークフローのステータスを表すコード  
- **`PowerAppsTrigger_input_jsonContent`**  
  - **役割:** 上記識別子をもとに取得・または Power Apps 側で取得した JSON ファイルコンテンツ (文字列)

これらは **Power Apps から直接入力**されるため、**変数の初期化アクションは不要**です。  
フロー内では、**トリガー出力として利用可能な動的コンテンツ**として参照します。

---

## 2. 変数(Compose) アクションへの統一

### 2.1 再代入しない値は「Compose」で保持

以前は「初期化アクション (Initialize variable)」を使用していましたが、  
**再代入しない** 場合は以下のように「Compose」アクションで値を取り扱いします。

1. **アクション名:** `Compose "cmpJsonContent"`  
   - **内容:** `@triggerOutputs()?['body/PowerAppsTrigger_input_jsonContent']`  
   - **役割:** JSON ファイルコンテンツ (文字列) をフロー内で扱うための保持

2. **アクション名:** `Compose "cmpLogObjectForStatus"`  
   - **内容:** 後で判定・抽出したステータス該当ログオブジェクトをセット  
   - **役割:** ステータスコードと合致する `Log` オブジェクトを格納

3. **アクション名:** `Compose "cmpHtmlBody"`  
   - **内容:** メールや承認依頼で用いる HTML 文字列を格納  
   - **役割:** 後段の「承認コネクタ」や「メール送信」などに渡す

---

## 3. JSON ファイルの解析 (`json()` 関数の活用)

JSON ファイルのスキーマが事前に判明している場合、**Parse JSON** アクションを使わず、以下のように `json()` 関数を活用するとフローが簡潔になります。

1. **アクション名:** `Compose "cmpParsedJson"`  
   - **式:**  
     ```txt
     json(outputs('cmpJsonContent'))
     ```
   - **コメント:**  
     これにより、後続で `outputs('cmpParsedJson')?['Log']` 等のようにプロパティへアクセスできます。

2. **ステータスコードと合致する `Log` の抽出**  
   - たとえば Filter Array アクションや条件分岐を使わず、`cmpParsedJson` の構造が明確であれば直接式でアクセスすることも可能です。  
   - 例:  
     ```txt
     outputs('cmpParsedJson')?['Log']?[variables('PowerAppsTrigger_input_workflowStatusCode')]
     ```
     ※ JSON の構造次第ですが、もし「ログ」配列に `"statusCode"` プロパティがあるなら `filter(...)` などで抽出できます。

3. **抽出結果を `cmpLogObjectForStatus` に設定**  
   - **アクション名:** `Compose "cmpLogObjectForStatus"`  
   - **内容:** 上記式(もしくはフィルタ結果)の出力  
   - **コメント:** 以降、このオブジェクトを参照して承認コネクタを設定する

---

## 4. フロー全体の流れ (要点のみ)

前回の提案から変更のない流れを簡略化して列挙します。

1. **Power Apps トリガー**  
   - 3 つの引数 (`jsonFileIdentifier`, `workflowStatusCode`, `jsonContent`) を受け取る

2. **Compose "cmpJsonContent"**  
   - `PowerAppsTrigger_input_jsonContent` をセット (ここでは文字列)

3. **Compose "cmpParsedJson"** (json 関数)  
   - `json(outputs('cmpJsonContent'))` を実行  
   - 結果として、JSON オブジェクト全体を扱える

4. **ステータスコードに応じた `Log` 抽出**  
   - `cmpLogObjectForStatus` へ必要情報を格納 (Compose)

5. **SharePoint Lists アイテム取得**  
   - `PowerAppsTrigger_input_workflowStatusCode` などから対象リストアイテムを取得  
   - 必要に応じてメール文面作成用の情報を抜き出し

6. **Compose "cmpHtmlBody"**  
   - メール/承認依頼で用いる HTML 文字列を作成し格納

7. **承認コネクタ実行**  
   - `cmpLogObjectForStatus` の内容を使い、承認者・選択肢・詳細等を設定

8. **承認結果判定**  
   - 差し戻しかどうか分岐し、それぞれの処理(更新ログの追加、メール送信、次ステータス用フロー呼び出しなど)

9. **子フロー呼び出し**  
   - JSON のメタデータ更新や編集ログの追加などを行う子フローを実行 (フロー内のアクションとして呼び出し)

10. **エラーハンドリング (スコープ)**  
   - 失敗時にはスコープ外でログ書き込み・通知を実行

---

## 5. マーメイド図 (Mermaid) によるフロー概念図

以下の例は、簡易的なマーメイド図です。実際の構成やアクション数はもっと多くなる場合がありますが、要点のみを視覚化しています。

```mermaid
flowchart TB
    A[Power Apps<br>Trigger] --> B[Compose: cmpJsonContent<br>jsonContentを格納]
    B --> C[Compose: cmpParsedJson<br>json(outputs('cmpJsonContent'))]
    C --> D[Extract Log<br>(cmpLogObjectForStatus)]
    D --> E[Get SP List Item<br>フィルタ ID=...]
    E --> F[Compose: cmpHtmlBody<br>(HTML文面)]
    F --> G[Start an approval<br>(承認コネクタ)]
    G --> H{承認結果<br>(差し戻し？)}
    H -- No --> I[子フロー呼び出し<br>Update JSON<br>ログ追加<br>次ステータスフロー呼び出し]
    H -- Yes --> J[子フロー呼び出し<br>差し戻しログ追加<br>申請者へメール]
    I --> K[End]
    J --> K[End]

    subgraph "Error Handling Scope"
       M[Main Process] --> N[On Error<br>Log & Notification]
    end
```

- **Power Apps Trigger**: トリガー引数として `jsonFileIdentifier`, `workflowStatusCode`, `jsonContent` を受領  
- **cmpJsonContent**: JSON 文字列を保持 (Compose)  
- **cmpParsedJson**: `json()` 関数でパースした JSON オブジェクトを保持  
- **cmpLogObjectForStatus**: ステータスコードに合致する `Log` 情報を抽出し格納  
- **承認コネクタ (Start an approval)**: タイトル、担当者、回答オプション等を `cmpLogObjectForStatus` から設定  
- **承認結果 (差し戻し分岐)**: カスタムオプション「差し戻し」で分岐  
- **子フロー呼び出し**: それぞれ JSON の更新や編集履歴追加を行う共通処理  
- **エラー時**: 失敗時はスコープ外でログ記録や通知 (管理者・申請者など)

---

## まとめ

1. **Power Apps トリガー**で取得した値 (JsonFileIdentifier, WorkflowStatusCode, JsonContent) は「変数の初期化」を行わず、そのままフロー内で参照します。  
2. **再代入されない値**は「Compose」を使用し、わかりやすい名前 (例: `cmpJsonContent`, `cmpParsedJson`, `cmpHtmlBody`) で統一します。  
3. **JSON の解析**は `json()` 関数を用いることでフローを簡潔にし、後続のプロパティアクセスを容易にします。  
4. **子フローの呼び出し**によって、複数ステータス分岐で共通的に必要な SharePoint 更新やログ追加処理をまとめて保守性を高めます。  
5. **エラーハンドリング**はスコープを活用してログ記録・通知を行い、ワークフロー全体の安定運用を確保します。

これらを組み合わせることで、よりシンプルかつ運用管理しやすい Power Automate フロー設計が可能になります。
