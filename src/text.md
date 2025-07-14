## 銀行支店別事務処理手続きの可視化デモ

### 1. デモストーリー
**「事務処理の効率化で、顧客満足度と生産性を同時に向上」**

#### 背景設定
- 複数支店を持つ地方銀行での業務改善プロジェクト
- 顧客からの「手続きに時間がかかる」という声
- 支店間での処理時間・品質のばらつき

### 2. 可視化する指標（KPI）

#### 処理効率指標
- **平均処理時間**（手続き別・支店別）
- **待ち時間**（受付〜処理開始）
- **1日あたり処理件数**
- **処理エラー率**

#### 顧客満足度関連
- **手続き完了率**（当日完了/後日対応）
- **顧客クレーム件数**
- **処理時間帯分布**（混雑時間の把握）

### 3. 分析軸の拡充

#### 手続き種別（より実務的に）
- **住所変更**
  - 通常の住所変更
  - 海外転居に伴う変更
- **氏名変更**
  - 結婚による改姓
  - 離婚による改姓
- **口座関連**（追加）
  - 口座解約
  - カード再発行
- **相続手続き**（追加）

#### 時系列分析
- 月別・曜日別・時間帯別の傾向
- 繁忙期の特定（月末、給料日など）

#### 担当者別分析
- ベテラン vs 新人の処理時間差
- 研修効果の可視化

### 4. Power BIで実現するダッシュボード構成

#### エグゼクティブサマリー
- 全体KPIカード（処理件数、平均時間、満足度）
- 支店ランキング（効率性TOP5）
- アラート表示（基準値を超えた支店）

#### 詳細分析画面
- **支店比較ビュー**
  - 散布図（処理時間 × 処理件数）
  - ヒートマップ（支店×手続き種別）
- **時系列トレンド**
  - 折れ線グラフ（月次推移）
  - 曜日別・時間帯別ヒートマップ
- **ドリルダウン機能**
  - 支店 → 担当者 → 個別案件

### 5. ビジネスインパクトの訴求点

#### 定量的効果
- 処理時間20%削減による人件費削減額の試算
- 顧客離脱防止による収益保全効果
- エラー削減によるリスク低減

#### 定性的効果
- ベストプラクティスの横展開
- スタッフのモチベーション向上
- 顧客体験の改善

### 6. デモのハイライト機能

#### Power BI特有の機能紹介
- **リアルタイム更新**
  - 当日の処理状況をライブ表示
- **AI Insights**
  - 異常値の自動検出
  - 処理時間の要因分析
- **モバイル対応**
  - 支店長の外出先からの確認
- **自然言語Q&A**
  - 「最も効率的な支店は？」等の質問に即答

### 7. デモシナリオの流れ（15分想定）

1. **課題提起**（2分）
   - 現状の課題を数値で提示
2. **ダッシュボード全体像**（3分）
   - KPIの改善状況を視覚的に
3. **問題発見デモ**（5分）
   - 特定支店の問題をドリルダウンで発見
   - 原因分析（時間帯、担当者、手続き種別）
4. **改善施策の効果測定**（3分）
   - Before/Afterの比較
5. **今後の展開**（2分）
   - 他業務への展開可能性

Power BIデモ用のデータスキーマを具体化いたします。スタースキーマ形式で設計します。

## データベーススキーマ設計

### 1. ファクトテーブル

#### **F_事務処理履歴** (メインファクトテーブル)
```sql
CREATE TABLE F_事務処理履歴 (
    処理ID            INT PRIMARY KEY,
    支店ID            INT,
    従業員ID          INT,
    顧客ID            INT,
    手続きID          INT,
    処理日付ID        INT,
    受付時刻          TIME,
    処理開始時刻      TIME,
    処理完了時刻      TIME,
    待ち時間_分       INT,
    処理時間_分       INT,
    総所要時間_分     INT,
    エラー有無        BIT,
    当日完了フラグ    BIT,
    顧客満足度        INT,  -- 1-5段階
    備考              NVARCHAR(500)
)
```

### 2. ディメンションテーブル

#### **D_支店マスタ**
```sql
CREATE TABLE D_支店マスタ (
    支店ID            INT PRIMARY KEY,
    支店コード        NVARCHAR(10),
    支店名            NVARCHAR(50),
    支店区分          NVARCHAR(20),  -- 本店/支店/出張所
    地域区分          NVARCHAR(20),  -- 都市部/郊外/地方
    都道府県          NVARCHAR(20),
    住所              NVARCHAR(200),
    開設年月          DATE,
    窓口数            INT,
    従業員数          INT,
    月間来店客数_目安 INT
)
```

#### **D_従業員マスタ**
```sql
CREATE TABLE D_従業員マスタ (
    従業員ID          INT PRIMARY KEY,
    従業員番号        NVARCHAR(20),
    氏名              NVARCHAR(50),
    所属支店ID        INT,
    役職              NVARCHAR(30),  -- 支店長/課長/主任/一般
    経験年数          INT,
    スキルレベル      NVARCHAR(10),  -- 上級/中級/初級
    雇用形態          NVARCHAR(20),  -- 正社員/パート/派遣
    入社年月          DATE,
    研修受講回数      INT
)
```

#### **D_手続きマスタ**
```sql
CREATE TABLE D_手続きマスタ (
    手続きID          INT PRIMARY KEY,
    手続きコード      NVARCHAR(20),
    手続き名称        NVARCHAR(100),
    手続き大分類      NVARCHAR(50),  -- 口座管理/顧客情報変更/カード関連/相続
    手続き中分類      NVARCHAR(50),  -- 住所変更/氏名変更/再発行等
    標準処理時間_分   INT,
    必要書類数        INT,
    難易度            NVARCHAR(10),  -- 高/中/低
    本人確認レベル    NVARCHAR(10),  -- 厳格/通常/簡易
    システム処理有無  BIT
)
```

#### **D_顧客マスタ**
```sql
CREATE TABLE D_顧客マスタ (
    顧客ID            INT PRIMARY KEY,
    顧客番号          NVARCHAR(20),
    年齢層            NVARCHAR(20),  -- 20代/30代/40代/50代/60代以上
    性別              NVARCHAR(10),
    顧客区分          NVARCHAR(20),  -- 個人/法人
    顧客ランク        NVARCHAR(10),  -- プレミア/ゴールド/一般
    主要取引支店ID    INT,
    取引年数          INT,
    取引商品数        INT,
    デジタル利用区分  NVARCHAR(20)   -- ヘビー/ライト/非利用
)
```

#### **D_日付マスタ**
```sql
CREATE TABLE D_日付マスタ (
    日付ID            INT PRIMARY KEY,
    日付              DATE,
    年                INT,
    四半期            INT,
    月                INT,
    週番号            INT,
    日                INT,
    曜日              NVARCHAR(10),
    曜日番号          INT,  -- 1:月曜〜7:日曜
    営業日フラグ      BIT,
    月末フラグ        BIT,
    給料日フラグ      BIT,  -- 25日
    祝日フラグ        BIT,
    祝日名            NVARCHAR(50)
)
```

### 3. 補助テーブル

