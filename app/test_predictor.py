import pandas as pd
from predictor import predict_dropout

df = pd.read_csv("data/example_input.csv")

results = predict_dropout(df)
print(results.head())
