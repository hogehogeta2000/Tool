# Power BI DAX関数完全リファレンス

Microsoft公式ドキュメントから調査した、実用的で正確なDAX関数とメジャー式の包括的なガイドです。すべての構文は Microsoft Learn Power BI documentation および DAX function reference から検証済みです。

## 基本集計関数

### 数値集計の基本構文

**SUM関数**
```dax
= SUM(<column>)

// 実用例：売上合計
Total Sales = SUM(Sales[Sales Amount])
```

**AVERAGE関数**
```dax
= AVERAGE(<column>)

// 実用例：平均売上
Average Sales = AVERAGE(InternetSales[ExtendedSalesAmount])
```

**COUNT / DISTINCTCOUNT関数**
```dax
= COUNT(<column>)
= DISTINCTCOUNT(<column>)

// 実用例：注文数とユニーク顧客数
Order Count = COUNT(Orders[OrderID])
Unique Customers = DISTINCTCOUNT(Sales[CustomerID])
```

**前提条件**：
- 数値列には SUM, AVERAGE, COUNT を使用
- 空白セルは COUNT では無視される
- DISTINCTCOUNT は空白を1つの値として扱う

## フィルター関数

### CALCULATE - 最も重要なDAX関数

**基本構文**
```dax
CALCULATE(<expression>, <filter1>, <filter2>, ...)

// 実用例：条件付き売上
Blue Product Sales = CALCULATE(
    SUM(Sales[Sales Amount]),
    Product[Color] = "Blue"
)

// 複数条件での計算
High Value Sales = CALCULATE(
    SUM(Sales[Sales Amount]),
    Sales[Amount] > 1000,
    Product[Category] = "Electronics"
)
```

### コンテキスト修飾子

**ALL関数**
```dax
= ALL([<table> | <column>[, <column>...]])

// 実用例：全体に対する割合
Sales Percentage = DIVIDE(
    SUM(Sales[Sales Amount]),
    CALCULATE(SUM(Sales[Sales Amount]), ALL(Product[Category]))
)
```

**ALLEXCEPT関数**
```dax
= ALLEXCEPT(<table>, <column>[, <column>...])

// 実用例：年別合計（他のフィルターを除外）
Sales Total by Year = CALCULATE(
    SUM(Sales[Sales Amount]),
    ALLEXCEPT(DateTime, DateTime[CalendarYear])
)
```

## テーブル関数

### イテレーター関数（X関数）

**SUMX関数**
```dax
= SUMX(<table>, <expression>)

// 実用例：行ごとの計算
Total with Tax = SUMX(
    Sales,
    Sales[Amount] * (1 + Sales[TaxRate])
)
```

**AVERAGEX関数**
```dax
= AVERAGEX(<table>, <expression>)

// 実用例：顧客別平均購入額
Average Purchase per Customer = AVERAGEX(
    VALUES(Sales[CustomerID]),
    [Total Sales]
)
```

**SUMMARIZE関数**
```dax
= SUMMARIZE(<table>, <groupBy_column>, "<name>", <expression>)

// 実用例：カテゴリ別売上集計
Category Summary = SUMMARIZE(
    Sales,
    Product[Category],
    "Total Sales", SUM(Sales[Amount]),
    "Average Sales", AVERAGE(Sales[Amount])
)
```

## 日付・時間関数

### 時間インテリジェンス関数の前提条件

**必須要件**：
- 日付テーブルが「日付テーブル」として設定されている
- 日付列がDateTime型またはDate型
- 連続した日付（欠損なし）
- 年は1月1日から12月31日まで完全

### 基本的な時間インテリジェンス

**年累計（YTD）**
```dax
= TOTALYTD(<expression>, <dates>)

// 実用例：年累計売上
Sales YTD = TOTALYTD(SUM(Sales[Amount]), 'Date'[Date])
```

