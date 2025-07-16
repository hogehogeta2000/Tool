import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

# 日本語のFakerインスタンスを作成
fake = Faker('ja_JP')

# シード値を設定（再現性のため）
random.seed(42)
np.random.seed(42)
Faker.seed(42)

# 定数定義
NUM_BRANCHES = 20
NUM_EMPLOYEES = 150
NUM_CUSTOMERS = 3000
NUM_TRANSACTIONS = 50000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

# 支店データの生成
def create_branches():
    regions = ['関東', '関西', '中部', '九州', '東北', '北海道', '中国', '四国']
    branch_types = ['本店', '支店', '出張所']
    
    branches = []
    for i in range(NUM_BRANCHES):
        branch = {
            'branch_id': f'BR{i+1:03d}',
            'branch_name': f'{fake.city()}支店',
            'region': random.choice(regions),
            'branch_type': random.choices(branch_types, weights=[1, 8, 3])[0]
        }
        branches.append(branch)
    
    return pd.DataFrame(branches)

# 営業担当者データの生成
def create_employees(branches_df):
    departments = ['個人営業部', '法人営業部', '資産運用部']
    positions = ['一般', '主任', '係長', '課長', '部長']
    
    employees = []
    for i in range(NUM_EMPLOYEES):
        hire_date = fake.date_between(start_date='-10y', end_date='-1y')
        employee = {
            'employee_id': f'EMP{i+1:04d}',
            'employee_name': fake.name(),
            'branch_id': random.choice(branches_df['branch_id'].tolist()),
            'department': random.choice(departments),
            'hire_date': hire_date,
            'position': random.choices(positions, weights=[40, 25, 20, 10, 5])[0]
        }
        employees.append(employee)
    
    return pd.DataFrame(employees)

# 顧客データの生成
def create_customers(employees_df):
    customer_types = ['個人', '法人']
    industries = ['製造業', '小売業', 'サービス業', '建設業', 'IT', '医療', '不動産', 'その他']
    
    customers = []
    for i in range(NUM_CUSTOMERS):
        customer_type = random.choices(customer_types, weights=[7, 3])[0]
        customer = {
            'customer_id': f'CUST{i+1:05d}',
            'customer_name': fake.company() if customer_type == '法人' else fake.name(),
            'customer_type': customer_type,
            'industry': random.choice(industries) if customer_type == '法人' else None,
            'registration_date': fake.date_between(start_date='-5y', end_date='today'),
            'assigned_employee_id': random.choice(employees_df['employee_id'].tolist())
        }
        customers.append(customer)
    
    return pd.DataFrame(customers)

# 商品マスタの生成
def create_products():
    products = [
        # 預金商品
        {'product_id': 'PRD001', 'product_name': '普通預金', 'product_category': '預金', 'product_type': '普通預金'},
        {'product_id': 'PRD002', 'product_name': '定期預金', 'product_category': '預金', 'product_type': '定期預金'},
        {'product_id': 'PRD003', 'product_name': '積立定期預金', 'product_category': '預金', 'product_type': '積立預金'},
        
        # 融資商品
        {'product_id': 'PRD004', 'product_name': '住宅ローン', 'product_category': '融資', 'product_type': '住宅ローン'},
        {'product_id': 'PRD005', 'product_name': 'カーローン', 'product_category': '融資', 'product_type': 'マイカーローン'},
        {'product_id': 'PRD006', 'product_name': '事業性融資', 'product_category': '融資', 'product_type': '事業融資'},
        {'product_id': 'PRD007', 'product_name': 'カードローン', 'product_category': '融資', 'product_type': 'カードローン'},
        
        # 投資信託
        {'product_id': 'PRD008', 'product_name': '国内株式投信', 'product_category': '投資信託', 'product_type': '株式型'},
        {'product_id': 'PRD009', 'product_name': '海外株式投信', 'product_category': '投資信託', 'product_type': '株式型'},
        {'product_id': 'PRD010', 'product_name': 'バランス型投信', 'product_category': '投資信託', 'product_type': 'バランス型'},
        {'product_id': 'PRD011', 'product_name': '債券型投信', 'product_category': '投資信託', 'product_type': '債券型'},
        
        # 保険商品
        {'product_id': 'PRD012', 'product_name': '生命保険', 'product_category': '保険', 'product_type': '生命保険'},
        {'product_id': 'PRD013', 'product_name': '医療保険', 'product_category': '保険', 'product_type': '医療保険'},
        {'product_id': 'PRD014', 'product_name': 'がん保険', 'product_category': '保険', 'product_type': 'がん保険'},
    ]
    
    return pd.DataFrame(products)

