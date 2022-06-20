import logging
import re
import ssl
import requests
from lxml import etree
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import time
import random

logging.captureWarnings(True)


def getHtmlText(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0", 'Cookie':'your cookies'}
    r = requests.get(url, headers = headers, verify = False)
    r.encoding = 'utf-8'
    return r.content

def getCollectionTitle(html):                    # 获取收藏夹标题
    html = etree.HTML(html)
    title = html.xpath('/html/body/div[3]/div[1]/div/div//h2/a/text()')
    return title

def getCollectionLinks(html):                  #获取收藏夹地址
    html = etree.HTML(html)
    link = html.xpath('/html/body/div[3]/div[1]/div/div//h2/a/@href')
    for i in range(len(link)):
        link[i] = 'https://www.zhihu.com/'+link[i]
    return link

def getContentTitle(html):             #收藏内容的标题
    html = etree.HTML(html)
    title = html.xpath('/html/body/div[3]/div[1]/div/div[2]//h2/a/text()')     #获取标题
    return title

def getContentLink(html):                   #获取展开内容的链接，cautions:因为有专栏和问答，所以链接比较混乱。需要判断和补全
    links = re.findall(r'<link itemprop="url" href="(.*?)">', html.decode('utf-8'), re.S)
    link = []
    for lin in links:
        if (lin[0:9] == '/question'):
            link.append('https://www.zhihu.com' + lin)           #答案地址补全
        if (lin[0:16] == 'https://zhuanlan'):
            link.append(lin)
    return link

def getContentMarkdown(url):
    if str(url).startswith('https://www'):
        html = getHtmlText(url)
        soup = BeautifulSoup(html, "html.parser")
        content_title = soup.find_all("h1", class_="QuestionHeader-title")[0].get_text()
        body = soup.find_all(class_="RichContent-inner")[0]
    if str(url).startswith('https://zhuanlan'):
        html = getHtmlText(url)
        soup = BeautifulSoup(html, "html.parser")
        body = soup.find(class_="RichText ztext Post-RichText")
        content_title = soup.find(class_="Post-Title").get_text()
    html_template = """
        <!DOCTYPE html>
        <html>
        <body>
        <h1>{title}</h1>
        {content}
        </body>
        </html>
        """  # html网页框架
    html = html_template.format(title=content_title, content=body)
    return html

def main():

    #获取收藏夹全部标题
    url = 'https://www.zhihu.com/collections/mine'
    html = getHtmlText(url)           #获取“我的收藏页面的html内容”
    title = getCollectionTitle(html)            #获取收藏夹的标题
    title_links = getCollectionLinks(html)      #获取收藏夹的链接，收藏夹收藏的内容>10条需要分页
    #判断该收藏夹是否大于10条收藏内容
    i = 0
    pages = []                       #全部收藏页面
    for links in title_links:                       #获取收藏夹内的所有收藏链接
        bookmark_detail = getHtmlText(links)        #点击收藏夹，进入收藏夹
        bookmark_detail_etree = etree.HTML(bookmark_detail)        #为lxml解析做准备
        max_page = bookmark_detail_etree.xpath('//div[@class="zm-invite-pager"]/span[last()-1]/a/text()')        #判断收藏条数是否大于10条

        if len(max_page) == 0:
            bookmark_page = links
            pages.append(bookmark_page)
            print(bookmark_page)

        if len(max_page) != 0:
            for i in range(1, int(max_page[0])+1):
                bookmark_page = links + '?page='+ str(i)
                pages.append(bookmark_page)
                print(bookmark_page)

    collection_title = []
    collection_link = []
    for i in range(len(pages)):
        pages_link = pages[i]
        pages_content = getHtmlText(pages_link)
        print(getContentTitle(pages_content), getContentLink(pages_content))
        collection_title.append(getContentTitle(pages_content))
        collection_link.append(getContentLink(pages_content))

    all_anwser_links = []
    all_titles = []
    for i in range(len(collection_link)):
        for j in range(len(collection_link[i])):
            all_anwser_links.append(collection_link[i][j])
            all_titles.append(collection_title[i][j])
            # print(all_anwser_links)
            with open("address.txt", 'a') as f:
                f.write(collection_link[i][j] + '\n')

    with open('address.txt', 'r+') as f:
        line = f.read()
    a = line.split('\n')

    for i in range(len(a)):
        time.sleep(random.randint(0, 9))
        every_content = getContentMarkdown(a[i])
        print('the {i} of all {b} competiton'.format(i=i, b=len(a)))
        if ((i / 100) + 1):
            with open('{a}.md'.format(a=int(i / 100)), 'a', encoding='utf-8') as f:
                f.write(md(every_content))
                f.write('\n' * 2)

if __name__ == '__main__':
    main()
