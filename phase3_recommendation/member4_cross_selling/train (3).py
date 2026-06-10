import joblib
from mlxtend.frequent_patterns import apriori, association_rules
from preprocess import prepare_transactions

data = prepare_transactions("data/transactions.csv")

frequent_itemsets = apriori(
    data,
    min_support=0.2,
    use_colnames=True
)

rules = association_rules(
    frequent_itemsets,
    metric="lift",
    min_threshold=1
)

print("\nAssociation Rules:\n")
print(rules)

joblib.dump(
    rules,
    "models/association_rules.pkl"
)

print("\nModel Saved Successfully!")