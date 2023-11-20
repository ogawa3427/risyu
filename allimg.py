import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os

directory = 'ind_csvs'
os.makedirs(directory, exist_ok=True)

# 科目のリストを読み込む
with open('kamoku_dict.csv', 'r', encoding='utf-8') as f:
    kamoku = [line.strip() for line in f.readlines()]

# 2023q4data.csv ファイルを開き、各行をチェックする
with open('2023q4data.csv', 'r', encoding='utf-8') as f:
    data_lines = f.readlines()

    # 各科目についてループ
    for item in kamoku:
        # 該当する行を含むファイルを作成
        print(item)
        file_path = os.path.join(directory, f'{item}.csv')
        with open(file_path, 'w', encoding='utf-8') as out_file:
            # データファイルの各行をチェック
            for line in data_lines:
                if item in line:
                    # 該当する行を書き込み
                    out_file.write(line)

for item in kamoku:
    file_path = os.path.join(directory, f'{item}.csv')

    # CSVファイルを読み込み、列名を設定
    data = pd.read_csv(file_path)
    data.columns = ['Timestamp', 'Schedule Number', 'Appropriate Number', 'Total Registrations', 'Priority', '1st Preference', '2nd Preference', '3rd Preference', '4th Preference', '5th Preference']

    # タイムスタンプを日時形式に変換
    data['Timestamp'] = pd.to_datetime(data['Timestamp'].astype(str), format='%Y%m%d%H%M%S')

    # Timestamp 列と数値データのみを含む列に限定
    numeric_columns = ['Timestamp', 'Appropriate Number', 'Total Registrations', 'Priority', '1st Preference', '2nd Preference', '3rd Preference', '4th Preference', '5th Preference']
    data_numeric = data[numeric_columns]

    # 30分間隔でデータを再サンプリングし、平均を計算
    resampled_data_all = data_numeric.resample('30T', on='Timestamp').mean()

    # 優先指定から第5希望までの数を累積
    preferences_all = resampled_data_all[['Priority', '1st Preference', '2nd Preference', '3rd Preference', '4th Preference', '5th Preference']].cumsum(axis=1)

    # 色の強さと線の太さを設定
    color_strengths = np.linspace(0.8, 0.1, num=len(preferences_all.columns))
    line_widths = np.linspace(3, 1, num=len(preferences_all.columns))

    # 適正人数の自然数倍でy軸の目盛りを設定し、太くする
    appropriate_number = data['Appropriate Number'].iloc[0]
    max_y_value = preferences_all.max().max()
    y_ticks = np.arange(0, max_y_value + appropriate_number, appropriate_number)

    colors = ['red', 'purple', 'green', 'blue', 'orange', 'cyan']
    
    # グラフをプロット
    plt.figure(figsize=(14, 8))
    for i, column in enumerate(preferences_all.columns):
        plt.plot(preferences_all.index, preferences_all[column], label=column, 
                 color=colors[i % len(colors)], linewidth=3)

    # 各日の正午に縦軸を追加
    start_date = data['Timestamp'].min().normalize()
    end_date = data['Timestamp'].max().normalize()
    noon_times = pd.date_range(start=start_date, end=end_date, freq='D') + pd.DateOffset(hours=12)
    for noon in noon_times:
        plt.axvline(noon, color='gray', linestyle='--', linewidth=0.7)

    # y軸の目盛りを設定
    plt.yticks(y_ticks, fontsize=10, weight='bold')

    # その他のグラフ設定（軸ラベル、タイトル、グリッドなど）
    plt.xlabel('Time')
    plt.ylabel('Number of People')
    plt.title(f'Cumulative Preferences Over Time - {item}')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    # X軸の日付フォーマットを設定
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_minor_locator(mdates.HourLocator(interval=6))

    plt.tight_layout()

    # グラフを保存
    plot_file_path = f'/home/ogawa27/risyu/static/imgs/{item}.png'
    plt.savefig(plot_file_path)

    # グラフの表示は省略（すべてのグラフを表示するのは効率的でないため）
    plt.close()

    print(item)
