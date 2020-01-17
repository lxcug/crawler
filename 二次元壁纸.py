import os
import requests
from bs4 import BeautifulSoup
import sys


class DownloadPics:
    def __init__(self, keyword):
        # 关键词
        self.keyword = keyword
        # 网址
        self.url = 'https://konachan.net/'
        # 搜索的网址
        self.serach_url = 'https://konachan.net/post?tags=' + keyword

    def make_dirs(self):
        if os.path.isdir(self.keyword):
            print(self.keyword + '文件夹已经存在，但没有影响')
        else:
            print('该文件夹不存在，正在创建' + self.keyword + '文件夹')
            os.mkdir(self.keyword)
            print('创建成功...')

    def get_main_urls(self):
        urls = []
        try:
            res = requests.get(self.serach_url)
            if res.status_code == 200:
                print('正在搜索，请稍后......')
                soup = BeautifulSoup(res.text, 'lxml')
        except requests.RequestException:
            print('连接失败')
            sys.exit()
        list = soup.find(class_='content').find_all('li')
        page = soup.find(class_='pagination').find_all('a')[-2].string
        print('一共有{}页壁纸\n请选择下载页数(输入0代表全部下载，'
              '输入其他数字代表下载页数):'.format(page))
        download_pages = int(input(''))
        if download_pages == 0:
            download_pages = page
        for i in range(1, download_pages+1):
            n_search_url = 'https://konachan.net/post?page=' + \
                           str(i+1) + '&tags=' + self.keyword
            res2 = requests.get(n_search_url)
            soup2 = BeautifulSoup(res2.text, 'lxml')
            list2 = soup2.find(class_='content').find_all('li')
            for item in list2:
                urls.append(self.url + item.find(class_='inner').find(class_='thumb').get('href'))
        return urls

    def get_download_urls(self, urls):
        # 储存图片下载链接的列表
        download_urls = []
        print('正在搜索下载链接请稍后......')
        for url in urls:
            res3 = requests.get(url)
            soup3 = BeautifulSoup(res3.text, 'lxml')
            download_urls.append(soup3.find(class_='content').find(class_='image').get('src'))
        print('搜索成功，正在进入下载')
        return download_urls

    def download_pics(self, download_urls):
        for i in range(len(download_urls)):
            img_name = self.keyword + ' ' + str(i+1) + '.jpg'
            with open(self.keyword + '/{}'.format(img_name), 'wb') as f:
                img = requests.get(download_urls[i]).content
                f.write(img)
                print('图片' + img_name + '下载成功')
        print('下载完成')


if __name__ == '__main__':
    urls = []
    download_urls = []
    kywd = input('输入搜索的关键词:')
    # 获得每页图片的url
    fun = DownloadPics(kywd)
    # 创建文件夹
    fun.make_dirs()
    # 获得每个图片主页的url
    urls = fun.get_main_urls()
    # 获取高清大图的url
    download_urls = fun.get_download_urls(urls)
    # 下载图片
    fun.download_pics(download_urls)



