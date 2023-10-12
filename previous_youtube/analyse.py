'''importing required modules here'''
import json
import re
import traceback
from concurrent.futures import ThreadPoolExecutor
from time import time
import helper
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


class ChannelAnalyzer :
    COOKIES = {
        'VISITOR_INFO1_LIVE': 'LwaxKRZtIw8',
        'YSC': 'LNp1RoB5gPQ',
        'PREF': 'f4=4000000&tz=Asia.Calcutta&f5=30000&gl=US',
        'LOGIN_INFO': 'AFmmF2swRAIgZb637gFzNg6UTrGvpWvjACZcyQlh2HtLrYw_KyKT-XECICyDY3NqMfrv5M7lTte5ESP_Ha7Zu5Mm2wvIT7fG4Xu-:QUQ3MjNmd3JzQl9wMGExZ0lUSDMwdERDZWFjUFdfWTdLVjVDVVFMSE1aUmVIMkZsYXFpbEtjSGIwRzBUZlM1a1BJQ0dsQ1lNelhOcEhBTEhVcHFUNnpyMEFGQTNjdEtrSW8wVTVEa0p6dEFuNk1UeDQtUWVmdDlNRVp1bG5tN3dwOXk4ZUk4ZHY5M29oaVlNZkV4RjFGNG9YRkFBTUxJLUQxZzRmZzUyUzRwei1hOGY0cjJzQl9CYksxVnk4R3V6Y2NMMXctaWdBU01tM1JWc2JFY3l0VEFjTk4tcGg4NUR2dw==',
        'SID': 'YwgGZXrH7E0hL4eweK7cK5vmszJdhHNq5X-j8EuIhfYZTE4YMTNExVB-d2NilZ8vFxpoiQ.',
        '__Secure-1PSID': 'YwgGZXrH7E0hL4eweK7cK5vmszJdhHNq5X-j8EuIhfYZTE4YQyaZrxPL8NL4L1cG3EPBDQ.',
        '__Secure-3PSID': 'YwgGZXrH7E0hL4eweK7cK5vmszJdhHNq5X-j8EuIhfYZTE4Y62zG-RVSmhp_xOp_1Jnbog.',
        'HSID': 'Al-_yPCzsbeMHkKqw',
        'SSID': 'AwF-IVorIOmUmFN2f',
        'APISID': 'HcIzNrsjSdCwtLKs/AJhmJZaw7MgypEgFY',
        'SAPISID': 'f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA',
        '__Secure-1PAPISID': 'f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA',
        '__Secure-3PAPISID': 'f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA',
        'SIDCC': 'APoG2W_Hn0F62zj4yXIJrYuNGXkDYd2p9_3Dj-09riGMefMc01x6vceZZLJjrE03PbL67XgCGwE',
        '__Secure-1PSIDCC': 'APoG2W_vHWsap1Ug4kqD8uR2Vwb499r25gEEjXuJlhRZsI-VpF1rAJ0rAVGWt5F6tswCZvq4rH0',
        '__Secure-3PSIDCC': 'APoG2W_zeSruta_u6vxiGBWwK4HClkl8KFeXHrmIT5kwZ6-6jO9tRDgVh0Z5Ee-hTrsuj6T6q9A',
    } # requests headers
    HEADERS = {
        'authority': 'www.youtube.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ta;q=0.8,hi;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': 'VISITOR_INFO1_LIVE=LwaxKRZtIw8; YSC=LNp1RoB5gPQ; PREF=f4=4000000&tz=Asia.Calcutta&f5=30000&gl=US; LOGIN_INFO=AFmmF2swRAIgZb637gFzNg6UTrGvpWvjACZcyQlh2HtLrYw_KyKT-XECICyDY3NqMfrv5M7lTte5ESP_Ha7Zu5Mm2wvIT7fG4Xu-:QUQ3MjNmd3JzQl9wMGExZ0lUSDMwdERDZWFjUFdfWTdLVjVDVVFMSE1aUmVIMkZsYXFpbEtjSGIwRzBUZlM1a1BJQ0dsQ1lNelhOcEhBTEhVcHFUNnpyMEFGQTNjdEtrSW8wVTVEa0p6dEFuNk1UeDQtUWVmdDlNRVp1bG5tN3dwOXk4ZUk4ZHY5M29oaVlNZkV4RjFGNG9YRkFBTUxJLUQxZzRmZzUyUzRwei1hOGY0cjJzQl9CYksxVnk4R3V6Y2NMMXctaWdBU01tM1JWc2JFY3l0VEFjTk4tcGg4NUR2dw==; SID=YwgGZXrH7E0hL4eweK7cK5vmszJdhHNq5X-j8EuIhfYZTE4YMTNExVB-d2NilZ8vFxpoiQ.; __Secure-1PSID=YwgGZXrH7E0hL4eweK7cK5vmszJdhHNq5X-j8EuIhfYZTE4YQyaZrxPL8NL4L1cG3EPBDQ.; __Secure-3PSID=YwgGZXrH7E0hL4eweK7cK5vmszJdhHNq5X-j8EuIhfYZTE4Y62zG-RVSmhp_xOp_1Jnbog.; HSID=Al-_yPCzsbeMHkKqw; SSID=AwF-IVorIOmUmFN2f; APISID=HcIzNrsjSdCwtLKs/AJhmJZaw7MgypEgFY; SAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; __Secure-1PAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; __Secure-3PAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; SIDCC=APoG2W_Hn0F62zj4yXIJrYuNGXkDYd2p9_3Dj-09riGMefMc01x6vceZZLJjrE03PbL67XgCGwE; __Secure-1PSIDCC=APoG2W_vHWsap1Ug4kqD8uR2Vwb499r25gEEjXuJlhRZsI-VpF1rAJ0rAVGWt5F6tswCZvq4rH0; __Secure-3PSIDCC=APoG2W_zeSruta_u6vxiGBWwK4HClkl8KFeXHrmIT5kwZ6-6jO9tRDgVh0Z5Ee-hTrsuj6T6q9A',
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
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-client-data': 'CJa2yQEIorbJAQipncoBCN/zygEIlKHLAQia/swBCIWgzQEI5LDNAQjatM0BCNy9zQEIu77NAQjgxM0BCO/EzQEImsXNAQjBxc0BGNOdzQE=',
    } # cookies for requests

    def __init__(self,df:pd.DataFrame):
        """
           Initialize an instance of the ChannelAnalyzer class.

           Parameters:
               df (pd.DataFrame): A pandas DataFrame containing YouTube channel data, where each row represents
                   a YouTube channel entry with columns 'urls' and 'subscribers_count'.

           Returns:
               None

           Note:
               The 'send_requests' method is responsible for starting the channel analysis, where channel URLs are
               processed in parallel using ThreadPoolExecutor with a maximum of 4 worker threads.
           """
        self.df = df
        self.exception = []
        self.send_requests() # starts analysing process
        print(set(self.exception))

    def get_videos_details(self,videoinfo:list)->tuple:
        """
          Extracts video titles and timestamps from a list of video information.

          This function takes a list of video information and extracts the video titles
          and timestamps for each video. The video information should be in the form of a list,
          and each item in the list should contain information about a video.

          Parameters:
              videoinfo (list): A list containing information about YouTube videos.

          Returns:
              tuple: A tuple containing two lists - titles and video_time_stamps.
                  - titles (list): A list of strings representing the titles of the videos.
                  - video_time_stamps (list): A list of strings representing the timestamps
                    of the videos in the format 'X days/secs/mins/hours ago'.

          Note:
              If any error occurs while extracting the information for a video, the function
              will print an error message along with the problematic video information and
              continue processing the remaining videos.
          """
        titles = [] # to store all the titles of the videos
        video_time_stamps = [] # to store the all the timestamps of the videos
        for info in videoinfo:
            try:
                # Extract the video title from the video information
                video_title = info['richItemRenderer'][
                'content']['videoRenderer']['title']['runs'][0]['text']
                titles.append(video_title)

                # Extract the video timestamp from the video information
                video_time_stamps.append(info[
                'richItemRenderer']['content']['videoRenderer'][
                'publishedTimeText']['simpleText'])
            except Exception as e :
                # If an error occurs, print an error message along with the problematic video information
                self.exception.append(f'exception occured  in get_videos_details error is :{e}\n{info}')
        return titles,video_time_stamps

    def process_urls(self,url):
        """
            Process a URL and extract video information.

            This function takes a URL, sends an HTTP request to the URL, and processes the response
            to extract video information such as video titles and timestamps. It uses the BeautifulSoup
            library to parse the HTML contents of the URL page and extract the necessary data.

            Parameters:
                url (str): The URL of the YouTube channel's video page.

            Returns:
                str: An empty string.

            Note:
                This function relies on the helper method 'get_videos_details' to extract video titles
                and timestamps from the parsed HTML content. If any error occurs during the process,
                error messages will be printed to the console.
            """
        response = requests.get(url, cookies=self.COOKIES, headers=self.HEADERS)
        if response.status_code == 200:
            soup = bs(response.text, 'lxml') # parsing html contents of the url page
            try:
                script_tag = soup.find('script', string=re.compile('var ytInitialData =.*'))
                json_object = re.search('=\s(\{.*\});</script>', str(script_tag), re.M).group(1)
                video_info_dic = json.loads(json_object)
                videoinfo = video_info_dic['contents']['twoColumnBrowseResultsRenderer']['tabs'][1][
                'tabRenderer']['content']['richGridRenderer']['contents']
                try:
                    # Extract video titles and timestamps using the helper method 'get_videos_details'
                    video_titles,time_stamps = self.get_videos_details(videoinfo)
                    # video_titles,time_stamps = title_time_stamp[0],title_time_stamp[1]
                except Exception as e:
                    self.exception.append(f'check the get_videos_details function for'\
                          f'this error message : \n{e}')
                try:
                    # Filter the YouTube channel using the extracted video titles, timestamps, and URL
                    filter_  = helper.filter_channel(self.df, video_titles, time_stamps, url,self.exception)
                    try:
                        helper.email_check(url,self.HEADERS,self.COOKIES,filter_)
                    except Exception as e:
                        self.exception.append('check the email_check function in helper module for this '\
                              f'errros message: {e}')

                except Exception as e:
                    self.exception.append(f'check the filter_channel function in the helper.py for ' \
                          f'this error message: \n"{e}"')
                    traceback.print_exc()

            except Exception as e:
                self.exception.append(f'check the videoinfo in process_urls for this error: {e}')
        else:
            print(f'response is not ok:{response.status_code} {response.url}')

    def send_requests(self):
        """
        Process YouTube channel URLs in parallel using ThreadPoolExecutor.

        This method takes the URLs of YouTube channel video pages from the DataFrame and appends
        '/videos' to each URL to create the video page URLs. Then, it uses ThreadPoolExecutor
        from the concurrent.futures module to process these URLs in parallel with a maximum of 4
        worker threads.

        Parameters:
            None

        Returns:
            None

        Note:
            This method relies on the 'process_urls' method to process individual video page URLs.
            The ThreadPoolExecutor enables concurrent processing, which can speed up the overall
            execution time.
        """
        urls = [
            url + '/videos' for url in list(self.df['urls'])] # making videos page urls
        with ThreadPoolExecutor(max_workers=4) as executor: # using concurrent futures
            executor.map(self.process_urls,urls)



