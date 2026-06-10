import pandas as pd
from mlxtend.preprocessing import TransactionEncoder

def prepare_transactions(path):

    df = pd.read_csv(path)

    transactions = []

    for row in df["Products"]:
        transactions.append(row.split(","))

    te = TransactionEncoder()

    te_array = te.fit(transactions).transform(transactions)

    encoded_df = pd.DataFrame(
        te_array,
        columns=te.columns_
    )

    return encoded_df