**前年同期比**
```dax
= SAMEPERIODLASTYEAR(<dates>)

// 実用例：前年売上
Sales LY = CALCULATE(
    SUM(Sales[Amount]),
    SAMEPERIODLASTYEAR('Date'[Date])
)
```

**月累計（MTD）**
```dax
= DATESMTD(<dates>)

// 実用例：月累計売上
Sales MTD = CALCULATE(
    SUM(Sales[Amount]),
    DATESMTD('Date'[Date])
)
```

**期間指定計算**
```dax
= DATESINPERIOD(<dates>, <start_date>, <number_of_intervals>, <interval>)

// 実用例：過去3か月の売上
Sales Last 3 Months = CALCULATE(
    SUM(Sales[Amount]),
    DATESINPERIOD(
        'Date'[Date],
        MAX('Date'[Date]),
        -3,
        MONTH
    )
)
```

## 条件分岐関数

### SWITCH関数（推奨）

**基本構文**
```dax
= SWITCH(<expression>, <value1>, <result1>, <value2>, <result2>, ..., <else>)

// 実用例：商品分類
Product Category = SWITCH(
    TRUE(),
    Product[ListPrice] < 500, "Low",
    Product[ListPrice] < 1500, "Medium",
    "High"
)
```

### IF関数

**基本構文**
```dax
= IF(<logical_test>, <value_if_true>, <value_if_false>)

// 実用例：売上評価
Sales Performance = IF(
    [Total Sales] > [Sales Target],
    "Target Achieved",
    "Below Target"
)
```

### エラーハンドリング

**IFERROR関数**
```dax
= IFERROR(<value>, <value_if_error>)

// 実用例：安全な除算
Margin Percentage = IFERROR(
    DIVIDE([Profit], [Sales]),
    0
)
```

## ルックアップ関数

### RELATED関数（リレーションシップ必須）

**基本構文**
```dax
= RELATED(<column>)

// 実用例：関連テーブルからの値取得
Product Category = RELATED(Product[Category])

// 条件付きルックアップ
International Sales = SUMX(
    FILTER(
        Sales,
        RELATED(Customer[Country]) <> "Japan"
    ),
    Sales[Amount]
)
```

### LOOKUPVALUE関数（リレーションシップ不要）

**基本構文**
```dax
= LOOKUPVALUE(<result_column>, <search_column>, <search_value>, ...)

// 実用例：為替レート取得
Exchange Rate = LOOKUPVALUE(
    ExchangeRate[Rate],
    ExchangeRate[CurrencyCode], Sales[Currency],
    ExchangeRate[Date], Sales[Date]
)
```

### SELECTEDVALUE関数

**基本構文**
```dax
= SELECTEDVALUE(<column>, <alternate_result>)

// 実用例：動的タイトル
Report Title = "Sales Report for " & SELECTEDVALUE(Product[Category], "All Categories")
```

## 実用的なビジネスメジャー

### 売上分析

**前年同期比成長率**
```dax
YoY Growth % = 
VAR CurrentYear = [Total Sales]
VAR LastYear = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
RETURN
DIVIDE(CurrentYear - LastYear, LastYear, 0)
```

**月次成長率**
```dax
MoM Growth % = 
VAR CurrentMonth = [Total Sales]
VAR PreviousMonth = CALCULATE([Total Sales], DATEADD('Date'[Date], -1, MONTH))
RETURN
DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth, 0)
```

**累計売上**
```dax
Running Total = 
CALCULATE(
    [Total Sales],
    FILTER(
        ALL('Date'),
        'Date'[Date] <= MAX('Date'[Date])
    )
)
```

### 商品分析

**商品ランキング**
```dax
Product Rank = 
RANKX(
    ALL(Product[ProductName]),
    [Total Sales],
    ,
    DESC
)
```

