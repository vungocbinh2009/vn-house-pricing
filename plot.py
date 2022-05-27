import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = pd.read_csv("full_data.csv")
# num_floors = data["num_floors"]
# sns.histplot(num_floors[num_floors <= 10])
# plt.savefig("fig1.png")

price = data["price"]
sns.histplot(price)
plt.savefig("fig2.png")