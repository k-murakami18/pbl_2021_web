from bs4 import BeautifulSoup
import requests
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

import base64
from io import BytesIO


def scraping(arg: str):
    dict_user = {'title': [], 'rating': []}
    user_id = arg

    user_path = 'https://filmarks.com/users/' + user_id + '/marks?view=poster'

    rs = requests.get(user_path)
    soup = BeautifulSoup(rs.content, 'lxml')

    # Mark数を取得
    mark_count = soup.find('span', class_='p-users-navi__count').text

    if int(mark_count) > 0:
        # 1ページに36作品表示できる＋1ページ分
        page_num = int(mark_count)//36+1

        for page in range(1, page_num + 1):
            rs = requests.get(user_path, params={'page': page})
            soup = BeautifulSoup(rs.content, 'lxml')

            # タイトル
            titles = soup.select('.c-content-item__title > a')
            # 評価
            ratings = soup.select(
                '.c-content-item-infobar__item.c-content-item-infobar__item--star.is-active > a > span')

            for title, rating in zip(titles, ratings):
                dict_user['title'].append(title.get_text())
                dict_user['rating'].append(rating.get_text())

        df_user = pd.DataFrame(dict_user)
        df_user['rating'] = df_user['rating'].str.replace('-', '0')
        df_user['rating'] = df_user['rating'].astype('float64')

    fig = plt.figure(figsize=None, facecolor='white')
    plt.rcParams['font.family'] = "MS Gothic"
    ax = fig.add_subplot(111)

    data = df_user['rating']
    ax.hist(data, bins=10, rwidth=0.9)

    ax.set_title('自分の視聴映画の評価の分布')
    ax.set_xlabel('評価')
    ax.set_ylabel('度数')
    ax.set_xticks([x-0.5 for x in range(1, 6)], minor=True)
    ax.set_xticks(range(0,6), minor=False)
    ax.set_xticklabels([x-0.5 for x in range(1, 6)], color='gray', minor=True)
    ax.set_xticklabels(range(0,6), fontsize=12, minor=False)

    ax.grid()

    io = BytesIO()
    fig.savefig(io, format="png")
    # base64 形式に変換する。
    io.seek(0)
    img = base64.b64encode(io.read()).decode()

    return img
