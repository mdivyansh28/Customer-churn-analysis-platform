from prediction import ChurnPrediction

trainer = ChurnPrediction(
    "data/Customer Churn.csv"
)

results = trainer.train_models()

print("\nMODEL COMPARISON\n")

for model, metrics in results.items():

    print("\n", model)

    for metric, value in metrics.items():

        print(metric, ":", value)