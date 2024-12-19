# **Power AutomateでSharePointリストの変更をトリガーにしたフロー構築**

この資料では、SharePointリストの特定列が変更された場合に処理を実行するPower Automateフローの手順を説明します。  
本フローでは、タイムゾーン変換や変更時刻の取得に `formatDateTime` 関数を活用します。

---

## **フロー全体の流れ**
1. **アイテムが作成または変更されたときにトリガー**
2. **現在の時刻を取得**
3. **現在時刻を日本時間（JST）に変換**
4. **3分前の時刻を計算**
5. **`formatDateTime`を使用して日時を適切な形式に修正**
6. **変更の有無を確認して処理を分岐**

---

### **1. トリガーの設定**
トリガーには、「**SharePoint - アイテムが作成または変更されたとき**」を使用します。

#### **トリガー条件**
トリガー条件を設定し、変更がない場合にフローを実行しないようにします。

**条件式例**（空でない場合のみトリガー）：
```expression
@not(empty(triggerOutputs()?['body']))
```

---

### **2. 現在の時刻を取得**
「**現在の時刻を取得**」アクションを使用して、現在のUTC時刻を取得します。この時点ではまだUTC形式です。

---

### **3. タイムゾーンを日本時間（JST）に変換**
「**時刻の変換（Convert time zone）」アクションを追加**し、日本時間（JST）に変換します。

#### **設定項目**
- **Base time**: 「現在の時刻を取得」で得られるUTC時刻
- **Source time zone**: `(UTC) Coordinated Universal Time`
- **Destination time zone**: `(UTC+09:00) Osaka, Sapporo, Tokyo`
- **Format string**: `yyyy-MM-ddTHH:mm:ssZ`

これにより、現在時刻が日本時間に変換されます。

### **4. 3分前の時刻を計算**
「**日時を追加または減算（Add to time）」アクションを使用**し、JSTの現在時刻から3分前の時刻を計算します。

### **5. `formatDateTime`関数を使用して日時形式を修正**
「3分前の時刻」を、(6)用に変更します

#### **アクション**
「**式を適用（Compose）」アクション**を追加し、以下の式を入力します：

```expression
formatDateTime(outputs('Add_to_time'), 'yyyy-MM-ddTHH:mm:ssZ')
```

#### **ポイント**
この式で、3分前の日時をISO 8601形式に整形します。この形式は、SharePointの「Get changes for an item or a file (properties only)」アクションで使用可能です。

---

### **6. アイテムの変更を取得**
「**Get changes for an item or a file (properties only)**」アクションを使用して、SharePointリスト内の特定列が変更されたかを確認します。

こちらから変更を取得できます
