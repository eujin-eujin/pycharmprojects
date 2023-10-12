# import required libraries
import json
import re
from time import time
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from helper import *


class YouTube:
    URL = 'https://www.youtube.com'
    COOKIES = {
        'YSC': 'Zz_O20FcZLM',
        'VISITOR_INFO1_LIVE': 'Mi9O6FN657g',
        'PREF': 'f4=4000000&tz=Asia.Calcutta',
        'GPS': '1',
    }
    HEADERS = {
        'authority': 'www.youtube.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': 'YSC=Zz_O20FcZLM; VISITOR_INFO1_LIVE=Mi9O6FN657g; PREF=f4=4000000&tz=Asia.Calcutta; GPS=1',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"114.0.5735.199"',
        'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.199", "Google Chrome";v="114.0.5735.199"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    def __init__(self,keyword):
        self.keyword = keyword
        self.df = create_csv()
        self.start()

    def save_csv(self,channel_id:str,channel_name:str)->None:
        ''' this method is to save the each row to the existing csv'''
        channel_dic = {
            'search query': self.keyword,
            'urls': '',
            'channel name': channel_name,
            'channel id': channel_id,
            'subscribers': ''
        }
        df = pd.DataFrame([channel_dic]) # creates single row of the dataframe
        if not ((self.df['channel name'] == channel_name) & (
                self.df['channel id'] == channel_id)).any():  # check for dublicates
            self.df = pd.concat([self.df, df], ignore_index=True) # appends the row into existing df
            csv = self.df.to_csv('channels.csv', index=False) # stores all the data in existing csv

    def get_chanels(self):
        '''this method is to get the channel name and channel id of the
        search results'''
        infinite_scroll(self.driver)
        html = self.driver.page_source
        soup  = BeautifulSoup(html,'lxml') # parsing here
        videos = soup.find_all('ytd-video-renderer',{
            "class":"style-scope ytd-item-section-renderer"}) # getting all the videos container
        for video in videos:
            try:
                #parsing channel name
                channel_name = video.find('a',{
            'class':'yt-simple-endpoint style-scope yt-formatted-string'}).text.strip()
            except:
                channel_name = ''
            try:
                #parsing channel id
                channel_id  = video.find('a',{
                    'class':'yt-simple-endpoint style-scope yt-formatted-string'})['href']
            except:
                channel_id = ''
            self.save_csv(channel_id,channel_name)


    def get_subscribers(self):
        '''this method to get the subscribers of the channel from their
        chanel id we got the from the get_channels method'''
        def start_requests(url):
            response = requests.get(url,headers=self.HEADERS,cookies=self.COOKIES) # sending request to url page
            soup = BeautifulSoup(response.text,'lxml') # parsing html response
            store_response(response.status_code, url,self.df)  # storing response in to dataframe
            try:
                json_ = soup.find('script',string=re.compile(
                    'var ytInitialData = .*')).text # getting json content from the parsed soup
                json_data = re.search(r'var ytInitialData =(.*);',json_).group(1)
                data = json.loads(json_data)
                subscriber_count = data ['header'][
                    'c4TabbedHeaderRenderer']['subscriberCountText']['simpleText'] #getting subscriber_count
                return  url ,clean_subscribers(subscriber_count)
            except:
                try:
                    subscriber_count = re.search(
                    r"([\d.]+)\s?[kKmM]\s?Subscriber",response.text,re.DOTALL).group(1)
                    return  url , float(clean_subscribers(subscriber_count))
                except:
                    return  url,np.nan

        urls = self.df['channel id'].apply(
            lambda channel_id: self.URL + str(channel_id)) # making chanel url from chanel id
        # we are getting subscribers of the each channel by their url
        urls_list = check_urls(urls.values, self.df)
        self.df.loc[:, 'urls'] = urls
         # this line checks the url from df
        if urls_list:
            url_subscribers = list(map(start_requests,urls_list))
            update_subscribers(self.df,url_subscribers)# updating subscribers
            csv = self.df.to_csv('channels.csv',index=False) # saving the changes of the csv.

    def start(self):
        self.driver = driver_setup()
        url = build_url(self.keyword, self.URL)
        self.driver.get(url)
        self.get_chanels()
        self.get_subscribers()
        self.driver.close()






