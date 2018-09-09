import requests,pymysql
from requests import RequestException
from pyquery import PyQuery


def get_one_page(page):
    try:
        url = 'https://search.jd.com/Search?keyword=ipad&page={}'.format(page)
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        response = requests.get(url,headers=headers)
        response.encoding = 'utf-8'
        return response.text
    except RequestException:
        return None


def parse_one_page(html):
    doc = PyQuery(html)
    price_list = doc('.p-price i').text().split()
    em_list = doc('.p-name em').items()
    comment_list = doc('.p-commit strong a').text().split()
    shop_list = doc('.p-shop').text().split()
    for price,title,comment,shop in zip(price_list,em_list,comment_list,shop_list):
        yield {
            'price':price,
            'title':title.text(),
            'comment':comment,
            'shop':shop
        }


def save_to_mysql(item):
    table = 't_goods'
    values = ','.join(['%s'] * len(item))
    try:
        sql = 'insert into {table} values(0,{values})'.format(table=table,values=values)
        cursor.execute(sql,tuple(item.values()))
        conn.commit()
        print('插入mysql成功')
    except Exception as e:
        print('插入mysql失败')
        print(e)
        conn.rollback()


def main():
    for i in range(0,20,2):
        html = get_one_page(i+1)
        for item in parse_one_page(html):
            save_to_mysql(item)

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='zws123456', db='jdgoods',charset='utf8')
    cursor = conn.cursor()
    main()