#### **D_時間帯マスタ**
```sql
CREATE TABLE D_時間帯マスタ (
    時間帯ID          INT PRIMARY KEY,
    時間              TIME,
    時間帯区分        NVARCHAR(20),  -- 開店直後/午前中/昼休み/午後/閉店前
    混雑度予想        NVARCHAR(10)   -- 高/中/低
)
```

#### **F_顧客フィードバック**
```sql
CREATE TABLE F_顧客フィードバック (
    フィードバックID  INT PRIMARY KEY,
    処理ID            INT,
    評価項目          NVARCHAR(50),  -- 待ち時間/対応品質/説明のわかりやすさ
    評価点            INT,  -- 1-5
    コメント          NVARCHAR(500),
    改善要望フラグ    BIT
)
```

#### **D_エラー詳細**
```sql
CREATE TABLE D_エラー詳細 (
    エラーID          INT PRIMARY KEY,
    処理ID            INT,
    エラー種別        NVARCHAR(50),  -- 書類不備/システムエラー/確認不足
    エラー内容        NVARCHAR(200),
    対応時間_分       INT,
    再発防止策        NVARCHAR(500)
)
```

### 4. 集計用ビュー（Power BI用）

#### **V_支店別日次集計**
```sql
CREATE VIEW V_支店別日次集計 AS
SELECT 
    s.支店名,
    d.日付,
    COUNT(f.処理ID) as 処理件数,
    AVG(f.処理時間_分) as 平均処理時間,
    AVG(f.待ち時間_分) as 平均待ち時間,
    SUM(CASE WHEN f.エラー有無 = 1 THEN 1 ELSE 0 END) as エラー件数,
    AVG(f.顧客満足度) as 平均満足度
FROM F_事務処理履歴 f
JOIN D_支店マスタ s ON f.支店ID = s.支店ID
JOIN D_日付マスタ d ON f.処理日付ID = d.日付ID
GROUP BY s.支店名, d.日付
```

### 5. リレーションシップ図

```
        D_支店マスタ ----┐
                        │
D_従業員マスタ ---------┼----> F_事務処理履歴 <---- D_時間帯マスタ
                        │           │
        D_顧客マスタ ----┤           ├---- F_顧客フィードバック
                        │           │
        D_手続きマスタ --┤           └---- D_エラー詳細
                        │
        D_日付マスタ ----┘
```

### 6. サンプルデータ生成の考慮点

- **支店数**: 20-30支店
- **従業員数**: 各支店10-30名
- **手続き種類**: 15-20種類
- **データ期間**: 過去1年分
- **1日あたり処理件数**: 支店規模により50-200件

このスキーマにより、Power BIで多角的な分析が可能になり、実務的なインサイトを導き出せます。
デモデータの準備方法について、実践的なアプローチをご提案します。

## デモデータ準備戦略

### 1. データ生成ツールの選択

#### **推奨アプローチ: Python + Faker**
```python
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker('ja_JP')
```

### 2. マスタデータ生成スクリプト

#### **支店マスタ生成**
```python
def create_branch_master():
    branches = []
    branch_types = ['本店', '支店', '出張所']
    regions = ['都市部', '郊外', '地方']
    prefectures = ['東京都', '大阪府', '愛知県', '福岡県', '北海道', 
                   '宮城県', '広島県', '神奈川県', '埼玉県', '千葉県']
    
    for i in range(25):
        branch = {
            '支店ID': i + 1,
            '支店コード': f'BR{str(i+1).zfill(3)}',
            '支店名': f'{random.choice(prefectures[0:5])}{fake.city()}支店',
            '支店区分': np.random.choice(branch_types, p=[0.1, 0.7, 0.2]),
            '地域区分': np.random.choice(regions, p=[0.4, 0.4, 0.2]),
            '都道府県': random.choice(prefectures),
            '窓口数': random.randint(3, 10),
            '従業員数': random.randint(15, 50),
            '月間来店客数_目安': random.randint(1000, 5000)
        }
        branches.append(branch)
    
    return pd.DataFrame(branches)
```

#### **手続きマスタ生成**
```python
def create_procedure_master():
    procedures = [
        # 住所変更系
        {'手続き名称': '住所変更（通常）', '大分類': '顧客情報変更', 
         '中分類': '住所変更', '標準処理時間_分': 15, '難易度': '低'},
        {'手続き名称': '住所変更（海外転居）', '大分類': '顧客情報変更', 
         '中分類': '住所変更', '標準処理時間_分': 30, '難易度': '高'},
        
        # 氏名変更系
        {'手続き名称': '氏名変更（結婚）', '大分類': '顧客情報変更', 
         '中分類': '氏名変更', '標準処理時間_分': 20, '難易度': '中'},
        {'手続き名称': '氏名変更（離婚）', '大分類': '顧客情報変更', 
         '中分類': '氏名変更', '標準処理時間_分': 20, '難易度': '中'},
        
        # その他手続き
        {'手続き名称': 'キャッシュカード再発行', '大分類': 'カード関連', 
         '中分類': '再発行', '標準処理時間_分': 10, '難易度': '低'},
        {'手続き名称': '口座解約', '大分類': '口座管理', 
         '中分類': '解約', '標準処理時間_分': 25, '難易度': '中'},
        {'手続き名称': '相続手続き', '大分類': '相続', 
         '中分類': '名義変更', '標準処理時間_分': 60, '難易度': '高'},
    ]
    
    df = pd.DataFrame(procedures)
    df['手続きID'] = range(1, len(df) + 1)
    return df
```

### 3. トランザクションデータ生成

#### **リアリスティックなパターンを含む処理履歴生成**
```python
def create_transaction_data(start_date, end_date, branches_df, procedures_df, employees_df):
    transactions = []
    current_date = start_date
    
    while current_date <= end_date:
        # 曜日による件数調整
        weekday = current_date.weekday()
        if weekday < 5:  # 平日
            base_count = 100
        else:  # 週末
            base_count = 30
            
        # 月末は1.5倍
        if current_date.day >= 25:
            base_count = int(base_count * 1.5)
        
        for branch in branches_df.itertuples():
            # 支店規模による調整
            branch_multiplier = branch.従業員数 / 30
            daily_count = int(base_count * branch_multiplier * random.uniform(0.8, 1.2))
            
            for _ in range(daily_count):
                # 時間帯による分布（開店直後と昼休み明けにピーク）
                hour_weights = [1, 2, 3, 2, 1, 1, 2, 3, 2, 1]  # 9-18時
                hour = np.random.choice(range(9, 19), p=np.array(hour_weights)/sum(hour_weights))
                minute = random.randint(0, 59)
                
                # 手続き選択（頻度に偏りを持たせる）
                procedure = procedures_df.sample(weights=[5, 1, 4, 2, 3, 2, 1]).iloc[0]
                
                # 処理時間の生成（正規分布 + 異常値）
                base_time = procedure['標準処理時間_分']
                if random.random() < 0.9:  # 90%は正常範囲
                    process_time = int(np.random.normal(base_time, base_time * 0.2))
                else:  # 10%は異常値
                    process_time = int(base_time * random.uniform(1.5, 3))
                
                # エラー発生（新人ほど高確率）
                employee = employees_df[employees_df['所属支店ID'] == branch.支店ID].sample().iloc[0]
                error_rate = 0.02 if employee['スキルレベル'] == '上級' else \
                            0.05 if employee['スキルレベル'] == '中級' else 0.10
                
                transaction = {
                    '処理ID': len(transactions) + 1,
                    '支店ID': branch.支店ID,
                    '従業員ID': employee['従業員ID'],
                    '手続きID': procedure['手続きID'],
                    '処理日付': current_date,
                    '受付時刻': f'{hour:02d}:{minute:02d}',
                    '待ち時間_分': random.randint(0, 20),
                    '処理時間_分': max(5, process_time),
                    'エラー有無': 1 if random.random() < error_rate else 0,
                    '顧客満足度': np.random.choice([1,2,3,4,5], 
                                                p=[0.05, 0.10, 0.20, 0.40, 0.25])
                }
                
                transactions.append(transaction)
        
        current_date += timedelta(days=1)
    
    return pd.DataFrame(transactions)
```

