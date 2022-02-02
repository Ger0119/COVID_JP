#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/02/01 16:20
# @Author  : Ketsu Kin
# @File    : manage.py
from Downloader import download
from datetime import datetime
from Graph import mk_linegraph, mk_donut, mk_map
import pandas as pd


def main():
    m = Manager()
    while True:
        m.check_cmd()
        print("Command>>", end="")
        m.get_cmd(str(input()))


class Manager(object):
    start = "2021/2/1"
    end = None
    target = "2022/2/1"
    cmd = ""
    DataFrame1 = ""
    DataFrame2 = ""
    file1 = "Data/nhk_news_covid19_domestic_daily_data.csv"
    file2 = "Data/nhk_news_covid19_prefectures_daily_data.csv"
    flag_load = 0

    def check_cmd(self):
        if not self.cmd:
            self.check_time()
        elif self.cmd == "exit":
            exit()
        elif self.cmd == "update":
            self.ask_date()
        elif self.cmd == "range":
            self.get_range()
        elif self.cmd == "target":
            self.get_target()
        elif self.cmd == "help":
            self.help()
        elif self.cmd == "load":
            self.load()
            self.flag_load = 1
        elif self.cmd == "info":
            print(f"start  : {self.start}")
            print(f"end    : {self.end}")
            print(f"target : {self.target}")
        elif "line" in self.cmd:
            if not self.flag_load:
                print("Dataをロードしてください。")
            else:
                self.linegraph()
        elif "map" in self.cmd:
            if not self.flag_load:
                print("Dataをロードしてください。")
            else:
                self.map()
        elif "donut" in self.cmd:
            if not self.flag_load:
                print("Dataをロードしてください。")
            else:
                self.donut()

    def get_cmd(self, cmd):
        self.cmd = cmd

    def load(self):
        self.DataFrame1 = pd.read_csv(self.file1, index_col=0)
        self.DataFrame2 = pd.read_csv(self.file2, index_col=0)

    def linegraph(self):
        mk_linegraph(self.DataFrame1, self.start, self.end)

    def map(self):
        data = self.DataFrame2.groupby("都道府県名").apply(lambda x: x.loc[self.target, :])
        mk_map(self.target, data.iloc[:, 2:])

    def donut(self):
        data = self.DataFrame2.groupby("都道府県名").apply(lambda x: x.loc[self.target, :])
        mk_donut(self.target, data.iloc[:, 2:])

    @staticmethod
    def check_time():
        with open("Data/download_time.log") as f:
            temp = f.readlines()
        print(f"前回データDownload時間: {temp[0]}")

    def ask_date(self):
        print("データを更新しますか? : ", end="")
        request = str(input())
        print()
        if request in ["N", "n", "No", "NO", "no"]:
            print("更新操作止めました。")
        else:
            self.update()
            print("データ更新完了しました。")

    @staticmethod
    def update():
        download()

    def get_range(self):
        print(f"Start　日付を入力してください。Default['{self.start}'] : ", end="")
        start = self.get_date()
        self.start = start if start else self.start
        print()

        print(f"End　  日付を入力してください。Default['{self.end}'] : ", end="")
        end = self.get_date()
        self.end = end if end else self.end
        print()

    def get_target(self):
        print(f"Target 日付を入力してください。Default['{self.target}'] : ", end="")
        target = self.get_date()
        self.target = target if target else self.target

    def get_date(self):
        while True:
            temp = str(input())
            if temp == "exit":
                print("更新操作止めました。")
                break
            elif temp == "":
                break
            if self.check_date(temp):
                break
            print("Value Error! 再入力してください。 : ", end="")
        return temp

    @staticmethod
    def check_date(date):
        try:
            d = datetime.strptime(date, "%Y/%m/%d")
        except ValueError:
            return False
        return datetime.now() > d > datetime(2019, 11, 1)

    @staticmethod
    def help():
        print("""Command>>   [info]   設定値を確認
            [load]   データをロード
            [range]  日付範囲を設定
            [target] 日付を設定
            [line]   line graph  を作成
            [map]    map graph   を作成
            [donut]  donut graph を作成
            [exit]   退出
            [help]   Help""")


if __name__ == '__main__':
    main()