# 営業実績データの生成
def create_sales_performance(employees_df, customers_df, products_df):
    transactions = []
    
    # 商品別の金額範囲と手数料率を定義
    amount_ranges = {
        '預金': (10000, 10000000, 0.001),
        '融資': (500000, 50000000, 0.02),
        '投資信託': (100000, 5000000, 0.03),
        '保険': (50000, 1000000, 0.15)
    }
    
    # 支店の実績傾向を設定（デモ用に特定の支店を高パフォーマンスに）
    branch_performance = {}
    for branch in employees_df['branch_id'].unique():
        # ランダムに20%の支店を高パフォーマンス支店に設定
        branch_performance[branch] = 1.5 if random.random() < 0.2 else 1.0
    
    for i in range(NUM_TRANSACTIONS):
        transaction_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
        employee_row = employees_df.sample(n=1).iloc[0]
        employee = employee_row['employee_id']
        branch = employee_row['branch_id']
        customer_row = customers_df.sample(n=1).iloc[0]
        customer = customer_row['customer_id']
        customer_type = customer_row['customer_type']
        
        # 商品選択に偏りを持たせる（顧客タイプに応じて）
        if customer_type == '個人':
            # 個人顧客は預金と保険が中心
            weights = {'預金': 0.4, '融資': 0.2, '投資信託': 0.2, '保険': 0.2}
        else:
            # 法人顧客は融資が中心
            weights = {'預金': 0.2, '融資': 0.5, '投資信託': 0.2, '保険': 0.1}
        
        # 重み付けに基づいて商品を選択
        categories = list(weights.keys())
        category_weights = list(weights.values())
        selected_category = random.choices(categories, weights=category_weights)[0]
        product = products_df[products_df['product_category'] == selected_category].sample(n=1).iloc[0]
        
        # 商品カテゴリに応じた金額と手数料を設定
        category = product['product_category']
        min_amount, max_amount, commission_rate = amount_ranges[category]
        
        # 複数の要因を組み合わせた金額計算
        base_amount = random.randint(min_amount, max_amount)
        
        # 1. 季節性（四半期末は取引増）
        month = transaction_date.month
        seasonal_factor = 1.0 + (0.3 if month in [3, 9, 12] else 0)
        
        # 2. 年次成長トレンド（2024年は2023年より20%成長）
        year = transaction_date.year
        growth_factor = 1.2 if year == 2024 else 1.0
        
        # 3. 支店パフォーマンス
        branch_factor = branch_performance.get(branch, 1.0)
        
        # 4. 営業担当者の経験（役職に応じた実績）
        position_factors = {
            '一般': 0.8,
            '主任': 1.0,
            '係長': 1.2,
            '課長': 1.5,
            '部長': 2.0
        }
        position = employee_row['position']
        position_factor = position_factors.get(position, 1.0)
        
        # 5. 曜日による傾向（月曜と金曜が多い）
        weekday = transaction_date.weekday()
        weekday_factor = 1.2 if weekday in [0, 4] else 1.0
        
        # すべての要因を組み合わせて最終的な金額を計算
        amount = base_amount * seasonal_factor * growth_factor * branch_factor * position_factor * weekday_factor
        
        # ランダム性を少し加える（±10%）
        amount = amount * (0.9 + random.random() * 0.2)
        
        commission = amount * commission_rate
        
        transaction = {
            'transaction_id': f'TRN{i+1:06d}',
            'transaction_date': transaction_date,
            'employee_id': employee,
            'customer_id': customer,
            'product_id': product['product_id'],
            'amount': int(amount),
            'commission_amount': int(commission)
        }
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