### 4. デモ用データの「仕込み」

#### **意図的なパターンの埋め込み**
```python
def add_demo_patterns(df):
    # パターン1: 特定支店の午後の処理時間が長い
    problem_branch = df[df['支店名'] == '東京中央支店'].index
    afternoon_mask = pd.to_datetime(df.loc[problem_branch, '受付時刻']).dt.hour >= 13
    df.loc[problem_branch[afternoon_mask], '処理時間_分'] *= 1.5
    
    # パターン2: 新人が多い支店のエラー率が高い
    rookie_branch = df[df['支店名'] == '埼玉新都心支店'].index
    df.loc[rookie_branch, 'エラー有無'] = \
        np.random.choice([0, 1], size=len(rookie_branch), p=[0.85, 0.15])
    
    # パターン3: 改善効果の演出（直近3ヶ月で徐々に改善）
    recent_mask = df['処理日付'] >= df['処理日付'].max() - timedelta(days=90)
    improvement_branch = df[df['支店名'] == '大阪梅田支店'].index
    
    # 時系列で改善を表現
    for idx in improvement_branch[recent_mask]:
        days_ago = (df['処理日付'].max() - df.loc[idx, '処理日付']).days
        improvement_factor = 1 - (90 - days_ago) / 90 * 0.3
        df.loc[idx, '処理時間_分'] = int(df.loc[idx, '処理時間_分'] * improvement_factor)
    
    return df
```

### 5. Excel/CSVファイル出力

```python
def export_demo_data():
    # 各種マスタデータ生成
    branches = create_branch_master()
    procedures = create_procedure_master()
    employees = create_employee_master()
    
    # トランザクションデータ生成（1年分）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    transactions = create_transaction_data(start_date, end_date, 
                                         branches, procedures, employees)
    
    # デモパターン追加
    transactions = add_demo_patterns(transactions)
    
    # Excelファイルに出力
    with pd.ExcelWriter('銀行業務デモデータ.xlsx', engine='xlsxwriter') as writer:
        branches.to_excel(writer, sheet_name='支店マスタ', index=False)
        procedures.to_excel(writer, sheet_name='手続きマスタ', index=False)
        employees.to_excel(writer, sheet_name='従業員マスタ', index=False)
        transactions.to_excel(writer, sheet_name='処理履歴', index=False)
        
        # デモ用サマリも作成
        summary = transactions.groupby(['支店名', '手続き名称']).agg({
            '処理時間_分': ['mean', 'count'],
            'エラー有無': 'sum',
            '顧客満足度': 'mean'
        }).round(2)
        summary.to_excel(writer, sheet_name='サマリ')
```

### 6. データ品質チェックリスト

#### **デモ前の確認事項**
- [ ] 全支店に十分なデータ量があるか（最低1000件/支店）
- [ ] 時系列でのトレンドが見えるか
- [ ] 異常値が適度に含まれているか（全体の5-10%）
- [ ] 改善ストーリーが数値で表現できているか
- [ ] 欠損値がないか
- [ ] 日付の連続性が保たれているか

### 7. Power BIへのインポート手順

1. **Excel版の場合**
   - Power BI Desktop起動
   - 「データを取得」→「Excel」
   - リレーションシップ自動検出ON

2. **SQL Server版の場合**
   ```sql
   -- データインポート用ストアドプロシージャ
   CREATE PROCEDURE sp_ImportDemoData
   AS
   BEGIN
       BULK INSERT D_支店マスタ
       FROM 'C:\DemoData\branches.csv'
       WITH (FORMAT = 'CSV', FIRSTROW = 2)
       -- 他のテーブルも同様
   END
   ```

3. **DirectQuery設定**（大規模デモの場合）
   - Azure SQL Databaseにデータ配置
   - Power BI ServiceでScheduled Refresh設定

このアプローチにより、リアリスティックで説得力のあるデモデータを効率的に準備できます。


