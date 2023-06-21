import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
import scipy.cluster.hierarchy as sch

data = pd.read_csv('Wholesale customers data.csv')
data.head()
data_scaled = normalize(data)
data_scaled = pd.DataFrame(data_scaled, columns=data.columns)
data_scaled.head()
plt.figure(figsize=(10,7))
plt.title("Dendrograms")
dend = sch.dendrogram(sch.linkage(data_scaled, method='ward'))
