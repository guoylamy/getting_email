import csv
import time
import multiprocessing
import os
from urllib.parse import urlparse
import random
import utility
import zen
from geopy.geocoders import Nominatim

path_data = '/home/amy/Summer Intern/Email/Zen/'
path_contact = path_data + 'result_contact/'
fail_url = []

def get_all_skills():
    urls = list()
    with open(path_data + 'all_urls.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
#            urls.append(row[0])
            get_skill_pages(row[0])
    print('Number of skill urls: ', len(urls))
#    pool = multiprocessing.Pool(processes=8)
#    pool.map(get_skill_pages, urls)
#    pool.close()
#    pool.join()

def request_skill_page(link):
#    driver = utility.get_firefox()
    driver = utility.get_headless_chrome()
    driver.get(link)
    time.sleep(random.randint(1, 2))
#    if 'Robot Check' not in driver.title:
#        driver = driver.page_source
    
    
    print('-----link:',link,'-----')
    try:
        name = driver.title
        nick_name = name.split(' ')[0]   
        user_name = name.split('(')[1].split(')')[0]
#        user_email = driver.find_element_by_xpath('//*[@itemprop="email"]/a').text
        user_region = driver.find_element_by_xpath('//*[@itemprop="homeLocation"]').text
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
        location = geolocator.geocode(user_region)
        add = location.address
        user_country = add.split(' ')[-1]
        if user_country == 'America':
            user_country = 'USA'
        if user_country not in ['中国','America','USA','India','Deutschland','UK','Nederland','España','France','България','Danmark','Portugal','Polska','Éire','Ireland','Malta']:
            print("not target country")
            return []

        user_email = zen.all(link,nick_name)
        if user_email==None:
            fail_url.append(link)
            print("cannot find user_email")
            return []
        if '@' in user_email:
            if '@users.noreply.github.com' in user_email:
                print('@users.noreply.github.com')
                return []
            user_info = [link,user_name,nick_name, user_email,user_country]
            print(user_info)
        else:
            print("no @ in user_email")
            fail_url.append(link)
            return []
    except:
        print("===incomplete:",link,"===")
        user_info = []
    
    driver.close()
    driver.quit()
#    return page
    return user_info

def get_skill_pages(url):
#    url_parse = urlparse(url)
#    url_id = url_parse.path.split('/')[1]
#    filename = url_id + '.html'
#    if filename in os.listdir(path_html):
#        return
    list_users = request_skill_page(url)
#    while len(list_users)==0:
#        request_skill_page(url,list_users)
    if len(list_users) == 0:
        return
    with open(path_contact + 'contact.csv', 'a') as FileOut:
        try:
            writer = csv.writer(FileOut, lineterminator='\n')
            print("write item:",list_users)
            writer.writerow(list_users)
        except:
            print("gbk cannot encode")
    print('Done: ', url)


if __name__ == '__main__':
    start = time.time()
    if not os.path.exists(path_contact):
        os.mkdir(path_contact)
    get_all_skills()
    #get_skill_pages('https://www.amazon.com/dp/B07D25QW22')
    with open(path_data + 'fail_url.csv', 'w') as FileOut:
        for item in fail_url:
            writer = csv.writer(FileOut, lineterminator='\n')
            writer.writerow(fail_url)
    end = time.time()
    time_exec = end - start
    print('Total exec time: ', time_exec/3600)
