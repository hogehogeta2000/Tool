import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

fake = Faker('ja_JP')


def create_branch_master():
    """支店マスタデータを生成"""
    branches = []
    branch_types = ['本店', '支店', '出張所']
    regions = ['都市部', '郊外', '地方']
    prefectures = ['東京都', '大阪府', '愛知県', '福岡県', '北海道', 
                   '宮城県', '広島県', '神奈川県', '埼玉県', '千葉県']
    
    # 特定の支店名を確実に含める（デモシナリオ用）
    fixed_branches = [
        {'name': '東京中央支店', 'pref': '東京都', 'region': '都市部', 'type': '支店'},
        {'name': '大阪梅田支店', 'pref': '大阪府', 'region': '都市部', 'type': '支店'},
        {'name': '埼玉新都心支店', 'pref': '埼玉県', 'region': '郊外', 'type': '支店'},
    ]
    
    for i in range(25):
        if i < len(fixed_branches):
            # 固定支店
            branch = {
                '支店ID': i + 1,
                '支店コード': f'BR{str(i+1).zfill(3)}',
                '支店名': fixed_branches[i]['name'],
                '支店区分': fixed_branches[i]['type'],
                '地域区分': fixed_branches[i]['region'],
                '都道府県': fixed_branches[i]['pref'],
                '窓口数': random.randint(5, 10),
                '従業員数': random.randint(20, 50),
                '月間来店客数_目安': random.randint(2000, 5000)
            }
        else:
            # ランダム支店
            branch = {
                '支店ID': i + 1,
                '支店コード': f'BR{str(i+1).zfill(3)}',
                '支店名': f'{random.choice(prefectures)}{fake.city()}支店',
                '支店区分': np.random.choice(branch_types, p=[0.1, 0.7, 0.2]),
                '地域区分': np.random.choice(regions, p=[0.4, 0.4, 0.2]),
                '都道府県': random.choice(prefectures),
                '窓口数': random.randint(3, 10),
                '従業員数': random.randint(15, 50),
                '月間来店客数_目安': random.randint(1000, 5000)
            }
        branches.append(branch)
    
    return pd.DataFrame(branches)


def create_procedure_master():
    """手続きマスタデータを生成"""
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


def create_employee_master(branches_df):
    """従業員マスタデータを生成"""
    employees = []
    employee_id = 1
    
    # 役職の定義と分布
    positions = {
        '支店長': {'ratio': 0.03, 'exp_min': 20, 'exp_max': 35, 'skill': '上級'},
        '副支店長': {'ratio': 0.05, 'exp_min': 15, 'exp_max': 30, 'skill': '上級'},
        '課長': {'ratio': 0.10, 'exp_min': 12, 'exp_max': 25, 'skill': '上級'},
        '係長': {'ratio': 0.15, 'exp_min': 8, 'exp_max': 20, 'skill': '中級'},
        '主任': {'ratio': 0.22, 'exp_min': 5, 'exp_max': 15, 'skill': '中級'},
        '一般職員': {'ratio': 0.45, 'exp_min': 0, 'exp_max': 10, 'skill': '初級'}
    }
    
    # 雇用形態の分布
    employment_types = {
        '正社員': 0.75,
        'パート': 0.20,
        '派遣': 0.05
    }
    
    # 姓のリスト（日本でよくある姓）
    last_names = ['佐藤', '鈴木', '高橋', '田中', '渡辺', '伊藤', '山本', '中村', '小林', '加藤',
                  '吉田', '山田', '佐々木', '山口', '斎藤', '松本', '井上', '木村', '清水', '山崎',
                  '森', '阿部', '池田', '橋本', '石川', '山下', '中島', '前田', '藤田', '小川']
    
    # 名のリスト（男性）
    male_first_names = ['太郎', '一郎', '健', '誠', '隆', '剛', '大輔', '健太', '翔太', '拓也',
                       '和也', '直樹', '浩', '明', '正', '博', '秀樹', '雄大', '智也', '裕介']
    
    # 名のリスト（女性）
    female_first_names = ['花子', '美香', '愛', '由美', '恵子', '裕子', '真由美', '陽子', '直美', '智子',
                         '美穂', '香織', '理恵', '麻衣', '彩', '舞', '優子', '綾子', '未来', '沙織']
    
    for branch in branches_df.itertuples():
        branch_employee_count = branch.従業員数
        
        # 役職ごとの人数を計算
        position_counts = {}
        remaining = branch_employee_count
        
        for position, info in positions.items():
            if position == '一般職員':
                # 残りは全て一般職員
                position_counts[position] = remaining
            else:
                count = max(1, int(branch_employee_count * info['ratio']))
                position_counts[position] = min(count, remaining)
                remaining -= position_counts[position]
        
        # 各役職の従業員を生成
        for position, count in position_counts.items():
            for _ in range(count):
                # 性別をランダムに決定（男性60%、女性40%）
                is_male = random.random() < 0.6
                
                # 名前生成
                last_name = random.choice(last_names)
                if is_male:
                    first_name = random.choice(male_first_names)
                else:
                    first_name = random.choice(female_first_names)
                
                # 経験年数とスキルレベル
                exp_min = positions[position]['exp_min']
                exp_max = positions[position]['exp_max']
                experience_years = random.randint(exp_min, exp_max)
                
                # スキルレベルの決定（経験年数も考慮）
                if experience_years >= 15:
                    skill_level = '上級'
                elif experience_years >= 5:
                    skill_level = '中級'
                else:
                    skill_level = '初級'
                
                # 新人は必ず初級
                if position == '一般職員' and experience_years <= 2:
                    skill_level = '初級'
                
                # 雇用形態（役職によって調整）
                if position in ['支店長', '副支店長', '課長']:
                    employment_type = '正社員'
                else:
                    employment_type = np.random.choice(
                        list(employment_types.keys()),
                        p=list(employment_types.values())
                    )
                
                # 入社年月を経験年数から逆算
                hire_date = datetime.now() - timedelta(days=experience_years * 365 + random.randint(-180, 180))
                
                # 研修受講回数（経験年数と役職に応じて）
                if experience_years <= 1:
                    training_count = random.randint(3, 5)  # 新人は研修多め
                elif position in ['支店長', '副支店長', '課長']:
                    training_count = experience_years + random.randint(5, 10)  # 管理職は研修多め
                else:
                    training_count = int(experience_years * 0.8) + random.randint(0, 3)
                
                employee = {
                    '従業員ID': employee_id,
                    '従業員番号': f'EMP{str(employee_id).zfill(6)}',
                    '氏名': f'{last_name} {first_name}',
                    '所属支店ID': branch.支店ID,
                    '役職': position,
                    '経験年数': experience_years,
                    'スキルレベル': skill_level,
                    '雇用形態': employment_type,
                    '入社年月': hire_date.strftime('%Y-%m-%d'),
                    '研修受講回数': training_count
                }
                
                employees.append(employee)
                employee_id += 1
    
    return pd.DataFrame(employees)


