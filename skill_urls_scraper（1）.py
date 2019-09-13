import csv
import time
import multiprocessing
import os
import random

from selenium.common.exceptions import NoSuchElementException

import utility


path_data = 'C:/Users/Tu Le/GoogleDriveUVA/dataset/'
path_categories = path_data + 'result_urls/'


def get_specific_categories():
    jobs = list()
    #jobs.append(('Novelty & Humor', 'https://www.amazon.com/s/ref=lp_13727921011_nr_n_14?fst=as%3Aoff&rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284858011&bbn=13727922011&ie=UTF8&qid=1551334584&rnid=13727922011'))
    jobs.append(('News', 'https://www.amazon.com/s/ref=lp_13727921011_nr_n_13?fst=as%3Aoff&rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284857011&bbn=13727922011&ie=UTF8&qid=1551334584&rnid=13727922011'))
    #jobs.append(('Weather', 'https://www.amazon.com/s/ref=lp_13727921011_nr_n_22?fst=as%3Aoff&rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284889011&bbn=13727922011&ie=UTF8&qid=1551334584&rnid=13727922011'))
    #jobs.append(('Music & Audio', 'https://www.amazon.com/s/ref=lp_13727921011_nr_n_12?fst=as%3Aoff&rh=n%3A13727921011%2Cn%3A%2113727922011%2Cn%3A14284851011&bbn=13727922011&ie=UTF8&qid=1551334584&rnid=13727922011'))

    pool = multiprocessing.Pool(processes=1)
    pool.starmap(get_pages, jobs)
    pool.close()
    pool.join()


def get_all_categories():
    # check progress
    completed = list()
    with open('progress.csv', 'r') as file_progress_in:
        progress_reader = csv.reader(file_progress_in)
        for row in progress_reader:
            completed.append(row[0])

    driver = utility.get_firefox()
    driver.get('https://www.amazon.com/b?ie=UTF8&node=13727921011')
    jobs = list()

    time.sleep(random.randint(5, 10))

    while 'Robot Check' in driver.title:
        driver.refresh()

    cates = driver.find_element_by_id('leftNav')
    links = cates.find_elements_by_tag_name('a')
    # stars = 4
    for link in links:
        if '& Up' in link.text or 'Days' in link.text:
            continue
            # jobs.append((str(stars) + link.text, link.get_attribute('href')))
            # stars -= 1
        else:
            if link.text not in completed:
                jobs.append((link.text, link.get_attribute('href')))
    driver.close()
    driver.quit()

    pool = multiprocessing.Pool(processes=8)
    pool.starmap(get_pages, jobs)
    pool.close()
    pool.join()


def get_number_of_pages(link_cate):
    driver = utility.get_firefox()
    driver.get(link_cate)
    time.sleep(random.randint(5, 10))

    if 'Robot Check' in driver.title:
        return 0

    try:
        num = int(driver.find_element_by_class_name('pagnDisabled').text)
    except NoSuchElementException:
        num = int(driver.find_elements_by_class_name('a-disabled')[-1].text)
    driver.close()
    driver.quit()
    return num


def get_skill_urls(link_page, list_skill_urls, list_failed):
    num_of_skills = 0
    driver = utility.get_firefox()
    driver.get(link_page)
    time.sleep(random.randint(1, 2))

    if 'Robot Check' in driver.title:
        if link_page not in list_failed:
            list_failed.append(link_page)
        return 0

    try:
        ul = driver.find_element_by_id('mainResults')
        lis = ul.find_elements_by_tag_name('li')
    except NoSuchElementException:
        lis = driver.find_elements_by_xpath(
            '//*[@class="sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"]')

    for li in lis:
        num_of_skills += 1
        url = 'https://www.amazon.com/dp/' + li.get_attribute('data-asin')
        list_skill_urls.append(url)
    driver.close()
    driver.quit()
    return num_of_skills


def get_pages(cate, link):
    # print('Start: ', cate, ' - ', link)
    num_of_skills = 0
    list_skill_urls = []
    list_failed_pages = []

    num_of_pages = get_number_of_pages(link)
    while num_of_pages == 0:
        num_of_pages = get_number_of_pages(link)

    #print('Number of pages for ', cate, ': ', num_of_pages)

    for num in range(1, num_of_pages + 1):
        link_page = link + '&page=' + str(num)
        num_of_skills_in_page = get_skill_urls(link_page, list_skill_urls, list_failed_pages)
        num_of_skills += num_of_skills_in_page
        #print('Page ', num, ': ', num_of_skills_in_page, ' skills')

    time.sleep(random.randint(5, 10))

    #count = 0
    while list_failed_pages:
        #count += 1
        #print('Loop ', count, ': list_failed remaining ', len(list_failed_pages), ' pages.')
        for page in list_failed_pages:
            num_of_skills_in_page = get_skill_urls(page, list_skill_urls, list_failed_pages)
            num_of_skills += num_of_skills_in_page
            if num_of_skills_in_page != 0:
                list_failed_pages.remove(page)

    with open(path_categories + cate + '_urls.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, lineterminator='\n')
        for item in list_skill_urls:
            writer.writerow([item])
    print('Done: ', num_of_skills, ' skills - ', cate, ' - ', link)
    with open('progress.csv', 'a') as file_progress_out:
        progress_writer = csv.writer(file_progress_out, lineterminator='\n')
        progress_writer.writerow([cate])


def combine_all_categories():
    list_final = []
    for filename in os.listdir(path_categories):
        with open(os.path.join(path_categories, filename), 'r') as file_in:
            reader = csv.reader(file_in)
            for row in reader:
                if row[0] not in list_final:
                    list_final.append(row[0])
    with open(path_data + 'all_urls.csv', 'w') as file_out:
        writer = csv.writer(file_out, lineterminator='\n')
        for item in list_final:
            writer.writerow([item])
    print('Done final: ', len(list_final), ' skills')


if __name__ == '__main__':
    if not os.path.exists(path_data):
        os.mkdir(path_data)
    if not os.path.exists(path_categories):
        os.mkdir(path_categories)
    start = time.time()
    get_all_categories()
    #get_specific_categories()
    combine_all_categories()
    end = time.time()
    time_exec = end - start
    print('Total exec time: ', time_exec/3600)