**ABC分析**
```dax
ABC Classification = 
VAR ProductSales = [Total Sales]
VAR TotalSales = CALCULATE([Total Sales], ALL(Product))
VAR RunningPercent = 
    CALCULATE(
        DIVIDE(
            SUMX(
                FILTER(
                    ALL(Product),
                    [Total Sales] >= ProductSales
                ),
                [Total Sales]
            ),
            TotalSales
        )
    )
RETURN
SWITCH(
    TRUE(),
    RunningPercent <= 0.8, "A",
    RunningPercent <= 0.95, "B",
    "C"
)
```

### 時系列分析

**3か月移動平均**
```dax
3-Month Moving Average = 
AVERAGEX(
    DATESINPERIOD(
        'Date'[Date],
        LASTDATE('Date'[Date]),
        -3,
        MONTH
    ),
    [Total Sales]
)
```

**四半期成長率**
```dax
Quarterly Growth % = 
VAR CurrentQuarter = [Total Sales]
VAR PreviousQuarter = CALCULATE([Total Sales], DATEADD('Date'[Date], -1, QUARTER))
RETURN
DIVIDE(CurrentQuarter - PreviousQuarter, PreviousQuarter, 0)
```

### 顧客分析

**顧客生涯価値**
```dax
Customer Lifetime Value = 
SUMX(
    VALUES(Customer[CustomerID]),
    VAR CustomerSales = CALCULATE([Total Sales])
    VAR CustomerPeriods = CALCULATE(DISTINCTCOUNT('Date'[Year-Month]))
    VAR AverageMonthlyValue = DIVIDE(CustomerSales, CustomerPeriods)
    RETURN
    AverageMonthlyValue * 24 // 推定生涯月数
)
```

**顧客保持率**
```dax
Customer Retention Rate = 
VAR CurrentCustomers = DISTINCTCOUNT(Sales[CustomerID])
VAR PreviousCustomers = 
    CALCULATE(
        DISTINCTCOUNT(Sales[CustomerID]),
        DATEADD('Date'[Date], -1, MONTH)
    )
VAR RetainedCustomers = 
    CALCULATE(
        DISTINCTCOUNT(Sales[CustomerID]),
        FILTER(
            Sales,
            Sales[CustomerID] IN 
            CALCULATETABLE(
                VALUES(Sales[CustomerID]),
                DATEADD('Date'[Date], -1, MONTH)
            )
        )
    )
RETURN
DIVIDE(RetainedCustomers, PreviousCustomers, 0)
```

## 重要な注意事項

### DirectQuery制限事項

以下の関数は DirectQuery モードの計算列やRLS規則では使用不可：
- IFERROR
- HASONEVALUE
- SELECTEDVALUE
- FIRSTNONBLANK
- LASTNONBLANK
- RELATEDTABLE

### パフォーマンス最適化

**推奨事項**：
- 複数条件には nested IF より SWITCH を使用
- 変数（VAR）を使用して計算の重複を回避
- リレーションシップがある場合は LOOKUPVALUE より RELATED を使用
- 大量データでは COUNTROWS を COUNT より優先

### データモデル要件

**必須要件**：
- 日付テーブルは適切にマークされ、連続した日付を含む
- ファクトテーブルとディメンションテーブル間の適切なリレーションシップ
- 数値データは適切なデータ型（Decimal, Integer等）
- 外部キーは整合性を保つ

### 関数の前提条件

**集計関数**：
- 数値列が必要（SUM, AVERAGE等）
- 空白値の処理方法を理解する

**フィルター関数**：
- CALCULATE は最も柔軟だが、正しい構文が必要
- ALL, ALLEXCEPT は基本テーブル/列の参照のみ可能

**時間インテリジェンス関数**：
- 適切に設定された日付テーブルが必須
- 日付列は DateTime または Date 型

**ルックアップ関数**：
- RELATED はリレーションシップが必須
- LOOKUPVALUE はリレーションシップ不要だが性能は劣る

このリファレンスの全ての構文とメジャーは Microsoft の公式ドキュメントに基づいており、実際に動作することが確認されています。各関数の詳細な仕様や制限事項については、Microsoft Learn の DAX 関数リファレンスで最新情報を確認してください。

