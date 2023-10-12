import os
import re
import langdetect
import pandas as pd
import requests
from  time import  time
from langdetect import DetectorFactory
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


'''----YouTube (youtube.py)----'''
# function to create a csv
def create_csv():
    # this function creates csv file name channels.csv if it's not
    # already exists
    if not os.path.exists('channels.csv'):
        df = pd.DataFrame(columns=[
            'search query' ,'urls',
            'channel name',
            'channel id' ,'subscribers'])
        csv = df.to_csv('channels.csv' ,index=False)
    return  pd.read_csv('channels.csv')

# function to build the url
def build_url(keyword:str,url:str)-> str:
    '''this method to build a url with filter applied which just
    a part of string along with the url'''
    keyword ='+'.join(keyword.split(' '))
    video_url =  f'{url}/results?search_query={keyword}&sp=EgYIBBABGAM%253D' #&sp=EgYIBBABGAM%253D
    return video_url

#setring up the driver
def driver_setup(headless=True):
    '''this function takes care of setting up the driver'''
    options = Options()
    if headless:
        options.add_argument('--headless=new')
    service = Service(executable_path="driver/chromedriver.exe")
    driver = webdriver.Chrome(options=options, service=service)
    driver.maximize_window()
    return  driver

# scrolling function
def infinite_scroll(driver):
    '''this method will press the pagedown key on keyboard
    untill it finds the No Result text on the page'''

    if 'Try different keywords or remove search filters' in driver.page_source:
        print('There is no Channel for this keyword')
        return # it just terminates the infinite loop if meets the condition
    js_code = 'window.scrollBy(0, 10000);'
    while True:
        driver.execute_script(js_code)
        page_end = driver.find_elements(
            By.XPATH, '//yt-formatted-string[@id="message"]') # No Results text on page
        if page_end:
            break

# to clean the subscribers text
def clean_subscribers(subscriber_count:str)->float:
    # it removes M and K and gives appropriate number 1000000 and 1000
    # then returns the subscriber count as float
    if 'M' in subscriber_count:
        subscriber_count = subscriber_count.replace('subscribers','').replace('M','')
        subscriber_count = float(subscriber_count)*1000000
    elif 'K' in subscriber_count:
        subscriber_count = subscriber_count.replace('subscribers','').replace('K','')
        subscriber_count = float(subscriber_count)*1000
    else:
        subscriber_count = float(subscriber_count.replace('subscribers',''))
    return  subscriber_count

# storing status of the requested url on appropriate rows
def store_response(status_code,url,df):
    # Check if the URL is present in the DataFrame
    if url in df['urls'].values:
        # Get the index of the URL in the DataFrame
        index = df.index[df['urls'] == url].tolist()[0]
        # Update the 'response' column in the appropriate row
        df.at[index, 'response'] = status_code

#updating subscribers in to csv
def update_subscribers(df,urls_subscribers):
    for url_subscriber in urls_subscribers:
        # Check if the URL is present in the DataFrame
        if url_subscriber[0] in df['urls'].values:
            # Get the index of the URL in the DataFrame
            index = df.index[df['urls'] == url_subscriber[0]].tolist()[0]
            # Update the 'subscribers' column in the appropriate row
            df.at[index, 'subscribers'] = url_subscriber[1]


# check before giving request to urls in df
def check_urls(urls,df):
    # if url not in df only stored in below list and get returned by the func
    url_not_df = [url for url in urls if url not in df['urls'].values]
    return  url_not_df


'''----ChannelAnalyzer (analyse.py)----'''

# this method checks whether the youtube channel has the eamil or not
# and update the status in to email column
def email_check(url: str, headers: dict, cookies: dict, filter: bool) -> None:
    """
    Check whether a channel has a business enquiry email by scraping its 'about' page.

    Parameters:
        url (str): The URL of the channel's 'about' page.
        headers (dict): Headers to be used in the HTTP request.
        cookies (dict): Cookies to be used in the HTTP request.
        filter (bool): If True, the function will search for patterns indicating
                       the presence of a business enquiry email.

    Returns:
        None: The function does not return anything. It updates the 'channels.csv' file
              with the email and status information for the channel.

    Note:
        The function assumes that the 'channels.csv' file contains a 'urls' column
        with the URLs of channels to be checked. It will update the 'email' and 'status'
        columns in this file based on the results of the check.
    """
    df = pd.read_csv('channels.csv') # reading csv and storing it in csv
    # Changing the videos page URL to about page
    about_url = url.replace('/videos', '') + '/about'
    if filter:
        response = requests.get(about_url, headers=headers, cookies=cookies)  # Getting response here
        # Looking for pattern that indicates a business enquiry email
        if re.search(r'[Ff]or\s?[Bb]usiness\s?[eiEI]n?q?u?i?r?i?e?s?|email|@gmail', response.text, re.M):
            email = 'yes'
            status = 'pass'
        else:
            email = 'no'
            status = 'pass'
    else:
        email = 'no'
        status = 'fail'
    if url.replace('/videos', '') in df['urls'].values:
        # Get the index of the URL in the DataFrame
        index = df.index[df['urls'] == url.replace('/videos', '')].tolist()[0]

        # Update the 'status and email' columns in the appropriate row
        df.at[index, 'email'] = email
        df.at[index, 'status'] = status
    df.to_csv('channels.csv', index=False)

