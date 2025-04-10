import pandas as pd
import numpy as np

data = pd.read_csv("LCOM_results/TypeMetrics.csv")

data  = data.sort_values(by = "LCOM1",ascending=False)

print(data.head(10))