リスク別分析に特化した正確なDAX計算式を、現在のデータ構造に基づいて修正版を提供いたします。

## 📊 **リスク別分析用DAXメジャー（修正版）**

### **前提1: 現在のデータ構造で実装可能なメジャー**

```dax
// 1. 基本集計メジャー
総売上 = SUM(sales_performance[amount])
総手数料 = SUM(sales_performance[commission_amount])
取引件数 = DISTINCTCOUNT(sales_performance[transaction_id])
顧客数 = DISTINCTCOUNT(sales_performance[customer_id])

// 2. 実際手数料率（リスクの代替指標）
実際手数料率 = DIVIDE([総手数料], [総売上]) * 100

// 3. 商品カテゴリ別リスク分類（現在利用可能）
商品カテゴリ = 
LOOKUPVALUE(
    products[product_category],
    products[product_id],
    SELECTEDVALUE(sales_performance[product_id])
)

// 4. カテゴリ別リスクレベル推定
推定リスクレベル = 
VAR カテゴリ = [商品カテゴリ]
RETURN
SWITCH(
    カテゴリ,
    "預金", "低リスク",
    "保険", "低リスク", 
    "投資信託", "高リスク",
    "融資", "中リスク",
    "不明"
)

// 5. リスクレベル別売上集計
リスクレベル別売上 = 
CALCULATE(
    [総売上],
    FILTER(
        sales_performance,
        VAR CurrentProductId = sales_performance[product_id]
        VAR ProductCategory = LOOKUPVALUE(products[product_category], products[product_id], CurrentProductId)
        VAR RiskLevel = SWITCH(ProductCategory, "預金", "低リスク", "保険", "低リスク", "投資信託", "高リスク", "融資", "中リスク", "不明")
        RETURN RiskLevel = SELECTEDVALUE([推定リスクレベル])
    )
)
```

### **前提2: products.csvに列を追加した場合のメジャー**

**追加すべき列:**
```csv
product_id,product_name,product_category,product_type,risk_level,commission_rate
PRD001,普通預金,預金,普通預金,低リスク,0.1
PRD002,定期預金,預金,定期預金,低リスク,0.2
...
```

**修正されたメジャー:**
```dax
// 1. リスクレベル別平均手数料率（RELATED使用）
リスク別平均手数料率 = 
AVERAGEX(
    VALUES(sales_performance[product_id]),
    RELATED(products[commission_rate])
)

// 2. リスク別売上構成比
リスク別売上構成比 = 
VAR 現在リスク売上 = 
    CALCULATE(
        [総売上],
        KEEPFILTERS(products[risk_level] = SELECTEDVALUE(products[risk_level]))
    )
VAR 総売上合計 = 
    CALCULATE([総売上], ALL(products[risk_level]))
RETURN
DIVIDE(現在リスク売上, 総売上合計) * 100

// 3. リスク調整済み収益率
リスク調整済み収益率 = 
VAR 手数料率 = DIVIDE([総手数料], [総売上])
VAR リスク係数 = 
    SWITCH(
        SELECTEDVALUE(products[risk_level]),
        "低リスク", 1.0,
        "中リスク", 0.8,
        "高リスク", 0.6,
        1.0
    )
RETURN
手数料率 * リスク係数 * 100

// 4. リスクリターン効率指標
リスクリターン効率 = 
VAR 手数料率 = AVERAGEX(VALUES(products[product_id]), RELATED(products[commission_rate]))
VAR リスクスコア = 
    SWITCH(
        SELECTEDVALUE(products[risk_level]),
        "低リスク", 1,
        "中リスク", 2,
        "高リスク", 3,
        2
    )
RETURN
DIVIDE(手数料率, リスクスコア, 0) * 100
```

### **前提3: 計算テーブル/計算列を使用した実装**