# this function filters the time stamp based on few conditions
# to find out whether the youtuber posts video daily or not...
def filter_video_time_stamps( video_time_stamps: list) -> bool:
    """
           Check the video time stamps for validity.

           This function filters the video_time_stamps list to determine if it represents
           it falls under the condition. The stamps is considered valid if the first element of the list
           does not contain the string 'month', and the list contains between 7 to 14 occurrences
           of the strings 'day' or 'days', and at most 2 occurrences of 'sec', 'secs', 'min', 'mins',
           'hour', or 'hours'.

           Parameters:
               video_time_stamps (list): A list of strings representing the video time stamps. The list
                   should contain timestamps in the form of 'X days/secs/mins/hours ago'.

           Returns:
               bool: True if the video time stamps satisfy the condition, False otherwise.
           """
    if 'month' in video_time_stamps[0]:  # if the lastest video posted month ago
        return False
    string = ' '.join(video_time_stamps)
    pattern = re.compile(r'secs?|minutes?|hours?|day$')  # making regex pattern to filter
    posts_in_day = len(re.findall(pattern, string))  # how many videos  in a day?
    posts_per_day = len(re.findall(r'days?', string))  # how many videos per day
    if posts_in_day <= 2 and (posts_per_day >= 7 and posts_per_day <= 14):
        return True  # if two max videos upload in a day and one/two days? one video
    else:
        return False

# this function detects the language of the youtube channel using few conditions
def detect_language(titles:list) -> bool:
    """
    Detects the dominant language from a list of YouTube video titles and checks for specific conditions.

    This function takes a list of video titles as input and detects the dominant language
    for each title using the langdetect library. It then checks for specific conditions
    to determine whether the titles meet the required criteria.

    Parameters:
    titles (list): A list of strings representing the video titles to be analyzed.

    Returns:
    bool: True if the titles meet the specified conditions, False otherwise.
    """
    DetectorFactory.seed = 0 # it will detect lang always as same before.
    # below line gets list of video titles and detects langs and score of each
    langs_and_scores = [langdetect.detect_langs(title) for title in titles if title]
    # we are getting the [lang,lang,lang] from the [[lang:score][lang:score][lang:score]]
    languages = [str(lang).split(':')[0] for lang_and_score in langs_and_scores
                 for lang  in lang_and_score]
    # if any of the video's lang is "ta" or all of the videos lang are "en" return True
    # else False.
    if 'ta' in languages:
        return True
    elif all( lang=='en' for lang in languages):
        return True
    else:
        return False

# this function filters the youtbe channel based the few conditions
def filter_channel(
        df: pd.DataFrame, titles: list,
        video_time_stamps: list, url: str,exception:list) -> bool:
    """
    Filters YouTube Channel based on specific conditions.

    This method filters YouTube Channel data stored in a pandas DataFrame to determine whether
    the input channel url meets the required conditions for processing. The conditions
    include checking the subscribers_count, detecting the language of video titles,
    and filtering the video_time_stamps using helper functions.

    Parameters:
        df (pd.DataFrame): A pandas DataFrame containing YouTube Channel data, where each row represents
            a YouTube Channel data and columns include 'urls' and 'subscribers_count'.
        video_time_stamps (list): A list of strings representing the timestamps of the video.
        titles (list): A list of strings representing the titles of the video.
        url (str): A string representing the URL of the video.

    Returns:
        bool: Returns True if the video meets all the specified conditions; otherwise, returns False.
    """
    # condition is applied to locate the subscribers_count for the appropriate urls
    condition = df['urls'].str.contains(url.replace('/videos', ''))
    subscribers_count = df.loc[condition, 'subscribers'].to_list()[0]
    # Check if the subscribers_count is within the required range
    if 1000 <= subscribers_count <= 1000000:
        subscribers_count = True
    else:
        subscribers_count = False
    try:
        language_filter = detect_language(titles) # detects language and returns bool
    except Exception as e:
        exception.append(f'check the detect_language function in the helper.py for ' \
              f'this error message: \n"{e}"')
    try:
        time_stamp_filter = filter_video_time_stamps(video_time_stamps) # filters timestamp and returns bool
    except Exception as e:
        exception.append(f'check the time_stamp_filter function in the helper.py for ' \
              f'this error message: \n"{e}"')
    # Check if the video titles are in the right language and video time stamps meet the criteria
    if (time_stamp_filter and language_filter) and subscribers_count:
        return True
    else:
        return False


'''---Main (__main__.py)---'''
# this decorator function is to tell us  time taken for running the function

def timing_decorator(func):
    def wrapper(*arg,**kwargs):
        start_time = time()
        func(*arg,**kwargs) # calls the orginal function
        end_time = time()
        execution_time = (end_time-start_time)/60
        print(f'time taken for running the {func.__name__} is : {execution_time:.3f} mins')
    return  wrapper