def add_special_patterns_to_employees(employees_df, branches_df):
    """デモ用に特定のパターンを従業員データに追加"""
    # パターン1: 東京中央支店に新人を多く配置（処理時間が長い原因）
    tokyo_branch = branches_df[branches_df['支店名'] == '東京中央支店']
    if not tokyo_branch.empty:
        tokyo_branch_id = tokyo_branch.iloc[0]['支店ID']
        tokyo_employees = employees_df[employees_df['所属支店ID'] == tokyo_branch_id].index
        
        # 東京中央支店の30%を新人（経験年数0-2年）に変更
        sample_size = int(len(tokyo_employees) * 0.3)
        new_employees = np.random.choice(tokyo_employees, sample_size, replace=False)
        
        for idx in new_employees:
            employees_df.loc[idx, '経験年数'] = random.randint(0, 2)
            employees_df.loc[idx, 'スキルレベル'] = '初級'
            employees_df.loc[idx, '研修受講回数'] = random.randint(1, 3)
            # 入社年月も調整
            hire_date = datetime.now() - timedelta(days=employees_df.loc[idx, '経験年数'] * 365)
            employees_df.loc[idx, '入社年月'] = hire_date.strftime('%Y-%m-%d')
    
    # パターン2: 大阪梅田支店にベテランを多く配置（処理時間が短い原因）
    osaka_branch = branches_df[branches_df['支店名'] == '大阪梅田支店']
    if not osaka_branch.empty:
        osaka_branch_id = osaka_branch.iloc[0]['支店ID']
        osaka_employees = employees_df[employees_df['所属支店ID'] == osaka_branch_id].index
        
        # 大阪梅田支店の50%をベテラン（経験年数10年以上）に変更
        sample_size = int(len(osaka_employees) * 0.5)
        veteran_employees = np.random.choice(osaka_employees, sample_size, replace=False)
        
        for idx in veteran_employees:
            employees_df.loc[idx, '経験年数'] = random.randint(10, 25)
            employees_df.loc[idx, 'スキルレベル'] = '上級'
            employees_df.loc[idx, '研修受講回数'] = employees_df.loc[idx, '経験年数'] + random.randint(5, 10)
            # 入社年月も調整
            hire_date = datetime.now() - timedelta(days=employees_df.loc[idx, '経験年数'] * 365)
            employees_df.loc[idx, '入社年月'] = hire_date.strftime('%Y-%m-%d')
        
        # パターン3: 特定の優秀な従業員を作成（デモで個人レベルのドリルダウン時に使用）
        star_employees = employees_df[
            (employees_df['所属支店ID'] == osaka_branch_id) & 
            (employees_df['役職'] == '主任')
        ]
        if not star_employees.empty:
            star_employee_idx = star_employees.index[0]
            employees_df.loc[star_employee_idx, '氏名'] = '山田 優子'
            employees_df.loc[star_employee_idx, '経験年数'] = 12
            employees_df.loc[star_employee_idx, 'スキルレベル'] = '上級'
            employees_df.loc[star_employee_idx, '研修受講回数'] = 25
    
    return employees_df


