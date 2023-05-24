# データベース接続に必要なライブラリをインポート
import pymysql
import time
import random
from datetime import datetime

# AWS RDSの設定情報
# <Your RDS Host>, <Your RDS User name>, <Your RDS Password>, <Your RDS Database name>は自分の環境に合わせて適切に書き換えてください
HOST = "Your RDS Host"
USER = "Your RDS User name"
PASSWORD = "Your RDS Password"
DATABASE = "Your RDS Database name"

# PyMySQLを用いてAWS RDSに接続
connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PASSWORD,
                             database=DATABASE)

try:
    with connection.cursor() as cursor:  # cursorを使ってSQL文を実行
        # 新規テーブル（sensor_data）を作成。テーブルにはtimeとsensor_valueの2つの列がある
        cursor.execute("""
        CREATE TABLE sensor_data (
            time TIMESTAMP NOT NULL,  # time: センサデータの取得時間
            sensor_value FLOAT NOT NULL  # sensor_value: センサの測定値
        );
        """)
        # テーブル作成の変更をデータベースに反映
        connection.commit()

        # センサデータの生成(架空データ)とデータベースへの挿入を開始
        start_time = time.time()  # データ生成開始時間
        while True:  # 無限ループ
            current_time = time.time()  # 現在時間
            elapsed_time = int(current_time - start_time)  # データ生成開始からの経過時間

            # 10秒ごとに異常値（1000.0）を生成、それ以外は0.0から100.0の間でランダムな正常値を生成
            if elapsed_time % 10 == 0:
                sensor_value = 1000.0  # 異常値
            else:
                sensor_value = random.uniform(0.0, 100.0)  # 正常値

            # 生成したセンサデータをデータベースに挿入
            cursor.execute("""
            INSERT INTO sensor_data (time, sensor_value) 
            VALUES (%s, %s);
            """, (datetime.now(), sensor_value))  # datetime.now()は現在の日時を取得
            
            # データ挿入の変更をデータベースに反映
            connection.commit()

            # 次のデータ生成まで1秒待機
            time.sleep(1)

finally:
    connection.close()  # データベース接続を終了