# 営業目標データの生成
def create_sales_targets(employees_df, products_df):
    targets = []
    categories = products_df['product_category'].unique()
    
    for year in [2023, 2024]:
        for month in range(1, 13):
            for _, employee in employees_df.iterrows():
                # 役職に応じた目標倍率
                position_multiplier = {
                    '一般': 1.0,
                    '主任': 1.2,
                    '係長': 1.5,
                    '課長': 2.0,
                    '部長': 3.0
                }
                
                multiplier = position_multiplier.get(employee['position'], 1.0)
                
                for category in categories:
                    # 基本目標額（カテゴリ別）
                    base_targets = {
                        '預金': 50000000,
                        '融資': 30000000,
                        '投資信託': 10000000,
                        '保険': 5000000
                    }
                    
                    target_amount = base_targets[category] * multiplier
                    
                    # 四半期末は目標を20%増
                    if month in [3, 6, 9, 12]:
                        target_amount *= 1.2
                    
                    target = {
                        'target_id': f'TGT{len(targets)+1:06d}',
                        'employee_id': employee['employee_id'],
                        'target_year': year,
                        'target_month': month,
                        'target_amount': int(target_amount),
                        'product_category': category
                    }
                    targets.append(target)
    
    return pd.DataFrame(targets)

# メイン処理
def main():
    print("デモデータの生成を開始します...")
    
    # 出力ディレクトリの作成
    output_dir = 'financial_demo_data'
    os.makedirs(output_dir, exist_ok=True)
    
    # 各テーブルの生成
    print("1. 支店データを生成中...")
    branches_df = create_branches()
    
    print("2. 営業担当者データを生成中...")
    employees_df = create_employees(branches_df)
    
    print("3. 顧客データを生成中...")
    customers_df = create_customers(employees_df)
    
    print("4. 商品データを生成中...")
    products_df = create_products()
    
    print("5. 営業実績データを生成中...")
    sales_performance_df = create_sales_performance(employees_df, customers_df, products_df)
    
    print("6. 営業目標データを生成中...")
    sales_targets_df = create_sales_targets(employees_df, products_df)
    
    # CSVファイルとして保存
    print("\nCSVファイルを保存中...")
    branches_df.to_csv(f'{output_dir}/branches.csv', index=False, encoding='utf-8-sig')
    employees_df.to_csv(f'{output_dir}/employees.csv', index=False, encoding='utf-8-sig')
    customers_df.to_csv(f'{output_dir}/customers.csv', index=False, encoding='utf-8-sig')
    products_df.to_csv(f'{output_dir}/products.csv', index=False, encoding='utf-8-sig')
    sales_performance_df.to_csv(f'{output_dir}/sales_performance.csv', index=False, encoding='utf-8-sig')
    sales_targets_df.to_csv(f'{output_dir}/sales_targets.csv', index=False, encoding='utf-8-sig')
    
    # サマリー情報の表示
    print("\n=== データ生成完了 ===")
    print(f"支店数: {len(branches_df)}")
    print(f"営業担当者数: {len(employees_df)}")
    print(f"顧客数: {len(customers_df)}")
    print(f"商品数: {len(products_df)}")
    print(f"取引件数: {len(sales_performance_df)}")
    print(f"目標レコード数: {len(sales_targets_df)}")
    print(f"\nデータは '{output_dir}' ディレクトリに保存されました。")

if __name__ == "__main__":
    main()
