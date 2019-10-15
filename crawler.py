import time
import threading
import requests
from bs4 import BeautifulSoup
import os


def get_main_urls(headers):
    urls = []
    for i in range(233):
        res = requests.get('https://www.mzitu.com/' + '/page/' + str(i+1), headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        list = soup.find(class_='postlist').find_all('li')
        for item in list:
            url = item.find('a').get('href')
            with open('r.txt', 'a') as f:
                f.write(url + ',')
    return urls


def get_pics_urls(url, headers):
    global pic_urls
    res2 = requests.get(url, headers=headers)
    soup2 = BeautifulSoup(res2.text, 'lxml')
    total = soup2.find(class_='pagenavi').find_all('a')[-2].find('span').string
    title = soup2.find(class_='main-title').string
    index = 1
    file_folder = title
    folder = 'D:/pictures/images/' + file_folder + '/'
    if os.path.exists(folder) == False:
        os.makedirs(folder)
    for i in range(int(total)):
        res3 = requests.get(url + '/' + str(i+1), headers=headers)
        soup3 = BeautifulSoup(res3.text, 'lxml')
        pic_url = soup3.find('img').get('src')
        print('downloading......' + title + 'NO.' + str(index))
        filename = folder + str(index) + '.jpg'
        with open(filename, 'wb') as f:
            img = requests.get(pic_url, headers=headers).content
            f.write(img)
        index += 1
    print('当前图集下载完成')


if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) App'
                             'leWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.'
                             '3865.120 Safari/537.36',
               'Referer': 'https://www.mzitu.com/'
               }
    pic_urls = []
    i = 1
    print("程序于 {} 开始启动，请等待...".format(time.ctime()))
    # urls = get_main_urls(headers)
    #get_main_urls(headers)
    with open('r.txt', 'r') as f:
        urls = f.read().split(',')
    for url in urls:
        print('正在下载第' + str(i) + '个图集，共5574个图集')
        #get_pics_urls(url, headers)
        i += 1




