#!/usr/bin/env python
# coding: utf-8

def run_scraper():

    import csv
    from datetime import datetime
    import requests
    from bs4 import BeautifulSoup

    template = "https://jobs.apple.com/en-us/search?location=united-states-USA&page=1&sort=newest&search=data%20engineer%20"


    def get_url(location,page,position):
        """Generate a. url from position and location"""
        #template = "https://jobs.apple.com/en-us/search?search={}&sort=relevance&location={}"
        template = "https://jobs.apple.com/en-us/search?location={}&page={}&sort=newest&search={}"
        url = template.format(location,page,position)
        return url

    url = get_url('united-states-USA',1,'"Data Engineer"')

    response = requests.get(url)

    soup = BeautifulSoup(response.text,'html.parser')

    def get_total_results_count(soup):
        results = soup.find('h2',{"id": "resultCount"}).span.text
        num = 0
        numchar = ""
        for char in results:
            if char.isnumeric():
                numchar+=char
        results = int(numchar)
        return results

    num_total_jobs = get_total_results_count(soup)
    num_total_jobs


    # store responses 

    urls = []
    job_id_list_of_lists = []


    import os
    from ast import literal_eval

    def check_if_job_id_exists_on_file(job_id):
        the_job_id_file = "/Users/williamsalinas/airflow/dags/job_id_list.txt"

        if os.stat(the_job_id_file).st_size != 0:
            with open(the_job_id_file) as f:
                content = f.read().replace('\n','')
            job_id_array_from_file=literal_eval(content)

            
            array_of_list_from_file = []
            for i in job_id_array_from_file:
                for job_id_from_file in i:
                    array_of_list_from_file.append(job_id_from_file)
                    
            if job_id not in array_of_list_from_file:
                return job_id


    def job_id_list_func(soup):
        job_id_list = []
        jobs_list = soup.find_all('td','table-col-1')
        for job_url in jobs_list:
            job_id = job_url.a.get('id')
            #NEW STUFF 06/05/22
            id_exists = check_if_job_id_exists_on_file(job_id)
            if id_exists != None:
                    #THIS APPEND ALREADY EXISTED
                job_id_list.append(job_id)
            ##END OF NEW STUFF
        return job_id_list


    def get_total_pages():
        url = get_url('united-states-USA',1,'Data Engineer')
        soup = BeautifulSoup(response.text,'html.parser')
        total = soup.find_all('nav','pagination')[0].ul.find_all('li','pagination__mid')[0].find_all('span','pageNumber')
        total = total[1].text
        total = int(total)
        return total


    total = get_total_pages()


    total = get_total_pages()
    #total = 2
    for i in range(total):
        url = get_url('united-states-USA',i+1,'"Data Engineer"')
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        job_id_list=job_id_list_func(soup)
        
        job_id_list_of_lists.append(job_id_list)
        urls.append(url)


    #job_id_list_of_lists
    #urls


    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from time import sleep


    def open_job_links(url,job_id):
        detail_job = ""
        driver = webdriver.safari.webdriver.WebDriver(quiet=False)
        #driver = webdriver.Chrome('/usr/local/airflow/dags/chromedriver')
        driver.get(url);
        button = driver.find_element(By.ID,job_id)
        # clicking on the button
        if button != None:
            button.click()
            sleep(5)
            html_from_page = driver.page_source
            detail_job = BeautifulSoup(html_from_page, 'html.parser')
        return detail_job


    detail_job_array = []

    num = len(urls)
    for i in range(num):
        for job_id in job_id_list_of_lists[i]:
            print(urls[i],job_id)
            detail = open_job_links(urls[i],job_id)
            detail_job_array.append(detail)


    #len(detail_job_array)


    list_of_job_titles = []
    for detail_job in detail_job_array:
        job_details_list_but_get_only_element = detail_job.find_all('div','job-details')[0]
        job_detail = job_details_list_but_get_only_element
        job_title = job_detail.h1.text
        list_of_job_titles.append(job_title)
    list_of_job_titles


    def job_location_func(job_detail):
        job_location = job_detail.find('div','jd__header--info')
        job_location_list = job_location.find_all('span')
        job_location = ""
        for span in job_location_list:
            job_location += span.text
        return job_location



    list_of_job_locations = []
    for detail_job in detail_job_array:
        job_details_list_but_get_only_element = detail_job.find_all('div','job-details')[0]
        job_detail = job_details_list_but_get_only_element
        job_location = job_location_func(job_detail)
        list_of_job_locations.append(job_location)
    list_of_job_locations


    def job_qualifictions_func(job_detail):
        test = job_detail.find_all('div', recursive=False)
        test = test[1]
        test2 = test.find_all('div','jd__row--main jd__summary')[0]
        test3 = test2.ul.find_all('span')
        key_qualifications = []
        for span in test3:
            key_qualifications.append(span.text)
        return key_qualifications


    list_of_list_of_job_qualifications = []
    for detail_job in detail_job_array:
        job_details_list_but_get_only_element = detail_job.find_all('div','job-details')[0]
        job_detail = job_details_list_but_get_only_element
        list_of_job_qualifications = job_qualifictions_func(job_detail)
        list_of_list_of_job_qualifications.append(list_of_job_qualifications)
    list_of_list_of_job_qualifications


    def job_date_posted_func(job_detail):
        test = job_detail.find_all('div', recursive=False)
        test = test[1]
        date_posted = test.find_all('div','jd__row--sidebar jd__summary--sidebar')[0]
        date_posted = date_posted.time.text
        return date_posted


    list_of_job_date_posted = []
    for detail_job in detail_job_array:
        job_details_list_but_get_only_element = detail_job.find_all('div','job-details')[0]
        job_detail = job_details_list_but_get_only_element
        date_posted = job_date_posted_func(job_detail)
        list_of_job_date_posted.append(date_posted)
    list_of_job_date_posted


    def job_summary_func(job_detail):
        test = job_detail.find_all('div', recursive=False)
        test = test[1]
        test4 = test.find_all('div','jd__row--main jd__summary--main')[0]
        job_summary = test4.text
        return job_summary


    list_of_job_summary = []
    for detail_job in detail_job_array:
        job_details_list_but_get_only_element = detail_job.find_all('div','job-details')[0]
        job_detail = job_details_list_but_get_only_element
        job_summary = job_summary_func(job_detail)
        list_of_job_summary.append(job_summary)
    list_of_job_summary


    def job_description_func(job_detail):
        test = job_detail.find_all('div', recursive=False)
        test = test[1]
        test5 = test.find_all('div','jd__row--main jd__summary--main')[1]
        job_description = test5.text
        return job_description


    list_of_job_description = []
    for detail_job in detail_job_array:
        job_details_list_but_get_only_element = detail_job.find_all('div','job-details')[0]
        job_detail = job_details_list_but_get_only_element
        job_description = job_description_func(job_detail)
        list_of_job_description.append(job_description)
    list_of_job_description


    def job_education_and_experience_func(job_detail):
        test = job_detail.find_all('div', recursive=False)
        test = test[1]
        job_education_experience = []

        test6 = test.find('div', {"id": "accordion_education&experience"})
        #if type(test6.div.span) != "NoneType":    
        job_education_experience = test6.span
        
        if job_education_experience is None:
            job_education_experience = ""
        else:
            job_education_experience = job_education_experience.text

        return job_education_experience


    list_of_job_education_experience = []
    for detail_job in detail_job_array:
        job_details_list_but_get_only_element = detail_job.find_all('div','job-details')[0]
        job_detail = job_details_list_but_get_only_element
        job_education_experience = job_education_and_experience_func(job_detail)
        job_education_experience
        list_of_job_education_experience.append(job_education_experience)


    #list_of_job_education_experience


    def job_additional_qualifications_func(job_detail):
        test = job_detail.find_all('div', recursive=False)
        test = test[1]
        additinal_qualifications = []
        #check_if_size_greater_1 = len(test.find_all('div','jd__row--main jd__summary'))
        #accordion_additionalrequirements
        test7 = test.find('div', {"id": "accordion_additionalrequirements"})
        if test7 is None:
            additinal_qualifications = []
        else:
            test7 = test.find('div', {"id": "accordion_additionalrequirements"})
            additinal_qualifications_url = test7.ul
            
            if additinal_qualifications_url is None:
                additinal_qualifications = []
            else:
                additinal_qualifications_2 = test7.ul.find_all('span')
                get_spans_from_additional_spans = additinal_qualifications_2

                for span in get_spans_from_additional_spans:
                    additinal_qualifications.append(span.text)
                
        return additinal_qualifications


    list_of_list_of_additional_qualifications = []
    for detail_job in detail_job_array:
        job_details_list_but_get_only_element = detail_job.find_all('div','job-details')[0]
        job_detail = job_details_list_but_get_only_element
        additinal_qualifications = job_additional_qualifications_func(job_detail)
        list_of_list_of_additional_qualifications.append(additinal_qualifications)


    #list_of_list_of_additional_qualifications


    # STORING THEM IN A CSV

    import pandas as pd

    df = pd.DataFrame({'job_title': list_of_job_titles,
                    'job_location': list_of_job_locations,
                    'job_date_posted': list_of_job_date_posted,
                    'job_qualifications':list_of_list_of_job_qualifications,
                    'job_summary': list_of_job_summary,
                    'job_description':list_of_job_description,
                    'job_education_experience':list_of_job_education_experience,
                    'job_additional_qualifications':list_of_list_of_additional_qualifications})


    # from IPython.display import display
    # display(df.style.set_properties(**{
    #         'width': '230px',
    #         'max-width': '230px'
    #     }))


    df.to_csv('/Users/williamsalinas/airflow/dags/test_delta.csv',index=False)

    df_old = pd.read_csv('/Users/williamsalinas/airflow/dags/test_new.csv')


    # from IPython.display import display
    # display(df_old.style.set_properties(**{
    #         'width': '230px',
    #         'max-width': '230px'
    #     }))

    data = [df,df_old]
    df2 = pd.concat(data)

    # from IPython.display import display
    # display(df2.reset_index(drop=True).style.set_properties(**{
    #         'width': '230px',
    #         'max-width': '230px'
    #     }))

    df2.to_csv('/Users/williamsalinas/airflow/dags/test_merge.csv',index=False)

    #NEW CODE 06/09/22
    df_merge = pd.read_csv('/Users/williamsalinas/airflow/dags/test_merge.csv')
    python_string_format = "%Y/%m/%d"
    
    #convert the column in date format to apply strftime
    df_merge['job_date_posted'] = pd.to_datetime(df_merge['job_date_posted'])
    
    #apply desired date format
    df_merge['job_date_posted'].dt.strftime(python_string_format)

    #NEEDED TO GET RID OF THE TIME (HOUR,MINITE,SECOND) AND JUST KEEP THE DATE
    df_merge['job_date_posted'] = df_merge['job_date_posted'].dt.date
    
    df_merge.to_csv('/Users/williamsalinas/airflow/dags/data_engineer_apple_job_postings.csv',index=False)
    #update list
    #path to delete temp csv files
    temp_csv_merge="/Users/williamsalinas/airflow/dags/test_merge.csv"
    temp_csv_delta="/Users/williamsalinas/airflow/dags/test_delta.csv"
    if os.path.exists(temp_csv_merge):
        os.remove(temp_csv_merge)
    if os.path.exists(temp_csv_delta):
        os.remove(temp_csv_delta)