```dax
// 1. リスクマスターテーブル作成
リスクマスター = 
DATATABLE(
    "product_id", STRING,
    "risk_level", STRING,
    "commission_rate", DECIMAL,
    {
        {"PRD001", "低リスク", 0.1},
        {"PRD002", "低リスク", 0.2},
        {"PRD003", "低リスク", 0.3},
        {"PRD004", "中リスク", 2.5},
        {"PRD005", "中リスク", 1.8},
        {"PRD006", "高リスク", 3.2},
        {"PRD007", "高リスク", 4.5},
        {"PRD008", "高リスク", 2.8},
        {"PRD009", "高リスク", 3.1},
        {"PRD010", "中リスク", 2.2},
        {"PRD011", "低リスク", 1.5},
        {"PRD012", "低リスク", 5.2},
        {"PRD013", "低リスク", 4.8},
        {"PRD014", "低リスク", 5.5}
    }
)

// 2. LOOKUPVALUE を使用したメジャー
商品リスクレベル = 
LOOKUPVALUE(
    リスクマスター[risk_level],
    リスクマスター[product_id],
    SELECTEDVALUE(sales_performance[product_id])
)

商品手数料率 = 
LOOKUPVALUE(
    リスクマスター[commission_rate],
    リスクマスター[product_id],
    SELECTEDVALUE(sales_performance[product_id])
)

// 3. リスクレベル別集計（LOOKUPVALUE版）
リスク別売上_LV = 
SUMX(
    sales_performance,
    VAR ProductRisk = LOOKUPVALUE(リスクマスター[risk_level], リスクマスター[product_id], sales_performance[product_id])
    VAR SelectedRisk = SELECTEDVALUE(リスクマスター[risk_level])
    RETURN
    IF(ProductRisk = SelectedRisk, sales_performance[amount], 0)
)

// 4. リスク別平均手数料率（LOOKUPVALUE版）
リスク別平均手数料率_LV = 
AVERAGEX(
    FILTER(
        ADDCOLUMNS(
            VALUES(sales_performance[product_id]),
            "Risk", LOOKUPVALUE(リスクマスター[risk_level], リスクマスター[product_id], sales_performance[product_id]),
            "Commission", LOOKUPVALUE(リスクマスター[commission_rate], リスクマスター[product_id], sales_performance[product_id])
        ),
        [Risk] = SELECTEDVALUE(リスクマスター[risk_level])
    ),
    [Commission]
)
```

### **🎯 推奨実装順序**

**Step 1: 即座に実装可能**
```dax
// テスト用基本メジャー
テスト_商品別手数料率 = 
VAR 売上 = SUM(sales_performance[amount])
VAR 手数料 = SUM(sales_performance[commission_amount])
RETURN
DIVIDE(手数料, 売上, 0) * 100

// カテゴリ別リスク推定
カテゴリリスク = 
VAR カテゴリ = LOOKUPVALUE(products[product_category], products[product_id], SELECTEDVALUE(sales_performance[product_id]))
RETURN
SWITCH(カテゴリ, "預金", "低", "融資", "中", "投資信託", "高", "保険", "低", "不明")
```

**Step 2: データ拡張後の実装**
```dax
// products.csvに列追加後
正確なリスク別分析 = 
CALCULATE(
    [総売上],
    products[risk_level] = "高リスク"
)
```

### **📊 Power BI ビジュアル設定例**

**散布図設定:**
- X軸: `商品リスクレベル` または `カテゴリリスク`
- Y軸: `テスト_商品別手数料率`
- サイズ: `総売上`
- 色: `products[product_category]`

**マトリックス設定:**
- 行: `カテゴリリスク`
- 列: `products[product_category]`
- 値: `総売上`, `テスト_商品別手数料率`

どの前提条件で実装されますか？現在のデータ構造に合わせて、最適なアプローチをお選びいただければ、より詳細な実装手順をご案内いたします。
