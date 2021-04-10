import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame


class StockGraph:

    @classmethod
    def df_to_png(cls, df: DataFrame, filename):
        print(df['close'])
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['close'], color="red", label="close")
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=True,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=True)  # labels along the bottom edge are off
        plt.ticklabel_format(style='plain', axis='y')  # 숫자가 전부 안보이는 문제 해결
        print(filename)
        plt.savefig(filename)
        plt.show()


# 필요한 모듈import 하기
import plotly
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# fig = px.line(df, x='date', y='close', title='{}의 종가(close) Time Series'.format(company))
#
# fig.update_xaxes(
#     rangeslider_visible=True,
#     rangeselector=dict(
#         buttons=list([
#             dict(count=1, label="1m", step="month", stepmode="backward"),
#             dict(count=3, label="3m", step="month", stepmode="backward"),
#             dict(count=6, label="6m", step="month", stepmode="backward"),
#             dict(step="all")
#         ])
#     )
# )
# fig.show()