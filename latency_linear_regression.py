# Demo with UUID

import pandas as pd
from sklearn.linear_model import LinearRegression


def DOLR(df: pd.DataFrame, title: str):
    X = df['id'].values.reshape(-1, 1)
    Y = df['insert_ns'].values.reshape(-1, 1)

    lr = LinearRegression()
    lr.fit(X, Y)

    print(title)
    print("coef_:", lr.coef_[0][0])
    print("intercept_", lr.intercept_[0])
    print(lr.score(X, Y))
    print()

    import matplotlib.pyplot as plt

    plt.plot(X, Y, '-', label='Transaction Latency')
    plt.plot(X, lr.predict(X), label='Linear Regression')
    plt.title(title)
    plt.xlabel('Cumulative Query Count')
    plt.ylabel('Transaction (ns)')
    plt.legend()
    plt.ylim(2000000, 4000000)
    plt.savefig(f"./plot/{title}.png", dpi=300)
    plt.show()


df = pd.read_csv('./csv/uuid4.csv')
DOLR(df, "UUID4")
