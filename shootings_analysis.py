import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('data/shootings.csv', low_memory=False)
data = df.name.apply(lambda x: x.split(' ')[0]).value_counts()
sns.barplot(x=data.head(10).index,
            y=data.head(10).values)
plt.tick_params(labelrotation=90)
plt.subplots_adjust(left=0.1,
                    right=0.9,
                    top=0.95,
                    bottom=0.2)
plt.show()
