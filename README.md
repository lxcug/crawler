# crawler
## 爬取写真网站的美女图片
待爬取的网站有反爬机制，在你requests多次只会会远程停止你的连接，导致爬取失败。
我通过多次尝试直接抓取了该网站所有图集的urls，写入一个文件r.txt中，然后直接读取文件中的urls进行爬取
