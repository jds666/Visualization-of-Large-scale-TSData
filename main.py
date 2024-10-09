import re

#可视化文件夹D:\Pyprogram\Python_Data_Analysis\data_csv\temperature中所有csv文件数据
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# 读取Temperature_point_no_0a1ee4feff8d79e0-S.csv
filepath = r'D:\Pyprogram\Python_Data_Analysis\data_csv\temperature'


# 所有csv文件的时间戳起止时间
def get_time(filepath):
    all_csv_time = []
    for file in os.listdir(filepath):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(filepath, file))
            # df第一行 的“timestamp”
            time = df.iloc[0, 0]
            # df最后一行 的“timestamp”
            time_end = df.iloc[-1, 0]

            all_csv_time.append([file[21:-4],time, time_end])
    return all_csv_time

TIME_start_end = get_time(filepath)


import plotly.graph_objects as go
import numpy as np
from scipy.stats import gaussian_kde
from datetime import datetime

# 创建数据点，保留为 datetime 对象用于显示，转换为时间戳用于计算密集度
x_data = [datetime.strptime(time[1], '%Y-%m-%d %H:%M:%S') for time in TIME_start_end]
y_data = [datetime.strptime(time[2], '%Y-%m-%d %H:%M:%S') for time in TIME_start_end]

# 将 datetime 转换为时间戳用于密度计算
x_timestamps = [x.timestamp() for x in x_data]
y_timestamps = [y.timestamp() for y in y_data]

# 计算每个点的密集度（使用高斯核密度估计）
xy = np.vstack([x_timestamps, y_timestamps])
density = gaussian_kde(xy)(xy)

# 创建散点图，使用原始的 datetime 对象作为坐标，密集度作为颜色映射
fig = go.Figure(data=go.Scatter(
    x=x_data,  # 使用 datetime 对象显示
    y=y_data,  # 使用 datetime 对象显示
    mode='markers',
    marker=dict(
        size=8,
        color=density,  # 颜色映射为密集度
        colorscale='magenta',  # 洋红色
        showscale=True  # 显示颜色条
    )
))

# 更新布局
fig.update_layout(
    title='494个时间序列的时间戳范围',
    xaxis_title='开始时间',
    yaxis_title='结束时间',
    xaxis=dict(
        type='date',  # 确保 x 轴显示为日期格式
    ),
    yaxis=dict(
        type='date',  # 确保 y 轴显示为日期格式
    )
)

# 显示图表
fig.show()