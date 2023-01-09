import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# set seed
np.random.seed(123)

# example time series data of large positive values, dim is (10 by 5)
df = pd.DataFrame(np.abs(np.random.randn(10, 5)) * 1000, columns=list("ABCDE"))
df.set_index(pd.date_range("1/1/2000", periods=10), inplace=True)
df

# example time series data of positive percentage rates, dim is (10 by 5)
df2 = pd.DataFrame(np.abs(np.random.randn(10, 5)) * 0.1, columns=list("ABCDE"))
df2.set_index(pd.date_range("1/1/2000", periods=10), inplace=True)
df2

# plot df's A,B,C,D,E columns as time series line charts
df.plot()
plt.show()

# plot df's A,B,C columns as time series line charts
df[["A", "B", "C"]].plot()
plt.show()

# time series line chart
############################
# plot df's A,B,C columns as time series line charts, via matplotlib
# horizontal axis tickers less dense
# vertical axis tickers less dense
# grid lines
# title
plt.plot(df.index, df["A"], label="A")
plt.plot(df.index, df["B"], label="B")
plt.plot(df.index, df["C"], label="C")
plt.legend()
plt.xticks(df.index[::2])
plt.yticks(np.arange(0, 3000, 500))
plt.grid()
plt.title("Time Series Plot")
plt.show()

# time series stacked line chart
####################################
# legend text show A, A+B, A+B+C
plt.plot(df.index, df["A"], label="A")
plt.plot(df.index, df["B"] + df["A"], label="B")
plt.plot(df.index, df["C"] + df["B"] + df["A"], label="C")
text = ["A", "A+B", "A+B+C"]
plt.legend(text)
plt.xticks(df.index[::2])
plt.yticks(np.arange(0, 3000, 500))
plt.grid()
plt.title("Time Series Stacked Plot")
plt.show()


# time series stacked bar chart
####################################
# plot df's A,B,C columns as time series stacked bar charts, via matplotlib
# horizontal axis tickers less dense
plt.bar(df.index, df["A"], label="A", color="red")
plt.bar(df.index, df["B"], label="B", color="green", bottom=df["A"])
plt.bar(df.index, df["C"], label="C", color="blue", bottom=df["B"] + df["A"])
plt.legend()
plt.xticks(df.index[::2])
plt.show()


# time series stacked bar with line in secondary axis chart
###########################################################
# plot df's A,B,C columns as time series bar charts, via matplotlib
# add df2's A,B,C columns as time series line charts, in secondary y-axis
plt.bar(df.index, df["A"], label="A", color="red")
plt.bar(df.index, df["B"], label="B", color="green", bottom=df["A"])
plt.bar(df.index, df["C"], label="C", color="blue", bottom=df["B"] + df["A"])
# secondary y-axis
plt.twinx()
plt.plot(df2.index, df2["A"], label="A", color="red", linestyle="--")
plt.plot(df2.index, df2["B"], label="B", color="green", linestyle="--")
plt.plot(df2.index, df2["C"], label="C", color="blue", linestyle="--")
plt.xticks(df.index[::2])
plt.show()

# time series bar with line in secondary axis chart
###########################################################
# plot df's A columns as time series bar charts, via matplotlib
# add df2's A columns as time series line charts, in secondary y-axis
plt.bar(df.index, df["A"], label="A", color="red")
# secondary y-axis
plt.twinx()
plt.plot(df2.index, df2["A"], label="A", color="black", linestyle="--")
plt.xticks(df.index[::2])
plt.show()

# time series line chart with two subplots
############################################
# up and down figures in same chart
# up is df's A,B,C columns as time series line charts
# down is df2's A,B,C columns as time series line charts
fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(df.index, df["A"], label="A", color="red")
ax[0].plot(df.index, df["B"], label="B", color="green")
ax[0].plot(df.index, df["C"], label="C", color="blue")
ax[1].plot(df2.index, df2["A"], label="A", color="red", linestyle="--")
ax[1].plot(df2.index, df2["B"], label="B", color="green", linestyle="--")
ax[1].plot(df2.index, df2["C"], label="C", color="blue", linestyle="--")
plt.xticks(df.index[::2])
plt.show()
