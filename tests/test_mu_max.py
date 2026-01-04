import numpy as np
import pandas as pd
import wellflow as wf
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("long_example.xlsx")
threshold = wf.estimate_early_od_threshold(df=df, od_col="od_smooth")
max_tabls = wf.create_mu_max_table(df=df, threshold=threshold)
print(max_tabls)
max_tables2 = wf.create_mu_max_table2(df=df, threshold=threshold)
print(max_tables2)

#
# sns.lineplot(data=df,x="time_hours",y="mu",hue="well")
# plt.xlabel("time")
# plt.show()
