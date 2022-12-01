# Demo with UUID

import uuid
from time import time_ns

import pandas as pd
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='****************', database='benchmark')
cursor = conn.cursor()

x = []
y = []

for i in range(100000):
    start = time_ns()
    cursor.execute(f"INSERT INTO uuid4(id) VALUES('{uuid.uuid4()}');")
    conn.commit()
    end = time_ns()

    x.append(i)
    y.append((end - start))

    if i % 1000 == 0:
        print(i)

df = pd.DataFrame(x, columns=['id'])
df['insert_ns'] = y

df.to_csv('./csv/uuid4.csv', index=False)
