import joblib

rules = joblib.load("models/association_rules.pkl")

def recommend(product):

    product = product.strip().title()

    recommendations = []

    for _, row in rules.iterrows():

        antecedents = [str(x).title() for x in row["antecedents"]]
        consequents = [str(x).title() for x in row["consequents"]]

        if product in antecedents:
            recommendations.extend(consequents)

    return list(set(recommendations))


if __name__ == "__main__":

    product = input("Enter Product: ")

    result = recommend(product)

    print("\nRecommended Products:")
    print(result)