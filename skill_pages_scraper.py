import csv
import time
import multiprocessing
import os
from urllib.parse import urlparse
import random
import utility


path_data = 'D:\大三暑\summer intern\week6(9.9)\email_data'
path_html = path_data + 'result_html/'


def get_all_skills():
    urls = list()
    with open(path_data + 'all_urls.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            urls.append(row[0])
    print('Number of skill urls: ', len(urls))
    pool = multiprocessing.Pool(processes=8)
    pool.map(get_skill_pages, urls)
    pool.close()
    pool.join()


def request_skill_page(link):
    page = None
    driver = utility.get_firefox()
    driver.get(link)
    #time.sleep(random.randint(1, 2))
    if 'Robot Check' not in driver.title:
        page = driver.page_source
    driver.close()
    driver.quit()
    return page


def get_skill_pages(url):
    url_parse = urlparse(url)
    url_id = url_parse.path.split('/')[2]
    filename = url_id + '.html'
    if filename in os.listdir(path_html):
        return
    print(filename)
    page = request_skill_page(url)
    while page is None:
        page = request_skill_page(url)
    with open(path_html + filename, 'w', encoding='utf-8') as file_skill:
        file_skill.write(page)
    print('Done: ', url_id)


if __name__ == '__main__':
    start = time.time()
    if not os.path.exists(path_html):
        os.mkdir(path_html)
    get_all_skills()
    #get_skill_pages('https://www.amazon.com/dp/B07D25QW22')
    end = time.time()
    time_exec = end - start
    print('Total exec time: ', time_exec/3600)
