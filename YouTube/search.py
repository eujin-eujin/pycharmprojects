'''importing required modules'''
import json
import os
import re
from time import time
import pandas as pd
import requests
from bs4 import BeautifulSoup


class SearcResult:
    ''' it searches keywords  and gets the channels id
    from the search results'''
    COOKIES = {
        'VISITOR_INFO1_LIVE': 'LwaxKRZtIw8',
        'YSC': 'LNp1RoB5gPQ',
        'PREF': 'f4=4000000&tz=Asia.Calcutta&f5=30000&gl=US',
        'HSID': 'Al-_yPCzsbeMHkKqw',
        'SSID': 'AwF-IVorIOmUmFN2f',
        'APISID': 'HcIzNrsjSdCwtLKs/AJhmJZaw7MgypEgFY',
        'SAPISID': 'f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA',
        '__Secure-1PAPISID': 'f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA',
        '__Secure-3PAPISID': 'f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA',
        '_ga': 'GA1.1.778450163.1690521906',
        '_ga_2D63NQQFBG': 'GS1.1.1690521906.1.1.1690521936.0.0.0',
        'LOGIN_INFO': 'AFmmF2swRAIgQ_b64q3rQVEcR_I-snJwPgacWL2mpb0teMR5ynWJn8ECIE7HNGB68ztL78D7nJ7JOfLGTEMZJBgn_p789YbZiw8U:QUQ3MjNmeG1xYXJFR0hfUlVwUy0zdk04LU43UDFvN2ktNFFZRVRwMDNYYVRRWVJVUndLRU5pdW9sMUtmVW13V1NYZm9LaXBIQ200RXNuaE5QNEVvd3piRU5NRmtFVG91R01jNkV5bXJFQm5nWEdZcEgtMExhRGJsOVdfaHpMdlFPeGpIWUJzNkcxUExjYkdlVUdHR3NERlBIcjVNWXdFLTBrZTQ3aHptRHJLXzVlNUtZaGRzdk5KRWk5WXBQb2x4azhudHdzMTRMcnJnYkFRZDFPQm5oNUpxZDlLY0NTVS1CZw==',
        'SID': 'ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEXTaPg2WgwHI9KsAfdBmtYLA.',
        '__Secure-1PSID': 'ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEXCZnljh7L0qRwPWqF_ufN0A.',
        '__Secure-3PSID': 'ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEX5OSVeZJ-XsEWlVrYrg7n0A.',
        'VISITOR_PRIVACY_METADATA': 'CgJJThICGgA%3D',
        '__Secure-1PSIDTS': 'sidts-CjEBSAxbGX6CiMV4Ex0XJKQrnt6VNT-4XJSeTsI6MtQZhB3TIXriFDEkFJt-SdlRte_TEAA',
        '__Secure-3PSIDTS': 'sidts-CjEBSAxbGX6CiMV4Ex0XJKQrnt6VNT-4XJSeTsI6MtQZhB3TIXriFDEkFJt-SdlRte_TEAA',
        'SIDCC': 'APoG2W-xLd4bRu03N3QaScGMEJLyEIoBW7_GUvU2hKld5ww11lJh36FzoZoHdvql0_ig-Sv_joun',
        '__Secure-1PSIDCC': 'APoG2W9ExTLVGmxrYkUEYoE0IBwyPfCaT4H78xgEJzUVA8Ib2wpzzEjtsI7OTGXWT_-sUn2aMPTP',
        '__Secure-3PSIDCC': 'APoG2W8ramXw7l0pFENqwpnrDtmytHpvpvDhk2CzlGDLyF740SL095p52TPIZjK4pn9mlqiBq2AY',
    } # requests cookies
    HEADERS = {
        'authority': 'www.youtube.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ta;q=0.8,hi;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': 'VISITOR_INFO1_LIVE=LwaxKRZtIw8; YSC=LNp1RoB5gPQ; PREF=f4=4000000&tz=Asia.Calcutta&f5=30000&gl=US; HSID=Al-_yPCzsbeMHkKqw; SSID=AwF-IVorIOmUmFN2f; APISID=HcIzNrsjSdCwtLKs/AJhmJZaw7MgypEgFY; SAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; __Secure-1PAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; __Secure-3PAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; _ga=GA1.1.778450163.1690521906; _ga_2D63NQQFBG=GS1.1.1690521906.1.1.1690521936.0.0.0; LOGIN_INFO=AFmmF2swRAIgQ_b64q3rQVEcR_I-snJwPgacWL2mpb0teMR5ynWJn8ECIE7HNGB68ztL78D7nJ7JOfLGTEMZJBgn_p789YbZiw8U:QUQ3MjNmeG1xYXJFR0hfUlVwUy0zdk04LU43UDFvN2ktNFFZRVRwMDNYYVRRWVJVUndLRU5pdW9sMUtmVW13V1NYZm9LaXBIQ200RXNuaE5QNEVvd3piRU5NRmtFVG91R01jNkV5bXJFQm5nWEdZcEgtMExhRGJsOVdfaHpMdlFPeGpIWUJzNkcxUExjYkdlVUdHR3NERlBIcjVNWXdFLTBrZTQ3aHptRHJLXzVlNUtZaGRzdk5KRWk5WXBQb2x4azhudHdzMTRMcnJnYkFRZDFPQm5oNUpxZDlLY0NTVS1CZw==; SID=ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEXTaPg2WgwHI9KsAfdBmtYLA.; __Secure-1PSID=ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEXCZnljh7L0qRwPWqF_ufN0A.; __Secure-3PSID=ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEX5OSVeZJ-XsEWlVrYrg7n0A.; VISITOR_PRIVACY_METADATA=CgJJThICGgA%3D; __Secure-1PSIDTS=sidts-CjEBSAxbGX6CiMV4Ex0XJKQrnt6VNT-4XJSeTsI6MtQZhB3TIXriFDEkFJt-SdlRte_TEAA; __Secure-3PSIDTS=sidts-CjEBSAxbGX6CiMV4Ex0XJKQrnt6VNT-4XJSeTsI6MtQZhB3TIXriFDEkFJt-SdlRte_TEAA; SIDCC=APoG2W-xLd4bRu03N3QaScGMEJLyEIoBW7_GUvU2hKld5ww11lJh36FzoZoHdvql0_ig-Sv_joun; __Secure-1PSIDCC=APoG2W9ExTLVGmxrYkUEYoE0IBwyPfCaT4H78xgEJzUVA8Ib2wpzzEjtsI7OTGXWT_-sUn2aMPTP; __Secure-3PSIDCC=APoG2W8ramXw7l0pFENqwpnrDtmytHpvpvDhk2CzlGDLyF740SL095p52TPIZjK4pn9mlqiBq2AY',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"116.0.5845.111"',
        'sec-ch-ua-full-version-list': '"Chromium";v="116.0.5845.111", "Not)A;Brand";v="24.0.0.0", "Google Chrome";v="116.0.5845.111"',
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'x-client-data': 'CJa2yQEIorbJAQipncoBCN/zygEIk6HLAQia/swBCIWTzQEIhaDNAQiZss0BCNy9zQEIu77NAQjgxM0BCO7EzQEItsjNAQjCyM0BCLnKzQEIw8rNAQi2y80BCNDLzQEIuM3NARjTnc0B',
    } # requests headers
    def __init__(self,keywords:list):
        """
               Initialize an instance of SearcResult.

               Args:
                   keywords (list): A list of keywords to search on YouTube.

               Attributes:
                   url (str): The URL of the YouTube search results page.
                   df (pd.DataFrame): A DataFrame to store channel information.
                   keywords (list): A list of keywords for YouTube search.
                   params (dict): Parameters for the YouTube search URL.
                   api_url (str): The URL for the YouTube search API.
                   api_cookies (dict): Cookies required for making API requests.
                   api_headers (dict): Headers for making API requests.
                   api_params (dict): Parameters for making API requests.
                   api_json_data (dict): JSON data for making API requests.

               Example:
                   instance = SearcResult(keywords=['keyword1', 'keyword2'])
               """
        self.url = 'https://www.youtube.com/results'
        self.df = self.create_csv()
        self.keywords = keywords
        self.params =  {'search_query': "",
                        'sp':'EgYIBBABGAM%3D'}
        self.api_url = 'https://www.youtube.com/youtubei/v1/search'
        self.api_cookies = {
            'VISITOR_INFO1_LIVE': 'LwaxKRZtIw8',
            'YSC': 'LNp1RoB5gPQ',
            'PREF': 'f4=4000000&tz=Asia.Calcutta&f5=30000&gl=US',
            'HSID': 'Al-_yPCzsbeMHkKqw',
            'SSID': 'AwF-IVorIOmUmFN2f',
            'APISID': 'HcIzNrsjSdCwtLKs/AJhmJZaw7MgypEgFY',
            'SAPISID': 'f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA',
            '__Secure-1PAPISID': 'f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA',
            '__Secure-3PAPISID': 'f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA',
            '_ga': 'GA1.1.778450163.1690521906',
            '_ga_2D63NQQFBG': 'GS1.1.1690521906.1.1.1690521936.0.0.0',
            'LOGIN_INFO': 'AFmmF2swRAIgQ_b64q3rQVEcR_I-snJwPgacWL2mpb0teMR5ynWJn8ECIE7HNGB68ztL78D7nJ7JOfLGTEMZJBgn_p789YbZiw8U:QUQ3MjNmeG1xYXJFR0hfUlVwUy0zdk04LU43UDFvN2ktNFFZRVRwMDNYYVRRWVJVUndLRU5pdW9sMUtmVW13V1NYZm9LaXBIQ200RXNuaE5QNEVvd3piRU5NRmtFVG91R01jNkV5bXJFQm5nWEdZcEgtMExhRGJsOVdfaHpMdlFPeGpIWUJzNkcxUExjYkdlVUdHR3NERlBIcjVNWXdFLTBrZTQ3aHptRHJLXzVlNUtZaGRzdk5KRWk5WXBQb2x4azhudHdzMTRMcnJnYkFRZDFPQm5oNUpxZDlLY0NTVS1CZw==',
            'SID': 'ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEXTaPg2WgwHI9KsAfdBmtYLA.',
            '__Secure-1PSID': 'ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEXCZnljh7L0qRwPWqF_ufN0A.',
            '__Secure-3PSID': 'ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEX5OSVeZJ-XsEWlVrYrg7n0A.',
            'VISITOR_PRIVACY_METADATA': 'CgJJThICGgA%3D',
            '__Secure-1PSIDTS': 'sidts-CjEBSAxbGRAFdjWn4AbVkwwvk2XDMS-z6MCaCz-es0B14e_eGbbrkPtaPcS4dFLEkqC1EAA',
            '__Secure-3PSIDTS': 'sidts-CjEBSAxbGRAFdjWn4AbVkwwvk2XDMS-z6MCaCz-es0B14e_eGbbrkPtaPcS4dFLEkqC1EAA',
            'SIDCC': 'APoG2W_lqIjUfaNMauI7GenyacQMSOVWVzV1oFUmd77tU7mxk--NaXhHMssNc34Uns3TnRYgq2au',
            '__Secure-1PSIDCC': 'APoG2W_t-6QkCAlWe5KNB6eXxSotLB20L_aI7vrMy58cqKlbEi__kl1MMjPpqhXm4RlpwQ2pl9sT',
            '__Secure-3PSIDCC': 'APoG2W8xctnNjFdRlvNoS3TDk4kQtk64a04-T8OR4Z87Wqp5YehRj_Hx5YhxkBhWumHeDhlMy6hQ',
        }
        self.api_headers = {
            'authority': 'www.youtube.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,ta;q=0.8,hi;q=0.7',
            'authorization': 'SAPISIDHASH 1693042325_0478f924f27de68c34e3ede1165d4f031e290655',
            'content-type': 'application/json',
            # 'cookie': 'VISITOR_INFO1_LIVE=LwaxKRZtIw8; YSC=LNp1RoB5gPQ; PREF=f4=4000000&tz=Asia.Calcutta&f5=30000&gl=US; HSID=Al-_yPCzsbeMHkKqw; SSID=AwF-IVorIOmUmFN2f; APISID=HcIzNrsjSdCwtLKs/AJhmJZaw7MgypEgFY; SAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; __Secure-1PAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; __Secure-3PAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; _ga=GA1.1.778450163.1690521906; _ga_2D63NQQFBG=GS1.1.1690521906.1.1.1690521936.0.0.0; LOGIN_INFO=AFmmF2swRAIgQ_b64q3rQVEcR_I-snJwPgacWL2mpb0teMR5ynWJn8ECIE7HNGB68ztL78D7nJ7JOfLGTEMZJBgn_p789YbZiw8U:QUQ3MjNmeG1xYXJFR0hfUlVwUy0zdk04LU43UDFvN2ktNFFZRVRwMDNYYVRRWVJVUndLRU5pdW9sMUtmVW13V1NYZm9LaXBIQ200RXNuaE5QNEVvd3piRU5NRmtFVG91R01jNkV5bXJFQm5nWEdZcEgtMExhRGJsOVdfaHpMdlFPeGpIWUJzNkcxUExjYkdlVUdHR3NERlBIcjVNWXdFLTBrZTQ3aHptRHJLXzVlNUtZaGRzdk5KRWk5WXBQb2x4azhudHdzMTRMcnJnYkFRZDFPQm5oNUpxZDlLY0NTVS1CZw==; SID=ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEXTaPg2WgwHI9KsAfdBmtYLA.; __Secure-1PSID=ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEXCZnljh7L0qRwPWqF_ufN0A.; __Secure-3PSID=ZggGZUF1Vd4zG74N_OfCYmG6y9QO_K4Zv0VZMmWYKGqQqPEX5OSVeZJ-XsEWlVrYrg7n0A.; VISITOR_PRIVACY_METADATA=CgJJThICGgA%3D; __Secure-1PSIDTS=sidts-CjEBSAxbGRAFdjWn4AbVkwwvk2XDMS-z6MCaCz-es0B14e_eGbbrkPtaPcS4dFLEkqC1EAA; __Secure-3PSIDTS=sidts-CjEBSAxbGRAFdjWn4AbVkwwvk2XDMS-z6MCaCz-es0B14e_eGbbrkPtaPcS4dFLEkqC1EAA; SIDCC=APoG2W_lqIjUfaNMauI7GenyacQMSOVWVzV1oFUmd77tU7mxk--NaXhHMssNc34Uns3TnRYgq2au; __Secure-1PSIDCC=APoG2W_t-6QkCAlWe5KNB6eXxSotLB20L_aI7vrMy58cqKlbEi__kl1MMjPpqhXm4RlpwQ2pl9sT; __Secure-3PSIDCC=APoG2W8xctnNjFdRlvNoS3TDk4kQtk64a04-T8OR4Z87Wqp5YehRj_Hx5YhxkBhWumHeDhlMy6hQ',
            'dnt': '1',
            'origin': 'https://www.youtube.com',
            'referer': 'https://www.youtube.com/results?search_query=i+phone+14&sp=EgYIBBABGAM%253D',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"116.0.5845.111"',
            'sec-ch-ua-full-version-list': '"Chromium";v="116.0.5845.111", "Not)A;Brand";v="24.0.0.0", "Google Chrome";v="116.0.5845.111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'same-origin',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'x-client-data': 'CJa2yQEIorbJAQipncoBCN/zygEIk6HLAQia/swBCIWTzQEIhaDNAQiZss0BCNy9zQEIu77NAQjgxM0BCO7EzQEItsjNAQjCyM0BCLnKzQEIw8rNAQi2y80BCNDLzQEIuM3NARjTnc0B',
            'x-goog-authuser': '0',
            'x-goog-pageid': '106882159830204922769',
            'x-goog-visitor-id': 'CgtMd2F4S1JadEl3OCiHjaenBjIICgJJThICGgA%3D',
            'x-origin': 'https://www.youtube.com',
            'x-youtube-bootstrap-logged-in': 'true',
            'x-youtube-client-name': '1',
            'x-youtube-client-version': '2.20230824.06.00',
        }
        self.api_params = {
            'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
            'prettyPrint': 'false',
        }
        self.api_json_data = {
            'context': {
                'client': {
                    'hl': 'en',
                    'gl': 'US',
                    'remoteHost': '103.172.89.201',
                    'deviceMake': '',
                    'deviceModel': '',
                    'visitorData': 'CgtMd2F4S1JadEl3OCiHjaenBjIICgJJThICGgA%3D',
                    'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36,gzip(gfe)',
                    'clientName': 'WEB',
                    'clientVersion': '2.20230824.06.00',
                    'osName': 'Windows',
                    'osVersion': '10.0',
                    'originalUrl': 'https://www.youtube.com/results?search_query=i+phone+14&sp=EgYIBBABGAM%253D',
                    'screenPixelDensity': 2,
                    'platform': 'DESKTOP',
                    'clientFormFactor': 'UNKNOWN_FORM_FACTOR',
                    'configInfo': {
                        'appInstallData': 'CIeNp6cGEOLUrgUQjMuvBRDH5q8FEIjYrwUQ3eOvBRCF2f4SEOSz_hIQ65OuBRC7zP4SELTJrwUQuIuuBRDV5a8FEMLe_hIQgaWvBRCI468FEJjPrwUQ4-avBRDqw68FEOno_hIQ3ej-EhCU2f4SEMzfrgUQ1KGvBRCJ6K4FEOzYrwUQrLevBRClwv4SEMyu_hIQpN6vBRDE3a8FENuvrwUQtaavBRDuoq8FEL22rgUQ-r6vBRDyqK8FEOe6rwUQ2cmvBRCc6f4SEMXWrwU%3D',
                    },
                    'screenDensityFloat': 1.5,
                    'timeZone': 'Asia/Calcutta',
                    'browserName': 'Chrome',
                    'browserVersion': '116.0.0.0',
                    'acceptHeader': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'deviceExperimentId': 'ChxOekkzTVRVMk1UTTFOalkxT1RBeE16QTROdz09EIeNp6cGGIeNp6cG',
                    'screenWidthPoints': 750,
                    'screenHeightPoints': 571,
                    'utcOffsetMinutes': 330,
                    'userInterfaceTheme': 'USER_INTERFACE_THEME_LIGHT',
                    'connectionType': 'CONN_CELLULAR_4G',
                    'memoryTotalKbytes': '8000000',
                    'mainAppWebInfo': {
                        'graftUrl': 'https://www.youtube.com/results?search_query=i+phone+14&sp=EgYIBBABGAM%253D',
                        'pwaInstallabilityStatus': 'PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED',
                        'webDisplayMode': 'WEB_DISPLAY_MODE_BROWSER',
                        'isWebNativeShareAvailable': True,
                    },
                },
                'user': {
                    'lockedSafetyMode': False,
                },
                'request': {
                    'useSsl': True,
                    'internalExperimentFlags': [
                        {
                            'key': 'force_enter_once_in_webview',
                            'value': 'true',
                        },
                    ],
                    'consistencyTokenJars': [],
                },
                'clickTracking': {
                    'clickTrackingParams': 'CDoQt6kLGAQiEwjR1d6MgvqAAxVQ3TgGHZCfDRo=',
                },
                'adSignalsInfo': {
                    'params': [
                        {
                            'key': 'dt',
                            'value': '1693042314564',
                        },
                        {
                            'key': 'flash',
                            'value': '0',
                        },
                        {
                            'key': 'frm',
                            'value': '0',
                        },
                        {
                            'key': 'u_tz',
                            'value': '330',
                        },
                        {
                            'key': 'u_his',
                            'value': '3',
                        },
                        {
                            'key': 'u_h',
                            'value': '720',
                        },
                        {
                            'key': 'u_w',
                            'value': '1280',
                        },
                        {
                            'key': 'u_ah',
                            'value': '680',
                        },
                        {
                            'key': 'u_aw',
                            'value': '1280',
                        },
                        {
                            'key': 'u_cd',
                            'value': '24',
                        },
                        {
                            'key': 'bc',
                            'value': '31',
                        },
                        {
                            'key': 'bih',
                            'value': '571',
                        },
                        {
                            'key': 'biw',
                            'value': '733',
                        },
                        {
                            'key': 'brdim',
                            'value': '0,0,0,0,1280,0,1280,680,750,571',
                        },
                        {
                            'key': 'vis',
                            'value': '1',
                        },
                        {
                            'key': 'wgl',
                            'value': 'true',
                        },
                        {
                            'key': 'ca_type',
                            'value': 'image',
                        },
                    ],
                    'bid': 'ANyPxKrwLzXdzlfR4e0TD23rhQ9hDVuZXHtHHG5dBxmA-SFVtFOicmz5gUBDL-eS088laInYloF1GuMetkA2y2qSLu7Lyb34qw',
                },
            },
            'continuation': 'EqADEglpcGhvbmUgMTQakgNFZ1lJQkJBQkdBTklGSUlCQzBrMVRVd3lVME4xUlhkUmdnRUxUbkp5YUhCcWJsTmFkMFdDQVF0d05HUjNWVzB3WDAxT1o0SUJDM2xJUW10aFlVY3RRbHB6Z2dFTFJVeHVOWE53YkdGMldsV0NBUXQ0WlRWNVVYWm9kRUphVVlJQkMxZzVaRUV4YXpCUllVSTBnZ0VMUTB0MGEyZHhNMXBpTFZtQ0FRdFZlRU5EVGpOSGVXcG5kNElCQzNSd1JWOWtTbTFhTUVoM2dnRUxiVGRzVUdrNWNtcFBWa21DQVF0T1lrVlBjMUJMY2taR1k0SUJDMk5YWjJZMlVIcEJZVnBSZ2dFTFFUWk1jRGhRZHpaS2VFV0NBUXR4TW0xb2VFUmhVRE41YTRJQkMxUjNja2xmV1RsdGFYUkZnZ0VMU2xOQlVsaERkSFZ6YWsyQ0FRdFNjbTR5WTFKUllWWXlTWUlCQzJWa1JXRmpjek5YT0VKSmdnRUxTMjVGUnpSSVEzUkRNV3V5QVFZS0JBZ1hFQUklM0QYgeDoGCILc2VhcmNoLWZlZWQ%3D',
        }
        self.main()
    # search keywords on YouTube

    def search(self)->tuple:
        """
                Perform a search on YouTube for each keyword in the list and yield pagination tokens.

                This method iterates through the list of keywords, performs a search on YouTube,
                extracts pagination tokens from the search results, and yields a tuple containing
                the pagination token and the keyword. These tokens can be used to load additional
                search results.

                Yields:
                    Tuple[str, str]: A tuple containing the pagination token and the keyword.

                """
        for keyword in self.keywords:
            self.params['search_query'] = keyword
            response = requests.get(self.url,params=self.params,
                headers=self.HEADERS,cookies=self.COOKIES)
            soup = BeautifulSoup(response.text,'lxml')
            try:
                script_tag = soup.find('script', string=re.compile('var ytInitialData =.*'))
                json_object = re.search('=\s(\{.*\});</script>', str(script_tag), re.M).group(1)
                channel_details = json.loads(json_object)
                contents = channel_details['contents']['twoColumnSearchResultsRenderer'][
                          'primaryContents']['sectionListRenderer']['contents']
            except Exception as e:
                contents = []
                print(e)
            for content in contents[:-1]:
                try:
                    all_channels = content['itemSectionRenderer']['contents']
                    channel_relative_link = [ channel['videoRenderer']['ownerText'][
                        'runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']
                            ['url'] for channel in all_channels

                    ]
                except Exception as e:
                    channel_relative_link = []
                    print(e)
            try:
                token = contents[-1]['continuationItemRenderer'][
                'continuationEndpoint']['continuationCommand']['token']
            except Exception as e:
                token = ''
                print(e)
            yield token,keyword

    # collect channel id and channel name
    def get_channels(self,token:str,keyword:str)->None:
        """
              Retrieve channel information from YouTube search results using dynamic pagination.

              This method sends a POST request to the YouTube API to fetch additional search results
              using a pagination token. It extracts channel information from the response and saves
              it to a CSV file. The process continues until there are no more search results.

              Args:
                  token (str): The pagination token for fetching more search results.
                  keyword (str): The keyword for which the search results are obtained.

              Returns:
                  None"""
        self.api_json_data['continuation'] = token # loading token
        response = requests.post(self.api_url,params=self.api_params,headers=self.api_headers,
                                 cookies=self.api_cookies,json=self.api_json_data)
        if response.status_code == 200: # checks response
            search_results = json.loads(response.text)
            try:
                all_channels = search_results['onResponseReceivedCommands'][0]['appendContinuationItemsAction'][
                'continuationItems'][0]['itemSectionRenderer']['contents']
            except:
                all_channels = []
            try:
                channel_relative_links = [self.save_csv(channel['videoRenderer']['ownerText'][
                            'runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']
                                ['url'],keyword) for channel in all_channels]
            except:
                channel_relative_links = []
            try:
                token =  search_results['onResponseReceivedCommands'][0]['appendContinuationItemsAction'][
                'continuationItems'][1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
            except :
                token = ''
                try:
                    no_more_results = search_results['onResponseReceivedCommands'][0]['appendContinuationItemsAction'][
                    'continuationItems'][0]['itemSectionRenderer']['contents'][0]['messageRenderer']['text']['runs'][
                        0]['text']
                    if no_more_results:
                        print(no_more_results)
                except:
                    no_more_results =''
        else:
            print(response.status_code)

        if token:
            # dynamic pagination
            self.get_channels(token,keyword)
        else:
            # finished  token scraping
            pass

    # create or load channels.csv inside the data directory
    def create_csv(self)->pd.DataFrame:
        """
        Create or load a CSV file named 'channels.csv' in the 'data' directory.

        This function first checks if the 'channels.csv' file already exists in the 'data' directory.
        If it doesn't exist, it creates a new DataFrame with specified columns and saves it as 'channels.csv'.
        If the file already exists, it reads its content and returns it as a DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing channel information with columns:
                - 'keywords'
                - 'urls'
                - 'channel name'
                - 'channel id'
                - 'subscribers'
                - 'response'
                - 'email'
                - 'email id'
                - 'whatsapp'
                - 'contact'
                - 'income'

        Example:
            df = create_csv()
            # Use the DataFrame 'df' for further operations.
        """
        csv_file_path = 'data/channels.csv'

        # Check if the 'channels.csv' file already exists
        if not os.path.exists(csv_file_path):
            # Create a DataFrame with the specified columns
            df = pd.DataFrame(columns=[
                'keywords', 'urls', 'channel name', 'channel id',
                'subscribers', 'response', 'email', 'email id',
                'whatsapp', 'contact', 'income'
            ])
            # Save the DataFrame as a CSV file
            df.to_csv(csv_file_path, index=False)
        else:
            # Read the existing CSV file and return its content as a DataFrame
            df = pd.read_csv(csv_file_path)

        return df
    # to store the data in to csv

    def save_csv(self, channel_id: str,keyword:str) -> None:
        """
               Save channel information to a CSV file while checking for duplicates.

               This method takes a channel ID and a keyword, creates a dictionary with the channel's
               information, and stores it in a DataFrame. It checks if the channel ID already exists in
               the DataFrame to prevent duplicates and then appends the data to the CSV file.

               Args:
                   channel_id (str): The unique identifier of the YouTube channel.
                   keyword (str): The keyword associated with the channel.

               Returns:
                   None
               """
        channel_dic = {
            'keywords': keyword,
            'urls': self.url.replace('/results','') + f'{channel_id}/videos',
            'channel id': channel_id,

        }
        df = pd.DataFrame([channel_dic])  # Create a single-row DataFrame with the channel's data
        # Check for duplicates based on 'channel id'
        if not ( (self.df['channel id'] == channel_id)).any():
            # Append the new data row to the existing DataFrame, ensuring a sequential index
            self.df = pd.concat([self.df, df], ignore_index=True)
        # Save the updated DataFrame to the 'channels.csv' file without including the row numbers (index)
        csv = self.df.to_csv('data\channels.csv', index=False)

    # starts scraping process
    def main(self)->None:
        '''this method starts scraping process by calling the
        search() method '''
        for token,keyword in self.search():
            self.get_channels(token,keyword)



    #Note:
    # while iteratiting over the content list in search method.(content have three or data in it.. if
    # ad presents 3 , no ad 2 -> last one is always continuation token -> have to face if not last
    # one is token. )
    # search result faces two exception like "itemSectionRenderer",and "videoRenderer"
    # when ever the search result page have the ad in it
    # if new error comes we have to consider about it.