<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Power BIデモ実施ロードマップ</title>
    <style>
        body {
            font-family: 'Segoe UI', 'メイリオ', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #0078d4;
            text-align: center;
            margin-bottom: 40px;
            font-size: 28px;
        }
        
        .timeline {
            position: relative;
            padding: 20px 0;
        }
        
        .phase {
            display: flex;
            margin-bottom: 30px;
            position: relative;
        }
        
        .phase-header {
            width: 200px;
            padding-right: 30px;
            text-align: right;
            flex-shrink: 0;
        }
        
        .phase-title {
            font-weight: bold;
            color: #0078d4;
            font-size: 18px;
            margin-bottom: 5px;
        }
        
        .phase-duration {
            color: #666;
            font-size: 14px;
        }
        
        .phase-content {
            flex: 1;
            border-left: 3px solid #0078d4;
            padding-left: 30px;
            position: relative;
        }
        
        .phase-content::before {
            content: '';
            position: absolute;
            left: -8px;
            top: 0;
            width: 13px;
            height: 13px;
            background: #0078d4;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 0 0 3px #e3f2fd;
        }
        
        .task-card {
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 4px solid #40e0d0;
            transition: transform 0.2s;
        }
        
        .task-card:hover {
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .task-title {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .task-details {
            color: #666;
            font-size: 14px;
            line-height: 1.6;
        }
        
        .task-people {
            display: flex;
            gap: 10px;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        
        .person-tag {
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 12px;
        }
        
        .deliverable {
            background: #fff3cd;
            padding: 8px 15px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 13px;
            color: #856404;
        }
        
        .milestone {
            background: #d4edda;
            border: 2px solid #28a745;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
            color: #155724;
        }
        
        .risk-note {
            background: #f8d7da;
            color: #721c24;
            padding: 10px 15px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 13px;
        }
        
        .icon {
            font-size: 20px;
            margin-right: 5px;
        }
        
        .gantt-chart {
            margin-top: 50px;
            overflow-x: auto;
        }
        
        .gantt-header {
            display: flex;
            background: #0078d4;
            color: white;
            padding: 10px;
            font-weight: bold;
        }
        
        .gantt-row {
            display: flex;
            border-bottom: 1px solid #ddd;
            align-items: center;
            min-height: 40px;
        }
        
        .gantt-task-name {
            width: 250px;
            padding: 10px;
            font-size: 14px;
        }
        
        .gantt-timeline {
            flex: 1;
            position: relative;
            height: 30px;
        }
        
        .gantt-bar {
            position: absolute;
            height: 20px;
            background: linear-gradient(to right, #0078d4, #40e0d0);
            border-radius: 3px;
            top: 5px;
            color: white;
            font-size: 12px;
            display: flex;
            align-items: center;
            padding: 0 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .week-marker {
            position: absolute;
            top: 0;
            bottom: 0;
            border-left: 1px solid #e0e0e0;
            width: 1px;
        }
        
        @media (max-width: 768px) {
            .phase {
                flex-direction: column;
            }
            
            .phase-header {
                width: 100%;
                text-align: left;
                padding-right: 0;
                margin-bottom: 15px;
            }
            
            .phase-content {
                border-left: none;
                padding-left: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Power BIデモ実施までのロードマップ</h1>
        
        <div class="timeline">
            <!-- Phase 1: 企画・承認フェーズ -->
            <div class="phase">
                <div class="phase-header">
                    <div class="phase-title">Phase 1</div>
                    <div class="phase-duration">1～2週目</div>
                </div>
                <div class="phase-content">
                    <div class="task-card">
                        <div class="task-title">
                            <span class="icon">📋</span>
                            企画書作成
                        </div>
                        <div class="task-details">
                            • デモの目的・効果を明確化<br>
                            • ROI試算（処理時間20%削減による効果）<br>
                            • 必要リソース・予算の整理
                        </div>
                        <div class="deliverable">
                            📄 成果物: Power BIデモ企画書.pptx
                        </div>
                        <div class="task-people">
                            <span class="person-tag">あなた</span>
                        </div>
                    </div>
                    
                    <div class="task-card">
                        <div class="task-title">
                            <span class="icon">🤝</span>
                            上席への説明・承認取得
                        </div>
                        <div class="task-details">
                            • 部長/課長への企画説明<br>
                            • フィードバック反映<br>
                            • 正式承認の取得
                        </div>
                        <div class="risk-note">
                            ⚠️ リスク: 承認が遅れる可能性 → 事前の根回しが重要
                        </div>
                        <div class="task-people">
                            <span class="person-tag">あなた</span>
                            <span class="person-tag">上席</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Phase 2: 環境準備フェーズ -->
            <div class="phase">
                <div class="phase-header">
                    <div class="phase-title">Phase 2</div>
                    <div class="phase-duration">2～3週目</div>
                </div>
                <div class="phase-content">
                    <div class="task-card">
                        <div class="task-title">
                            <span class="icon">🔐</span>
                            IT部門との調整
                        </div>
                        <div class="task-details">
                            • Python利用申請書の提出<br>
                            • セキュリティ要件の確認<br>
                            • 開発環境のセットアップ許可
                        </div>
                        <div class="deliverable">
                            📄 成果物: ツール利用申請書、セキュリティチェックリスト
                        </div>
                        <div class="task-people">
                            <span class="person-tag">あなた</span>
                            <span class="person-tag">IT部門</span>
                            <span class="person-tag">セキュリティ担当</span>
                        </div>
                    </div>
                    
                    <div class="task-card">
                        <div class="task-title">
                            <span class="icon">💻</span>
                            開発環境構築
                        </div>
                        <div class="task-details">
                            • Python環境のインストール<br>
                            • 必要ライブラリの導入（pandas, faker等）<br>
                            • Power BI Desktopの設定
                        </div>
                        <div class="risk-note">
                            ⚠️ リスク: 社内プロキシ設定でライブラリインストールに時間がかかる可能性
                        </div>
                        <div class="task-people">
                            <span class="person-tag">あなた</span>
                            <span class="person-tag">IT部門（サポート）</span>
                        </div>
                    </div>
                    
                    <div class="milestone">
                        🎯 マイルストーン: 開発環境準備完了
                    </div>
                </div>
            </div>
            
            <!-- Phase 3: データ準備フェーズ -->
            <div class="phase">
                <div class="phase-header">
                    <div class="phase-title">Phase 3</div>
                    <div class="phase-duration">3～4週目</div>
                </div>
                <div class="phase-content">
                    <div class="task-card">
                        <div class="task-title">
                            <span class="icon">🗄️</span>
                            スキーマ設計・レビュー
                        </div>
                        <div class="task-details">
                            • データモデルの詳細設計<br>
                            • 業務部門とのレビュー会実施<br>
                            • フィードバック反映
                        </div>
                        <div class="deliverable">
                            📄 成果物: データベース設計書
                        </div>
                        <div class="task-people">
                            <span class="person-tag">あなた</span>
                            <span class="person-tag">業務部門</span>
                        </div>
                    </div>
                    
                    <div class="task-card">
                        <div class="task-title">
                            <span class="icon">🐍</span>
                            Pythonでデモデータ生成
                        </div>
                        <div class="task-details">
                            • マスタデータ生成スクリプト作成<br>
                            • トランザクションデータ生成（1年分）<br>
                            • デモシナリオ用パターンの埋め込み
                        </div>
                        <div class="deliverable">
                            📄 成果物: デモデータ生成スクリプト、銀行業務デモデータ.xlsx
                        </div>
                        <div class="task-people">
                            <span class="person-tag">あなた</span>
                        </div>
                    </div>
                    
                    <div class="task-card">
                        <div class="task-title">
                            <span class="icon">✅</span>
                            データ品質確認
                        </div>
                        <div class="task-details">
                            • データ整合性チェック<br>
                            • 業務観点での妥当性確認<br>
                            • デモストーリーとの整合性確認
                        </div>
                        <div class="task-people">
                            <span class="person-tag">あなた</span>
                            <span class="person-tag">業務部門（確認）</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Phase 4: ダッシュボード開発フェーズ -->
            <div class="phase">
                <div class="phase-header">
                    <div class="phase-title">Phase 4</div>
                    <div class="phase-duration">4～5週目</div>
                </div>
                <div class="phase-content">
                    <div class="task-card">
                        <div class="task-title">
                            <span class="icon">📊</span>
                            Power BIダッシュボード作成
                        </div>
                        <div class="task-details">
                            • データインポート・リレーション設定<br>
                            • 各種ビジュアルの作成<br>
                            • DAX計算式の実装<br>
                            • ドリルダウン機能の設定
                        </div>
                        <div class="deliverable">
                            📄 成果物: 銀行業務分析ダッシュボード.pbix
                        </div>
                        <div class="task-people">
                            <span class="person-tag">あなた</span>
                        </div>
                    </div>
                    
                    <div class="task-card">
                        <div class="task-title">
                            <span class="icon">🎨</span>
                            UI/UXブラッシュアップ
                        </div>
                        <div class="task-details">
                            • 配色・レイアウトの調整<br>
                            • インタラクティブ機能の追加<br>
                            • モバイルビューの最適化
                        </div>
                        <div class="task-people">
                            <span class="person-tag">あなた</span>
                            <span class="person-tag">デザイン担当（相談）</span>
                        </div>
                    </div>
                    
                    <div class="milestone">
                        🎯 マイルストーン: ダッシュボード完成
                    </div>
                </div>
            </div>
            
            <!-- Phase 5: デモ準備・実施フェーズ -->
            <div class="phase">
                <div class="phase-header">
                    <div class="phase-title">Phase 5</div>
                    <div class="phase-duration">5～6週目</div>
                </div>
                <div class="phase-content">
                    <div class="task-card">
                        <div class="task-title">
                            <span class="icon">🎭</span>
                            デモシナリオ作成・リハーサル
                        </div>
                        <div class="task-details">
                            • 15分のデモフロー確定<br>
                            • 説明資料の作成<br>
                            • 社内リハーサル実施（3回）
                        </div>
                        <div class="deliverable">
                            📄 成果物: デモシナリオ台本、説明スライド
                        </div>
                        <div class="task-people">
                            <span class="person-tag">あなた</span>
                            <span class="person-tag">チームメンバー</span>
                        </div>
                    </div>
                    
                    <div class="task-card">
                        <div class="task-title">
                            <span class="icon">🚀</span>
                            ITフェスティバルでのデモ実施
                        </div>
                        <div class="task-details">
                            • ブース設営<br>
                            • デモ実演（複数回）<br>
                            • 質疑応答対応<br>
                            • フィードバック収集
                        </div>
                        <div class="risk-note">
                            ⚠️ 注意: バックアップ環境の準備、オフラインでも動作可能な設定
                        </div>
                        <div class="task-people">
                            <span class="person-tag">あなた</span>
                            <span class="person-tag">サポートスタッフ</span>
                        </div>
                    </div>
                    
                    <div class="milestone">
                        🎉 最終マイルストーン: デモ実施完了！
                    </div>
                </div>
            </div>
        </div>
        
        <!-- ガントチャート -->
        <div class="gantt-chart">
            <h2 style="color: #0078d4; margin-bottom: 20px;">📅 タイムライン（6週間）</h2>
            <div class="gantt-header">
                <div class="gantt-task-name">タスク</div>
                <div class="gantt-timeline" style="display: flex;">
                    <div style="flex: 1; text-align: center;">Week 1</div>
                    <div style="flex: 1; text-align: center;">Week 2</div>
                    <div style="flex: 1; text-align: center;">Week 3</div>
                    <div style="flex: 1; text-align: center;">Week 4</div>
                    <div style="flex: 1; text-align: center;">Week 5</div>
                    <div style="flex: 1; text-align: center;">Week 6</div>
                </div>
            </div>
            
            <div class="gantt-row">
                <div class="gantt-task-name">企画・承認</div>
                <div class="gantt-timeline">
                    <div class="gantt-bar" style="left: 0%; width: 33%;">Phase 1</div>
                </div>
            </div>
            
            <div class="gantt-row">
                <div class="gantt-task-name">環境準備</div>
                <div class="gantt-timeline">
                    <div class="gantt-bar" style="left: 16%; width: 33%;">Phase 2</div>
                </div>
            </div>
            
            <div class="gantt-row">
                <div class="gantt-task-name">データ準備</div>
                <div class="gantt-timeline">
                    <div class="gantt-bar" style="left: 33%; width: 33%;">Phase 3</div>
                </div>
            </div>
            
            <div class="gantt-row">
                <div class="gantt-task-name">ダッシュボード開発</div>
                <div class="gantt-timeline">
                    <div class="gantt-bar" style="left: 50%; width: 33%;">Phase 4</div>
                </div>
            </div>
            
            <div class="gantt-row">
                <div class="gantt-task-name">デモ準備・実施</div>
                <div class="gantt-timeline">
                    <div class="gantt-bar" style="left: 66%; width: 34%;">Phase 5</div>
                </div>
            </div>
        </div>
        
        <!-- 成功のポイント -->
        <div style="margin-top: 40px; padding: 20px; background: #e3f2fd; border-radius: 8px;">
            <h3 style="color: #0078d4; margin-bottom: 15px;">🔑 成功のポイント</h3>
            <ul style="line-height: 1.8; color: #333;">
                <li><strong>早期の根回し:</strong> IT部門・セキュリティ部門との事前相談で承認をスムーズに</li>
                <li><strong>段階的な確認:</strong> 各フェーズで関係者レビューを実施し、手戻りを防止</li>
                <li><strong>リスク管理:</strong> Python利用許可の遅延、ネットワーク制限等を想定した代替案準備</li>
                <li><strong>デモの練習:</strong> 本番環境と同等の環境でリハーサルを重ねる</li>
                <li><strong>フィードバック収集:</strong> デモ後のアンケートで今後の展開につなげる</li>
            </ul>
        </div>
    </div>
</body>
</html>


金融機関でのPower BIデモ実施に向けた段取りを可視化いたします。段取りを可視化したロードマップを作成しました。金融機関特有の以下のポイントを考慮しています：

## 重要な考慮事項

### 1. **承認プロセスの重要性**
- 金融機関では新しいツール導入に慎重なため、早期の根回しが必須
- ROI（投資対効果）の明確な提示が承認の鍵

### 2. **セキュリティ要件**
- Python利用には情報セキュリティ部門の承認が必要
- データは架空のものを使用することを明記
- 社内ネットワークでのライブラリインストール制限への対処

### 3. **段階的アプローチ**
- 各フェーズでチェックポイントを設定
- 関係部門との連携を密に取る
- 手戻りリスクを最小化

### 4. **リスク対策**
- Python承認が下りない場合：Excelで手動データ作成の代替案
- ネットワーク制限：オフライン環境での動作確認
- 当日のトラブル：スタンドアロン版の準備

### 5. **成功要因**
- 業務部門を早期に巻き込み、実務的な視点を反映
- デモリハーサルを複数回実施
- 質問想定集の準備

この段取りに沿って進めることで、スムーズなデモ実施が可能になります。特に金融機関では承認プロセスに時間がかかることが多いため、余裕を持ったスケジュールで計画することをお勧めします。

Power BIデモ用の最終成果物となるダッシュボードを作成いたします。Power BIデモ用の最終成果物ダッシュボードを作成しました。このダッシュボードの特徴とデモでのアピールポイントをご説明します。

## ダッシュボードの主要機能

### 1. **KPIカード（エグゼクティブサマリー）**
- 平均処理時間、顧客満足度、エラー率、処理件数を一目で確認
- 前月比での改善/悪化を視覚的に表示
- アラートバッジで注意が必要な指標を強調

### 2. **支店別分析**
- 棒グラフで支店間の処理時間を比較
- 問題のある支店（東京中央支店）が一目瞭然
- クリックで詳細データへドリルダウン可能

### 3. **ヒートマップ分析**
- 支店×手続き種別のクロス分析
- 色の濃淡で処理時間の長短を直感的に把握
- 特定の組み合わせの問題を発見しやすい

### 4. **時系列トレンド**
- 12ヶ月の改善推移を可視化
- 改善施策の実施ポイントを明示
- 効果測定が容易

### 5. **詳細テーブル**
- 各支店のパフォーマンスを総合的に評価
- ステータス表示で優先対応すべき支店を識別

## デモでの効果的な見せ方

### ストーリー展開
1. **現状把握**（2分）
   - KPIカードでエラー率の上昇を指摘
   - 「要注意」アラートをクリック

2. **問題の特定**（3分）
   - 東京中央支店の処理時間が突出
   - ヒートマップで「口座解約」が特に遅いことを発見

3. **原因分析**（3分）
   - ドリルダウン機能で担当者レベルまで分析
   - 午後の時間帯に処理が遅延することを発見

4. **改善効果の提示**（2分）
   - 大阪梅田支店の改善事例を紹介
   - トレンドグラフで施策実施後の効果を数値で示す

### インタラクティブ要素の活用
- 各要素をクリックして詳細表示
- フィルター機能で特定条件での分析
- リアルタイム更新で「生きたデータ」をアピール

### ビジネス価値の訴求
- 処理時間20%削減 = 年間○○万円の人件費削減
- 顧客満足度向上による離脱防止効果
- ベストプラクティスの横展開による全体最適化

このダッシュボードにより、単なるデータの可視化ではなく、具体的なアクションにつながるインサイトを提供できることをデモで強調してください。



<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>銀行支店別事務処理分析ダッシュボード</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'メイリオ', sans-serif;
            background-color: #f2f2f2;
            color: #333;
            overflow-x: hidden;
        }
        
        /* ヘッダー */
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 15px 30px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 300;
        }
        
        .last-update {
            font-size: 14px;
            opacity: 0.9;
        }
        
        /* フィルターバー */
        .filter-bar {
            background: white;
            padding: 15px 30px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .filter-item {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        
        .filter-label {
            font-size: 12px;
            color: #666;
            font-weight: 600;
        }
        
        select {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
            cursor: pointer;
            font-size: 14px;
        }
        
        /* メインコンテンツ */
        .dashboard-content {
            padding: 20px;
            max-width: 1600px;
            margin: 0 auto;
        }
        
        /* KPIカード */
        .kpi-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .kpi-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
            border-left: 4px solid #0078d4;
            cursor: pointer;
        }
        
        .kpi-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .kpi-card.green { border-left-color: #48c774; }
        .kpi-card.orange { border-left-color: #ff9800; }
        .kpi-card.red { border-left-color: #f44336; }
        .kpi-card.purple { border-left-color: #9c27b0; }
        
        .kpi-title {
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        .kpi-value {
            font-size: 32px;
            font-weight: 700;
            color: #333;
            margin-bottom: 5px;
        }
        
        .kpi-change {
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .kpi-change.positive { color: #48c774; }
        .kpi-change.negative { color: #f44336; }
        
        /* チャートセクション */
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
        }
        
        .chart-title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
        }
        
        .chart-actions {
            display: flex;
            gap: 10px;
        }
        
        .chart-action {
            padding: 5px 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s;
        }
        
        .chart-action:hover {
            background: #0078d4;
            color: white;
            border-color: #0078d4;
        }
        
        /* 詳細テーブル */
        .detail-section {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th {
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            color: #666;
            border-bottom: 2px solid #dee2e6;
        }
        
        td {
            padding: 12px;
            border-bottom: 1px solid #eee;
            font-size: 14px;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        /* チャート要素 */
        .bar-chart {
            display: flex;
            align-items: flex-end;
            height: 300px;
            gap: 15px;
            padding: 20px 0;
        }
        
        .bar-group {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            cursor: pointer;
        }
        
        .bar {
            width: 100%;
            background: linear-gradient(to top, #0078d4, #40a9ff);
            border-radius: 4px 4px 0 0;
            transition: all 0.3s;
            position: relative;
            min-height: 20px;
        }
        
        .bar:hover {
            background: linear-gradient(to top, #005a9e, #0078d4);
            transform: translateY(-5px);
        }
        
        .bar-value {
            position: absolute;
            top: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 14px;
            font-weight: 600;
            color: #333;
            white-space: nowrap;
        }
        
        .bar-label {
            margin-top: 10px;
            font-size: 12px;
            color: #666;
            text-align: center;
            max-width: 100px;
        }
        
        /* ヒートマップ */
        .heatmap {
            display: grid;
            grid-template-columns: 100px repeat(4, 1fr);
            gap: 2px;
            margin-top: 20px;
        }
        
        .heatmap-cell {
            padding: 15px 10px;
            text-align: center;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }
        
        .heatmap-header {
            background: #f8f9fa;
            font-weight: 600;
            color: #666;
        }
        
        .heatmap-row-header {
            background: #f8f9fa;
            font-weight: 600;
            color: #666;
            text-align: left;
            padding-left: 15px;
        }
        
        .heatmap-cell:not(.heatmap-header):not(.heatmap-row-header) {
            color: white;
            font-weight: 500;
        }
        
        .heatmap-cell:hover:not(.heatmap-header):not(.heatmap-row-header) {
            transform: scale(1.1);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            z-index: 10;
        }
        
        /* 折れ線グラフ */
        .line-chart {
            height: 300px;
            position: relative;
            margin: 20px 0;
        }
        
        .line-chart-grid {
            position: absolute;
            width: 100%;
            height: 100%;
            border-left: 2px solid #ddd;
            border-bottom: 2px solid #ddd;
        }
        
        .line-chart-line {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        
        /* ポップアップ */
        .tooltip {
            position: absolute;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 12px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 1000;
        }
        
        .tooltip.show {
            opacity: 1;
        }
        
        /* レスポンシブ */
        @media (max-width: 768px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }
            
            .filter-bar {
                flex-direction: column;
                align-items: stretch;
            }
            
            .bar-chart {
                height: 250px;
            }
        }
        
        /* アニメーション */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .kpi-card, .chart-container, .detail-section {
            animation: slideIn 0.5s ease-out forwards;
        }
        
        .kpi-card:nth-child(1) { animation-delay: 0.1s; }
        .kpi-card:nth-child(2) { animation-delay: 0.2s; }
        .kpi-card:nth-child(3) { animation-delay: 0.3s; }
        .kpi-card:nth-child(4) { animation-delay: 0.4s; }
        
        /* アラートバッジ */
        .alert-badge {
            display: inline-block;
            background: #f44336;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            margin-left: 10px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏦 銀行支店別事務処理分析ダッシュボード</h1>
        <div class="last-update">最終更新: 2025年7月14日 10:30</div>
    </div>
    
    <div class="filter-bar">
        <div class="filter-item">
            <label class="filter-label">対象期間</label>
            <select id="periodFilter">
                <option>過去30日間</option>
                <option>過去90日間</option>
                <option>過去1年間</option>
                <option>カスタム期間</option>
            </select>
        </div>
        <div class="filter-item">
            <label class="filter-label">地域</label>
            <select id="regionFilter">
                <option>全地域</option>
                <option>都市部</option>
                <option>郊外</option>
                <option>地方</option>
            </select>
        </div>
        <div class="filter-item">
            <label class="filter-label">手続き種別</label>
            <select id="procedureFilter">
                <option>全手続き</option>
                <option>住所変更</option>
                <option>氏名変更</option>
                <option>口座関連</option>
                <option>カード関連</option>
            </select>
        </div>
        <div class="filter-item">
            <label class="filter-label">支店規模</label>
            <select id="sizeFilter">
                <option>全規模</option>
                <option>大規模（30名以上）</option>
                <option>中規模（15-29名）</option>
                <option>小規模（14名以下）</option>
            </select>
        </div>
    </div>
    
    <div class="dashboard-content">
        <!-- KPIセクション -->
        <div class="kpi-section">
            <div class="kpi-card" onclick="showDetail('processing-time')">
                <div class="kpi-title">平均処理時間</div>
                <div class="kpi-value">18.5分</div>
                <div class="kpi-change positive">
                    <span>▼ 12.3%</span>
                    <span>前月比</span>
                </div>
            </div>
            
            <div class="kpi-card green" onclick="showDetail('satisfaction')">
                <div class="kpi-title">顧客満足度</div>
                <div class="kpi-value">4.2<span style="font-size: 20px">/5</span></div>
                <div class="kpi-change positive">
                    <span>▲ 0.3pt</span>
                    <span>前月比</span>
                </div>
            </div>
            
            <div class="kpi-card orange" onclick="showDetail('error-rate')">
                <div class="kpi-title">エラー発生率<span class="alert-badge">要注意</span></div>
                <div class="kpi-value">3.8%</div>
                <div class="kpi-change negative">
                    <span>▲ 0.5%</span>
                    <span>前月比</span>
                </div>
            </div>
            
            <div class="kpi-card purple" onclick="showDetail('daily-volume')">
                <div class="kpi-title">1日平均処理件数</div>
                <div class="kpi-value">2,456件</div>
                <div class="kpi-change positive">
                    <span>▲ 8.7%</span>
                    <span>前月比</span>
                </div>
            </div>
        </div>
        
        <!-- チャートセクション -->
        <div class="charts-grid">
            <!-- 支店別処理時間 -->
            <div class="chart-container">
                <div class="chart-header">
                    <h3 class="chart-title">支店別平均処理時間（分）</h3>
                    <div class="chart-actions">
                        <button class="chart-action" onclick="sortChart()">並び替え</button>
                        <button class="chart-action" onclick="drillDown()">詳細表示</button>
                    </div>
                </div>
                <div class="bar-chart" id="branchChart">
                    <div class="bar-group" onclick="showBranchDetail('東京中央')">
                        <div class="bar" style="height: 85%">
                            <span class="bar-value">25.3分</span>
                        </div>
                        <span class="bar-label">東京中央支店</span>
                    </div>
                    <div class="bar-group" onclick="showBranchDetail('大阪梅田')">
                        <div class="bar" style="height: 45%">
                            <span class="bar-value">13.5分</span>
                        </div>
                        <span class="bar-label">大阪梅田支店</span>
                    </div>
                    <div class="bar-group" onclick="showBranchDetail('名古屋栄')">
                        <div class="bar" style="height: 60%">
                            <span class="bar-value">18.0分</span>
                        </div>
                        <span class="bar-label">名古屋栄支店</span>
                    </div>
                    <div class="bar-group" onclick="showBranchDetail('福岡天神')">
                        <div class="bar" style="height: 55%">
                            <span class="bar-value">16.5分</span>
                        </div>
                        <span class="bar-label">福岡天神支店</span>
                    </div>
                    <div class="bar-group" onclick="showBranchDetail('札幌大通')">
                        <div class="bar" style="height: 70%">
                            <span class="bar-value">21.0分</span>
                        </div>
                        <span class="bar-label">札幌大通支店</span>
                    </div>
                </div>
            </div>
            
            <!-- 手続き別ヒートマップ -->
            <div class="chart-container">
                <div class="chart-header">
                    <h3 class="chart-title">支店×手続き別処理時間ヒートマップ</h3>
                    <div class="chart-actions">
                        <button class="chart-action" onclick="toggleHeatmapView()">表示切替</button>
                    </div>
                </div>
                <div class="heatmap" id="heatmap">
                    <div class="heatmap-cell heatmap-header"></div>
                    <div class="heatmap-cell heatmap-header">住所変更</div>
                    <div class="heatmap-cell heatmap-header">氏名変更</div>
                    <div class="heatmap-cell heatmap-header">口座解約</div>
                    <div class="heatmap-cell heatmap-header">カード再発行</div>
                    
                    <div class="heatmap-cell heatmap-row-header">東京中央</div>
                    <div class="heatmap-cell" style="background: #ff6b6b" onclick="showCellDetail('東京中央', '住所変更', 28)">28分</div>
                    <div class="heatmap-cell" style="background: #ff9f40" onclick="showCellDetail('東京中央', '氏名変更', 22)">22分</div>
                    <div class="heatmap-cell" style="background: #feca57" onclick="showCellDetail('東京中央', '口座解約', 35)">35分</div>
                    <div class="heatmap-cell" style="background: #48c774" onclick="showCellDetail('東京中央', 'カード再発行', 12)">12分</div>
                    
                    <div class="heatmap-cell heatmap-row-header">大阪梅田</div>
                    <div class="heatmap-cell" style="background: #48c774" onclick="showCellDetail('大阪梅田', '住所変更', 12)">12分</div>
                    <div class="heatmap-cell" style="background: #48c774" onclick="showCellDetail('大阪梅田', '氏名変更', 15)">15分</div>
                    <div class="heatmap-cell" style="background: #20bf6b" onclick="showCellDetail('大阪梅田', '口座解約', 20)">20分</div>
                    <div class="heatmap-cell" style="background: #0fb9b1" onclick="showCellDetail('大阪梅田', 'カード再発行', 8)">8分</div>
                    
                    <div class="heatmap-cell heatmap-row-header">名古屋栄</div>
                    <div class="heatmap-cell" style="background: #feca57" onclick="showCellDetail('名古屋栄', '住所変更', 18)">18分</div>
                    <div class="heatmap-cell" style="background: #ff9f40" onclick="showCellDetail('名古屋栄', '氏名変更', 20)">20分</div>
                    <div class="heatmap-cell" style="background: #feca57" onclick="showCellDetail('名古屋栄', '口座解約', 25)">25分</div>
                    <div class="heatmap-cell" style="background: #48c774" onclick="showCellDetail('名古屋栄', 'カード再発行', 10)">10分</div>
                    
                    <div class="heatmap-cell heatmap-row-header">福岡天神</div>
                    <div class="heatmap-cell" style="background: #48c774" onclick="showCellDetail('福岡天神', '住所変更', 15)">15分</div>
                    <div class="heatmap-cell" style="background: #feca57" onclick="showCellDetail('福岡天神', '氏名変更', 18)">18分</div>
                    <div class="heatmap-cell" style="background: #ff9f40" onclick="showCellDetail('福岡天神', '口座解約', 22)">22分</div>
                    <div class="heatmap-cell" style="background: #48c774" onclick="showCellDetail('福岡天神', 'カード再発行', 9)">9分</div>
                </div>
            </div>
        </div>
        
        <!-- トレンドチャート -->
        <div class="chart-container" style="margin-bottom: 30px;">
            <div class="chart-header">
                <h3 class="chart-title">処理時間の推移（過去12ヶ月）</h3>
                <div class="chart-actions">
                    <button class="chart-action" onclick="changeTimeRange()">期間変更</button>
                    <button class="chart-action" onclick="addComparison()">比較追加</button>
                </div>
            </div>
            <div class="line-chart">
                <svg width="100%" height="300" viewBox="0 0 800 300" preserveAspectRatio="none">
                    <!-- グリッド線 -->
                    <g stroke="#e0e0e0" stroke-width="1">
                        <line x1="0" y1="60" x2="800" y2="60" />
                        <line x1="0" y1="120" x2="800" y2="120" />
                        <line x1="0" y1="180" x2="800" y2="180" />
                        <line x1="0" y1="240" x2="800" y2="240" />
                    </g>
                    
                    <!-- 折れ線グラフ -->
                    <polyline
                        fill="none"
                        stroke="#0078d4"
                        stroke-width="3"
                        points="0,200 66,190 133,195 200,180 266,170 333,165 400,150 466,140 533,130 600,120 666,115 733,110"
                    />
                    
                    <!-- データポイント -->
                    <g fill="#0078d4">
                        <circle cx="0" cy="200" r="5" />
                        <circle cx="66" cy="190" r="5" />
                        <circle cx="133" cy="195" r="5" />
                        <circle cx="200" cy="180" r="5" />
                        <circle cx="266" cy="170" r="5" />
                        <circle cx="333" cy="165" r="5" />
                        <circle cx="400" cy="150" r="5" />
                        <circle cx="466" cy="140" r="5" />
                        <circle cx="533" cy="130" r="5" />
                        <circle cx="600" cy="120" r="5" />
                        <circle cx="666" cy="115" r="5" />
                        <circle cx="733" cy="110" r="5" />
                    </g>
                    
                    <!-- 改善ポイントのマーカー -->
                    <g>
                        <circle cx="400" cy="150" r="8" fill="#ff6b6b" opacity="0.8" />
                        <text x="410" y="145" font-size="12" fill="#666">改善施策実施</text>
                    </g>
                </svg>
            </div>
        </div>
        
        <!-- 詳細テーブル -->
        <div class="detail-section">
            <div class="chart-header">
                <h3 class="chart-title">支店別パフォーマンス詳細</h3>
                <div class="chart-actions">
                    <button class="chart-action" onclick="exportData()">データ出力</button>
                    <button class="chart-action" onclick="refreshData()">更新</button>
                </div>
            </div>
            <table id="detailTable">
                <thead>
                    <tr>
                        <th>支店名</th>
                        <th>処理件数</th>
                        <th>平均処理時間</th>
                        <th>エラー率</th>
                        <th>顧客満足度</th>
                        <th>改善率</th>
                        <th>ステータス</th>
                    </tr>
                </thead>
                <tbody>
                    <tr onclick="showBranchDetail('東京中央支店')">
                        <td>東京中央支店</td>
                        <td>458件</td>
                        <td>25.3分</td>
                        <td style="color: #f44336">5.2%</td>
                        <td>3.8/5</td>
                        <td style="color: #f44336">-2.3%</td>
                        <td><span style="background: #ffebee; color: #f44336; padding: 2px 8px; border-radius: 12px; font-size: 12px;">要改善</span></td>
                    </tr>
                    <tr onclick="showBranchDetail('大阪梅田支店')">
                        <td>大阪梅田支店</td>
                        <td>523件</td>
                        <td>13.5分</td>
                        <td style="color: #48c774">1.2%</td>
                        <td>4.6/5</td>
                        <td style="color: #48c774">+15.8%</td>
                        <td><span style="background: #e8f5e9; color: #48c774; padding: 2px 8px; border-radius: 12px; font-size: 12px;">優良</span></td>
                    </tr>
                    <tr onclick="showBranchDetail('名古屋栄支店')">
                        <td>名古屋栄支店</td>
                        <td>387件</td>
                        <td>18.0分</td>
                        <td style="color: #ff9800">3.5%</td>
                        <td>4.1/5</td>
                        <td style="color: #48c774">+5.2%</td>
                        <td><span style="background: #fff3e0; color: #ff9800; padding: 2px 8px; border-radius: 12px; font-size: 12px;">標準</span></td>
                    </tr>
                    <tr onclick="showBranchDetail('福岡天神支店')">
                        <td>福岡天神支店</td>
                        <td>412件</td>
                        <td>16.5分</td>
                        <td style="color: #48c774">2.8%</td>
                        <td>4.3/5</td>
                        <td style="color: #48c774">+8.7%</td>
                        <td><span style="background: #e8f5e9; color: #48c774; padding: 2px 8px; border-radius: 12px; font-size: 12px;">良好</span></td>
                    </tr>
                    <tr onclick="showBranchDetail('札幌大通支店')">
                        <td>札幌大通支店</td>
                        <td>276件</td>
                        <td>21.0分</td>
                        <td style="color: #ff9800">4.1%</td>
                        <td>3.9/5</td>
                        <td style="color: #ff9800">+1.2%</td>
                        <td><span style="background: #fff3e0; color: #ff9800; padding: 2px 8px; border-radius: 12px; font-size: 12px;">要観察</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- ツールチップ -->
    <div class="tooltip" id="tooltip"></div>
    
    <script>
        // フィルター機能
        document.querySelectorAll('select').forEach(select => {
            select.addEventListener('change', (e) => {
                console.log(`フィルター変更: ${e.target.id} = ${e.target.value}`);
                // 実際のPower BIではここでデータが更新される
                showNotification('フィルターが適用されました');
            });
        });
        
        // KPIカードクリック
        function showDetail(kpiType) {
            console.log(`KPI詳細表示: ${kpiType}`);
            showNotification(`${kpiType}の詳細分析画面を表示`);
        }
        
        // 支店詳細表示
        function showBranchDetail(branchName) {
            console.log(`支店詳細: ${branchName}`);
            showNotification(`${branchName}の詳細データをドリルダウン`);
        }
        
        // セル詳細表示
        function showCellDetail(branch, procedure, time) {
            showNotification(`${branch}の${procedure}: 平均${time}分\n担当者別分析を表示`);
        }
        
        // チャートソート
        function sortChart() {
            showNotification('処理時間の長い順に並び替えました');
        }
        
        // ドリルダウン
        function drillDown() {
            showNotification('担当者レベルの詳細データを表示');
        }
        
        // データエクスポート
        function exportData() {
            showNotification('Excelファイルとしてダウンロード開始');
        }
        
        // データ更新
        function refreshData() {
            showNotification('最新データに更新中...');
            setTimeout(() => {
                showNotification('データが更新されました');
            }, 1500);
        }
        
        // 通知表示
        function showNotification(message) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #333;
                color: white;
                padding: 15px 25px;
                border-radius: 4px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                z-index: 10000;
                animation: slideIn 0.3s ease-out;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => notification.remove(), 300);
            }, 2000);
        }
        
        // ホバー効果
        document.querySelectorAll('.bar, .heatmap-cell:not(.heatmap-header):not(.heatmap-row-header)').forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                const tooltip = document.getElementById('tooltip');
                tooltip.textContent = '詳細データを表示';
                tooltip.style.left = e.pageX + 10 + 'px';
                tooltip.style.top = e.pageY - 30 + 'px';
                tooltip.classList.add('show');
            });
            
            element.addEventListener('mouseleave', () => {
                document.getElementById('tooltip').classList.remove('show');
            });
        });
        
        // リアルタイム更新シミュレーション
        setInterval(() => {
            // KPI値を微小に変動させる
            const kpiValues = document.querySelectorAll('.kpi-value');
            kpiValues[3].textContent = (2450 + Math.floor(Math.random() * 20)) + '件';
        }, 5000);
        
        // スタイルアニメーション用
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideOut {
                to {
                    opacity: 0;
                    transform: translateX(50px);
                }
            }
        `;
        document.head.appendChild(style);
        
        // 初期メッセージ
        setTimeout(() => {
            showNotification('ダッシュボードへようこそ！各要素をクリックして詳細を確認できます。');
        }, 1000);
    </script>
</body>
</html>