def create_transaction_data(start_date, end_date, branches_df, procedures_df, employees_df):
    """トランザクションデータを生成"""
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
            
            # その支店の従業員を取得
            branch_employees = employees_df[employees_df['所属支店ID'] == branch.支店ID]
            if branch_employees.empty:
                continue
            
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
                employee = branch_employees.sample().iloc[0]
                error_rate = 0.02 if employee['スキルレベル'] == '上級' else \
                            0.05 if employee['スキルレベル'] == '中級' else 0.10
                
                transaction = {
                    '処理ID': len(transactions) + 1,
                    '支店ID': branch.支店ID,
                    '支店名': branch.支店名,  # 支店名を追加
                    '従業員ID': employee['従業員ID'],
                    '手続きID': procedure['手続きID'],
                    '手続き名称': procedure['手続き名称'],  # 手続き名称を追加
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


def add_demo_patterns(df):
    """デモ用のパターンをトランザクションデータに追加"""
    # パターン1: 特定支店の午後の処理時間が長い
    tokyo_rows = df[df['支店名'] == '東京中央支店'].index
    for idx in tokyo_rows:
        time_str = df.loc[idx, '受付時刻']
        hour = int(time_str.split(':')[0])
        if hour >= 13:  # 午後
            df.loc[idx, '処理時間_分'] = int(df.loc[idx, '処理時間_分'] * 1.5)
    
    # パターン2: 埼玉新都心支店のエラー率が高い
    saitama_rows = df[df['支店名'] == '埼玉新都心支店'].index
    if len(saitama_rows) > 0:
        # エラー率を15%に設定
        error_count = int(len(saitama_rows) * 0.15)
        error_indices = np.random.choice(saitama_rows, error_count, replace=False)
        df.loc[saitama_rows, 'エラー有無'] = 0  # 一旦全部0に
        df.loc[error_indices, 'エラー有無'] = 1  # 選択したものを1に
    
    # パターン3: 大阪梅田支店の改善効果（直近3ヶ月で徐々に改善）
    osaka_rows = df[df['支店名'] == '大阪梅田支店'].index
    if len(osaka_rows) > 0:
        recent_date = df['処理日付'].max() - timedelta(days=90)
        recent_osaka = df.loc[osaka_rows][df.loc[osaka_rows, '処理日付'] >= recent_date].index
        
        for idx in recent_osaka:
            days_ago = (df['処理日付'].max() - df.loc[idx, '処理日付']).days
            improvement_factor = 1 - (90 - days_ago) / 90 * 0.3
            df.loc[idx, '処理時間_分'] = int(df.loc[idx, '処理時間_分'] * improvement_factor)
    
    return df


def export_demo_data():
    """デモデータを生成してエクスポート"""
    print("マスタデータ生成中...")
    branches = create_branch_master()
    procedures = create_procedure_master()
    employees = create_employee_master(branches)
    
    # デモ用パターンを従業員に追加
    # employees = add_special_patterns_to_employees(employees, branches)
    
    print("トランザクションデータ生成中...")
    # トランザクションデータ生成（1年分）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    transactions = create_transaction_data(start_date, end_date, 
                                         branches, procedures, employees)
    
    # デモパターン追加
    print("デモパターン追加中...")
    transactions = add_demo_patterns(transactions)
    
    # Excel出力を試みる
    try:
        print("Excelファイルとして出力中...")
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
        
        print("✅ Excelファイル '銀行業務デモデータ.xlsx' を生成しました。")
        
    except ImportError:
        print("xlsxwriterがインストールされていないため、CSVファイルとして出力します...")
        
        # CSVファイルとして出力
        branches.to_csv('支店マスタ.csv', index=False, encoding='utf-8-sig')
        procedures.to_csv('手続きマスタ.csv', index=False, encoding='utf-8-sig')
        employees.to_csv('従業員マスタ.csv', index=False, encoding='utf-8-sig')
        transactions.to_csv('処理履歴.csv', index=False, encoding='utf-8-sig')
        
        # サマリも作成
        summary = transactions.groupby(['支店名', '手続き名称']).agg({
            '処理時間_分': ['mean', 'count'],
            'エラー有無': 'sum',
            '顧客満足度': 'mean'
        }).round(2)
        summary.to_csv('サマリ.csv', encoding='utf-8-sig')
        
        print("✅ 以下のCSVファイルを生成しました：")
        print("   - 支店マスタ.csv")
        print("   - 手続きマスタ.csv")
        print("   - 従業員マスタ.csv")
        print("   - 処理履歴.csv")
        print("   - サマリ.csv")
        
        print("\n💡 ヒント: Excelファイルとして出力したい場合は以下を実行してください：")
        print("   pip install xlsxwriter")
    
    # データ統計を表示
    print("\n📊 生成データ統計:")
    print(f"   - 支店数: {len(branches)}")
    print(f"   - 従業員数: {len(employees)}")
    print(f"   - 手続き種類: {len(procedures)}")
    print(f"   - 処理履歴数: {len(transactions):,}")
    print(f"   - データ期間: {start_date.strftime('%Y/%m/%d')} ～ {end_date.strftime('%Y/%m/%d')}")


if __name__ == "__main__":
    export_demo_data()
    print("\n✨ デモデータの生成が完了しました！")