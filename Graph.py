#!/usr/bin/env python
# -*- coding: utf-8 -*-b
# @Time    : 2022/01/27 17:50
# @Author  : Ketsu Kin
# @File    : Graph.py
import numpy as np
from japanmap import picture
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams['font.family'] = 'MS Gothic'


def mk_linegraph(df, start="2021/1/1", end=None, ):
    # file = "Data/nhk_news_covid19_domestic_daily_data.csv"
    # df = pd.read_csv(file, index_col=0)
    # df.index = pd.to_datetime(df.index, format='%Y/%m/%d')

    fig, ax = plt.subplots(2, 2, figsize=(18, 16))

    df.loc[start:end, :].plot.bar(subplots=True, ax=ax)

    for i in range(2):
        for j in range(2):
            ax[i, j].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            ax[i, j].xaxis.set_minor_locator(mdates.MonthLocator(interval=1))

    fig.autofmt_xdate()
    plt.show()


def mk_jpmap(ax, data):
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    divider = make_axes_locatable(ax)

    ax_cb = divider.append_axes("right", size="7%", pad="2%")

    fig = ax.get_figure()
    fig.add_axes(ax_cb)

    cmap = plt.cm.Reds
    norm = plt.Normalize(vmin=data.min(), vmax=data.max())
    colFunc = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()

    Z = picture(data.apply(colFunc))
    plt.colorbar(plt.cm.ScalarMappable(norm, cmap), cax=ax_cb, ax=ax)

    ax.imshow(Z, cmap=cmap)


def mk_map(date, data):
    # file = "Data/nhk_news_covid19_prefectures_daily_data.csv"
    # df = pd.read_csv(file, index_col=0)
    # d = df.groupby("都道府県名").apply(lambda x: x.iloc[-1, :])
    # data = d.iloc[:, 2:]

    fig = plt.figure(figsize=(18, 16))

    ax = fig.add_subplot(2, 2, 1)
    mk_jpmap(ax, data.iloc[:, 0])
    ax.set_title(f"{date} {data.columns[0]}")

    ax = fig.add_subplot(2, 2, 2)
    mk_jpmap(ax, data.iloc[:, 1])
    ax.set_title(f"{date} {data.columns[1]}")

    ax = fig.add_subplot(2, 2, 3)
    mk_jpmap(ax, data.iloc[:, 2])
    ax.set_title(f"{date} {data.columns[2]}")

    ax = fig.add_subplot(2, 2, 4)
    mk_jpmap(ax, data.iloc[:, 3])
    ax.set_title(f"{date} {data.columns[3]}")
    plt.show()


def func(pct, allvals):
    absolute = int(np.round(pct / 100. * np.sum(allvals)))
    if pct < 2:
        return ""
    return "{:.1f}%\n({:d} 人)".format(pct, absolute)


def mk_pie(data, ax):
    size = 0.5
    data = data.loc[data != 0]
    data = data.sort_values()

    ax.pie(data, radius=1.1, startangle=90,
           autopct=lambda pct: func(pct, data),
           pctdistance=0.8, labels=data.index,
           wedgeprops=dict(width=size, edgecolor='w'))


def mk_donut(date, data):
    fig, ax = plt.subplots(2, 2, figsize=(18, 16))

    mk_pie(data.iloc[:, 0], ax[0, 0])
    ax[0, 0].set_title(f"{date} {data.columns[0]}\n")

    mk_pie(data.iloc[:, 1], ax[0, 1])
    ax[0, 1].set_title(f"{date} {data.columns[1]}\n")

    mk_pie(data.iloc[:, 2], ax[1, 0])
    ax[1, 0].set_title(f"{date} {data.columns[2]}\n")

    mk_pie(data.iloc[:, 3], ax[1, 1])
    ax[1, 1].set_title(f"{date} {data.columns[3]}\n")

    plt.show()
