'''importing required modules'''
import json
import re
from time import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from channels_csv import  UpdateCsv
from filter_ import  Filter_



class VideoInfo:
    ''' it filters the youtube channels by applying
    few filters and updates the filtered channels in to csv'''
    def __init__(self):
        """
            Initialize the scraping process by setting up headers,
             cookies, API URL, and parameters.
        """
        self.df = pd.read_csv('data/channels.csv')
        self.HEADERS = {
            'authority': 'www.youtube.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            # 'cookie': 'VISITOR_INFO1_LIVE=zyQT-hhFXD4; VISITOR_PRIVACY_METADATA=CgJJThICGgA%3D; PREF=f4=4000000&tz=Asia.Calcutta; YSC=tzPD1-Hy06w; GPS=1',
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
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'x-client-data': 'CJa2yQEIorbJAQipncoBCN/zygEIlqHLAQia/swBCIWTzQEIhaDNAQiZss0BCNy9zQEIu77NAQjgxM0BCO/EzQEIwsjNAQi5ys0BCMPKzQEItsvNAQjQy80BCLjNzQEIk8/NARjTnc0B',
        } # requests header
        self.COOKIES = {
            'VISITOR_INFO1_LIVE': 'zyQT-hhFXD4',
            'VISITOR_PRIVACY_METADATA': 'CgJJThICGgA%3D',
            'PREF': 'f4=4000000&tz=Asia.Calcutta',
            'YSC': 'tzPD1-Hy06w',
            'GPS': '1',
        } # requests cookies
        self.api_url = 'https://www.youtube.com/youtubei/v1/browse'
        # Define API request cookies
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
            'VISITOR_PRIVACY_METADATA': 'CgJJThICGgA%3D',
            'SID': 'aQgGZSWNrwy8ajUHfL9TJEVkmT4J2sXfUmdgHjfyxQ66MNCD5ch0drho-0yw3ahxibUVKg.',
            '__Secure-1PSID': 'aQgGZSWNrwy8ajUHfL9TJEVkmT4J2sXfUmdgHjfyxQ66MNCDMbihvMQ4czyncC-_WZwLlA.',
            '__Secure-3PSID': 'aQgGZSWNrwy8ajUHfL9TJEVkmT4J2sXfUmdgHjfyxQ66MNCDukeaJZN5mh_fOSbeLI1rPA.',
            '__Secure-1PSIDTS': 'sidts-CjEBSAxbGZ08KoktW3MRJUgVcnKrTmixAE215eNLmixBDvCW05rxa8yYpwDLLGsY_oYBEAA',
            '__Secure-3PSIDTS': 'sidts-CjEBSAxbGZ08KoktW3MRJUgVcnKrTmixAE215eNLmixBDvCW05rxa8yYpwDLLGsY_oYBEAA',
            'SIDCC': 'APoG2W82CzhMy6u82dTlO2WshNPGiyjDyDWRZxaEqWt-neQgGeksTZdXqQfs67UeehCm_4005xY-',
            '__Secure-1PSIDCC': 'APoG2W8oAQRaIEeML63dyF6QfA6lR7Dw4BM74O0rfCdH0hfEvsOCwIoMLCfZKH-gnvnjw1or98zl',
            '__Secure-3PSIDCC': 'APoG2W_ApwLx8HprdAzLRbsrInJSI8R40BrPRWKypHcVXc0wH0s6pxoKK5AmNn8HZnHsYWU9ESBa',
        }
        # Define API request headers
        self.api_headers = {
            'authority': 'www.youtube.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,ta;q=0.8,hi;q=0.7',
            'authorization': 'SAPISIDHASH 1693475612_dd818fbbc60e5b180814bc74d85d9359d041acdd',
            'content-type': 'application/json',
            # 'cookie': 'VISITOR_INFO1_LIVE=LwaxKRZtIw8; YSC=LNp1RoB5gPQ; PREF=f4=4000000&tz=Asia.Calcutta&f5=30000&gl=US; HSID=Al-_yPCzsbeMHkKqw; SSID=AwF-IVorIOmUmFN2f; APISID=HcIzNrsjSdCwtLKs/AJhmJZaw7MgypEgFY; SAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; __Secure-1PAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; __Secure-3PAPISID=f7rsMB9wM29L1g1T/AvHV0xPXVgLFOTAqA; _ga=GA1.1.778450163.1690521906; _ga_2D63NQQFBG=GS1.1.1690521906.1.1.1690521936.0.0.0; LOGIN_INFO=AFmmF2swRAIgQ_b64q3rQVEcR_I-snJwPgacWL2mpb0teMR5ynWJn8ECIE7HNGB68ztL78D7nJ7JOfLGTEMZJBgn_p789YbZiw8U:QUQ3MjNmeG1xYXJFR0hfUlVwUy0zdk04LU43UDFvN2ktNFFZRVRwMDNYYVRRWVJVUndLRU5pdW9sMUtmVW13V1NYZm9LaXBIQ200RXNuaE5QNEVvd3piRU5NRmtFVG91R01jNkV5bXJFQm5nWEdZcEgtMExhRGJsOVdfaHpMdlFPeGpIWUJzNkcxUExjYkdlVUdHR3NERlBIcjVNWXdFLTBrZTQ3aHptRHJLXzVlNUtZaGRzdk5KRWk5WXBQb2x4azhudHdzMTRMcnJnYkFRZDFPQm5oNUpxZDlLY0NTVS1CZw==; VISITOR_PRIVACY_METADATA=CgJJThICGgA%3D; SID=aQgGZSWNrwy8ajUHfL9TJEVkmT4J2sXfUmdgHjfyxQ66MNCD5ch0drho-0yw3ahxibUVKg.; __Secure-1PSID=aQgGZSWNrwy8ajUHfL9TJEVkmT4J2sXfUmdgHjfyxQ66MNCDMbihvMQ4czyncC-_WZwLlA.; __Secure-3PSID=aQgGZSWNrwy8ajUHfL9TJEVkmT4J2sXfUmdgHjfyxQ66MNCDukeaJZN5mh_fOSbeLI1rPA.; __Secure-1PSIDTS=sidts-CjEBSAxbGZ08KoktW3MRJUgVcnKrTmixAE215eNLmixBDvCW05rxa8yYpwDLLGsY_oYBEAA; __Secure-3PSIDTS=sidts-CjEBSAxbGZ08KoktW3MRJUgVcnKrTmixAE215eNLmixBDvCW05rxa8yYpwDLLGsY_oYBEAA; SIDCC=APoG2W82CzhMy6u82dTlO2WshNPGiyjDyDWRZxaEqWt-neQgGeksTZdXqQfs67UeehCm_4005xY-; __Secure-1PSIDCC=APoG2W8oAQRaIEeML63dyF6QfA6lR7Dw4BM74O0rfCdH0hfEvsOCwIoMLCfZKH-gnvnjw1or98zl; __Secure-3PSIDCC=APoG2W_ApwLx8HprdAzLRbsrInJSI8R40BrPRWKypHcVXc0wH0s6pxoKK5AmNn8HZnHsYWU9ESBa',
            'dnt': '1',
            'origin': 'https://www.youtube.com',
            'referer': 'https://www.youtube.com/@WindiesCricket/videos',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"116.0.5845.140"',
            'sec-ch-ua-full-version-list': '"Chromium";v="116.0.5845.140", "Not)A;Brand";v="24.0.0.0", "Google Chrome";v="116.0.5845.140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'same-origin',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'x-client-data': 'CJa2yQEIorbJAQipncoBCN/zygEIkqHLAQia/swBCIWTzQEIhaDNAQiZss0BCNy9zQEIu77NAQjgxM0BCMLIzQEIucrNAQjDys0BCLbLzQEI0MvNAQi4zc0BCJPPzQEY053NAQ==',
            'x-goog-authuser': '0',
            'x-goog-pageid': '106882159830204922769',
            'x-goog-visitor-id': 'CgtMd2F4S1JadEl3OCiPxsGnBjIICgJJThICGgA%3D',
            'x-origin': 'https://www.youtube.com',
            'x-youtube-bootstrap-logged-in': 'true',
            'x-youtube-client-name': '1',
            'x-youtube-client-version': '2.20230829.01.02',
        }
        # Define API request params
        self.api_params = {
            'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
            'prettyPrint': 'false',
        }
        # Define API request JSON data
        self.api_json_data = {
            'context': {
                'client': {
                    'hl': 'en',
                    'gl': 'US',
                    'remoteHost': '103.172.89.195',
                    'deviceMake': '',
                    'deviceModel': '',
                    'visitorData': 'CgtMd2F4S1JadEl3OCiPxsGnBjIICgJJThICGgA%3D',
                    'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36,gzip(gfe)',
                    'clientName': 'WEB',
                    'clientVersion': '2.20230829.01.02',
                    'osName': 'Windows',
                    'osVersion': '10.0',
                    'originalUrl': 'https://www.youtube.com/@WindiesCricket/videos',
                    'screenPixelDensity': 2,
                    'platform': 'DESKTOP',
                    'clientFormFactor': 'UNKNOWN_FORM_FACTOR',
                    'configInfo': {
                        'appInstallData': 'CI_GwacGELiLrgUQieiuBRD6vq8FEMyu_hIQ8qivBRCI2K8FEOuTrgUQ2cmvBRDqw68FEOe6rwUQhdn-EhC0ya8FEKXC_hIQ-uT-EhDV5a8FEKTerwUQ0-GvBRCXz68FEIGlrwUQu8z-EhDE3a8FEL22rgUQwt7-EhCst68FEJTZ_hIQ5LP-EhDV6q8FEJbn_hIQg9-vBRDj5q8FENuvrwUQ7NivBRCMy68FEOLUrgUQ6-j-EhDH5q8FEMzfrgUQ7qKvBRDUoa8FEIjjrwUQtaavBRDd6P4SEOno_hIQ3eOvBRDF1q8FEJzp_hI%3D',
                    },
                    'screenDensityFloat': 1.5,
                    'timeZone': 'Asia/Calcutta',
                    'browserName': 'Chrome',
                    'browserVersion': '116.0.0.0',
                    'acceptHeader': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'deviceExperimentId': 'ChxOekkzTXpReU1qTXhOVGcwTXpRNU56QTJPUT09EI_GwacGGI_GwacG',
                    'screenWidthPoints': 190,
                    'screenHeightPoints': 571,
                    'utcOffsetMinutes': 330,
                    'userInterfaceTheme': 'USER_INTERFACE_THEME_LIGHT',
                    'connectionType': 'CONN_CELLULAR_4G',
                    'memoryTotalKbytes': '8000000',
                    'mainAppWebInfo': {
                        'graftUrl': 'https://www.youtube.com/@WindiesCricket/videos',
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
                    'clickTrackingParams': 'CC0Q8eIEIhMI8r64nNCGgQMVJL1WAR2OgQcQ',
                },
                'adSignalsInfo': {
                    'params': [
                        {
                            'key': 'dt',
                            'value': '1693475601422',
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
                            'value': '173',
                        },
                        {
                            'key': 'brdim',
                            'value': '0,0,0,0,1280,0,1280,680,190,571',
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
                    'bid': 'ANyPxKpiclzmTOjnw2UAYUlF13oAoHJ9HSN7lx3YYRX8aoOPcneW7I8JB6CPPRizo-nunaCVpc7D6DB7yVPuVL3t1LWSolzNxw',
                },
            },
            'continuation': '4qmFsgK1ChIYVUMyTUhUT1hrdGZUSzI2YURLeVFzM2NRGpgKOGdiT0J4ckxCM3JJQndyREJ3cWFCME55UVVaRFoxSnBXRE5TY2tWeFkwWkJVMnhtWlRkU2JWZGlTUzEyUlVFeE5EVklabnBCTlZJMU56aHRlazQzTW5RMmVreHpWa2hMV1RBMVEzQTNUbEJOTFZOdGNWazNURnBCWldsSGVWQndWa1l6WWxBMVgycFZURkEzVERWaE1HSkZOVUZIUlZoQ01uTmlZVVpUUW5wR00xcFBWWGRKZEhoU05FNXFNSFl3ZURSNFIzSjZYMjlCZFRsd2JrRkxObEF5Y1dnelNXNUpkMHQ0VFZWRVJHVlNka2w0VFdKSmRtaG9jVFJKYlROck1sZGZXakl3TTJoblVWaHVZbEpvY2tGaVl6SjJNbXg1YTJseGFEY3hPSGhoYmt0bmJqSkNOemRyV0V4c2R6SmxiVkkxTWpNMVRYbEtXVkIxVG5KTU1GSlNXR2R2VjNSeWFVZE5OVzFIYVRCNWR6QnRNVE0wWmxoZmFsSnhVamx6UjBsNFVHMDJObnBoTkhkRVpVazBjWHB3U1hGWE9HaFZRMGw1Ylcwd1dtRnVNelZsYm5OWmJVWXhTMHBoU1ZKdVoydFFOakp1TFdGcFZVeEVaVlZKU0hJdFNTMUdXamwzZDJacWFtNURkREpNV0ZOTVZWSnhNSFY2VURoWlVFVXdPWEYxYlhGTk9HaENMVFZRTm1VMk1sTTFhR0Y0ZWtkaU0yZEJjVkJpZUhZdE5XdGxibXcxYWsxeGN6SnVUVGRzY1hwemNUZEtlSGRYVjI5eE1rWnRYMWRHTFZsRlFtaHhkME5WZHpocFpYSTNXalZxTjNwaFEwWnZURGMxYkRNNWRYTktZVTluYzJoMFIxSTBRbFIzTVc5V05uZFlSM1oxUW0wdFRVOTNSM1pRZFVKdWNWcE9iM2xIUjB4SlgwcFRkMHBsVTIxUmJESndPRzE1YVc0dE4yRnZVRTUzWTBsemNHRk1XR3hyTkZFMVNsbFJZbmx5TTJkYU1VSkNOa05mVUU1VFdWSlFNMDQyYkRSTmFXTnlhbVJhTWxCTVRHSlZSblZsZFUxTFJ6UldXRTlKU0hNM1EyaG5aM1pEVjBzMFdFUndhR05YVXpaVmNFRXhVVTVNWVdSU1lXODNZemxYTTJKTVNtOTRhVkpRTVZndFJuSlVZVVZaYlhZMFduVlNhVk51YW1GS1VHSmthV0YzTmtaM2NVbFZMVE54VTNGUmVrdFVTMlpYTVc4MFVsVkxNWEpXUnpWa1EwVlpWRGx1YlhKa00xbHlMVTEyT0d0UFpXNUhWR2t3Tms1VlJERkhaVGxHZFZZek9FcDBOVmN0TlZCRVZtazJkMWRwVjBnemJGVk9jakZhUlZsdlJGVjBlbW80YkZoUVNFbHVPSFZDV2xWcVZWaEdVekpPVmxsaFl6TjJWaTA1WmpsVlNXNU1hR2w0Y2tOVVN6WndRblJuYkZKa2RFOXBWalJoUjNoSE0yWnJha1ZVYm5CRVYwTjBSVGREWkUxelRVOXdOa1J1Y25CTVYySXdOVFZ4UjJoWmRrWktTVEpIZW5wVWVVc3pUMEpGVVZaSldYZHpXV2hCZVhoQ015MU9SRlZZUW5aQlQzQnlMVmR5UTB0dFEyeG9XVTFyTkVzNE1FcDJRekZCZUdjU0pEWTBaamczWW1ZM0xUQXdNREF0TWpFNFpTMWhNR1prTFRFME1qSXpZbUpoWldSbFpSZ0I%3D',
        }
        self.send_request() # initializing scraping process by sending a request
    def clean_subscribers(self, subscriber_count: str) -> float:
        """
        Clean and convert subscriber count from string to float, considering 'K' (thousands) and 'M' (millions) suffixes.

        This method performs the following tasks:

        1. Stores suffix-to-multiplier mappings for 'M', 'K', 'million', and 'k'.
        2. Iterates through the mappings and checks if any suffix is present in the subscriber count.
        3. If a suffix is found, removes it from the subscriber count string and converts the result to float, multiplying it by the appropriate multiplier.
        4. If no suffix is found, directly converts the subscriber count string to float.
        5. Returns the cleaned and converted subscriber count as a float.

        Args:
            subscriber_count (str): Subscriber count as a string, possibly containing 'K' or 'M' suffixes.

        Returns:
            float: The cleaned and converted subscriber count as a float.
        """
        # Define suffix-to-multiplier mappings for 'M', 'K', 'million', and 'k'.
        suffix_multiplier = {
            'M': 1000000,
            'K': 1000,
            'million': 1000000,
            'k': 1000
        }

        # Iterate through each mapping and check for the presence of the suffix in the subscriber_count.
        for suffix, multiplier in suffix_multiplier.items():
            if suffix in subscriber_count:
                # Remove the suffix from the subscriber_count string.
                subscriber_count = subscriber_count.replace(suffix, '')
                # Convert the result to float and multiply by the appropriate multiplier.
                return float(subscriber_count) * multiplier

        # If no suffix is found, directly convert the subscriber_count to float and return.
        return float(subscriber_count)
    def get_videos_details(self, videoinfo: list, url: str) -> tuple:
        """
        Retrieve video details from YouTube channel, including titles, timestamps, views count, and video ID.

        This method performs the following tasks:

        1. Extracts video titles from the provided video information.
        2. Retrieves video timestamps, handling the situation for upcoming videos.
        3. Extracts video views count and handles exceptions, including handling upcoming videos.
        4. Calculates the approximate income for the last 30 days based on view counts.
        5. Returns the extracted video details as a tuple.

        Args:
            videoinfo (list): List of video information to process.
            url (str): The URL of the YouTube channel.

        Returns:
            tuple: A tuple containing titles, video timestamps, video ID, and approximate income.
        """
        titles = []  # to store all the titles of the videos
        video_time_stamps = []  # to store all the timestamps of the videos
        pulished_time_and_views = []  # to store all the video view counts
        videoinfo = videoinfo[:-1] if len(videoinfo) >= 30 else videoinfo[:]

        def check_upcoming_event(e):
            upcoming_event = info['richItemRenderer']['content']['videoRenderer']['upcomingEventData']
            if upcoming_event:
                print('Video has no views count or timestamp since it is an upcoming video')
            else:
                print(e, url)

        for info in videoinfo:
            try:
                # Extract the video title from the video information
                video_title = info['richItemRenderer']['content']['videoRenderer']['title']['runs'][0]['text']
                titles.append(video_title)
            except Exception as e:
                print(e, url)
            try:
                # Extract the video timestamp from the video information
                time_stamp = info['richItemRenderer']['content']['videoRenderer']['publishedTimeText']['simpleText']
                video_time_stamps.append(time_stamp)
            except Exception as e:
                check_upcoming_event(e)
            try:
                # Extract the video views count from the video information
                views = info['richItemRenderer']['content']['videoRenderer']['viewCountText']['simpleText']
                view_counts = re.sub(r'views?|no|,', lambda match: "0" if match.group() == "No" else '', views,
                                     flags=re.I)
                pulished_time_and_views.append((view_counts, time_stamp))
            except Exception as e:
                # If an error occurs, print an error message along with the problematic video information
                check_upcoming_event(e)
            try:
                # Extract the video URLs from the video information
                video_id = videoinfo[0]['richItemRenderer']['content']['videoRenderer']['videoId']
            except:
                video_id = ''

        # Calculate the last 30 days income of the channel based on view counts
        last_30_day_views = sum([int(view) for view, stamp in pulished_time_and_views if not 'month' in stamp])
        approx_income = (last_30_day_views / 1000) * 80

        return titles, video_time_stamps, video_id, f'{approx_income:.2f}'
    def check_videos_count(self, content:list, token:str) -> list:
        """
        Check the count of scraped videos and fetch additional pages if necessary.

        This method performs the following tasks:

        1. Checks the count of videos in the current content.
        2. If the count is less than 30 and a token is available, requests and processes additional pages.
        3. Limits the total number of videos to 31 to analyze the channel's recent data,

        Args:
            content (list): A list of video content data.
            token (str): A token for pagination, if available.

        Returns:
            list: A modified list of video content data, including videos from additional pages if fetched.
        """
        # Check if the current content contains fewer than 30 videos and a pagination token is available.
        if (len(content) < 30) and (token):
            # Remove the last item from content to avoid duplicates.
            content = content[:-1]

            # Send an HTTP POST request to fetch additional pages using the specified API parameters.
            new_response = requests.post(
                self.api_url,
                params=self.api_params,
                cookies=self.api_cookies,
                headers=self.api_headers,
                json=self.api_json_data,
            )

            # Parse the JSON content of the new response.
            json_content = json.loads(new_response.text)

        try:
            # Extract video content from the next page, if available.
            next_page_content = json_content['onResponseReceivedActions'][0]['appendContinuationItemsAction'][
                'continuationItems']
        except:
            # Handle exceptions if the next page content is not available.
            next_page_content = []

        # Combine the current content with videos from the next page.
        content = content + next_page_content

        # Limit the total number of videos to 31 for analyzing recent data.
        content = content[:31]

        return content
    def process_urls(self,url:str)->None:
        """
           Process a URL, retrieve and analyze data, and update CSV records.

           Args:
               url (str): The URL to process.

           This method performs the following tasks:

           1. Sends an HTTP GET request to the provided URL with specified headers and cookies.
           2. Checks if the requested URL matches the final URL (no redirects) and if there are no redirections.
           3. Stores the HTTP response status code and URL in a CSV file for record-keeping.
           4. Parses the HTML content of the response using BeautifulSoup.
           5. Extracts data, including:
              - Subscriber count
              - Video timestamps
              - Video IDs
              - Income information
           6. Updates the subscriber count in the CSV file.
           7. Checks video counts and retrieves video details.
           8. Filters the results based on specific criteria.
           9. Performs an email check and updates the CSV file with email IDs and contact details of the channel, if available.

           Returns:
               None
           """
        # Send an HTTP GET request to the provided URL with headers and cookies.
        response = requests.get(url, headers=self.HEADERS, cookies=self.COOKIES)
        # Check if the requested URL matches the final URL (no redirects) and if there are no redirections.
        if (url == response.url) & (not response.history):
            # Store the HTTP response status code and URL in a CSV file.
            UpdateCsv().store_response(response.status_code,url,self.df)
            # Parse the HTML content of the response using BeautifulSoup.
            soup = BeautifulSoup(response.text, 'lxml')

            try:
                # Find the script tag containing 'var ytInitialData' and extract JSON data.
                script_tag = soup.find('script', string=re.compile('var ytInitialData =.*'))
                json_object = re.search('=\s(\{.*\});</script>', str(script_tag), re.M).group(1)
                video_info_dic = json.loads(json_object)

                # Extract video content data.
                content = video_info_dic['contents']['twoColumnBrowseResultsRenderer']['tabs'][1][
                    'tabRenderer']['content']['richGridRenderer']['contents']
            except Exception as e:
                # Handle exceptions and log the error along with the URL.
                video_info_dic = ''
                print(e,url)
                content = []

            try:
                # Extract a token for pagination, if available.
                token = content[-1]['continuationItemRenderer']['continuationEndpoint'][
                    'continuationCommand']['token']
            except:
                token = ''

            try:
                # Extract the subscriber count from video_info_dic.
                subscribers_count = video_info_dic['header']['c4TabbedHeaderRenderer'][
                    'subscriberCountText']['accessibility']['accessibilityData']['label'].replace(
                        'subscribers',''
                    ).replace('subscriber','')

                # Update the subscriber count in the CSV.
                subscribers_count = self.clean_subscribers(subscribers_count)
                UpdateCsv().update_subscribers(self.df,url,subscribers_count)
            except:
                subscribers_count = float(0)
                UpdateCsv().update_subscribers(self.df,url,subscribers_count)

            # Check videos count and get video details.
            all_contents = self.check_videos_count(content,token)
            titles, timestamps,video_id,income = self.get_videos_details(all_contents, url)

            # Filter the results and get the filter_result.
            filter_result = Filter_(self.df,video_id,timestamps,url).result
            # Perform an email check and update the CSV.
            UpdateCsv().email_check(url, self.df, self.HEADERS, self.COOKIES,filter_result, income)
        else:
            # If there are redirections or an error, print the HTTP response status code.
            # Store the HTTP response status code and URL in a CSV file.
            UpdateCsv().store_response(response.status_code,url,self.df)
    def send_request(self)->None:
        """
        Send HTTP requests to multiple URLs concurrently using ThreadPoolExecutor.

        This method performs the following tasks:

        1. Retrieves a list of URLs from the DataFrame.
        2. Checks the validity of the URLs and filters out any invalid or duplicate URLs.
        3. Utilizes ThreadPoolExecutor with a maximum of 8 worker threads to send HTTP requests.
        4. Invokes the `process_urls` method for each valid URL to initiate the scraping process.

        Args:
            None

        Returns:
            None
        """
        # Retrieve a list of URLs from the DataFrame,
        urls = self.df['urls'].to_list()

        # Check and filter the URLs to ensure they are not scraped before.
        urls = UpdateCsv().check_urls(urls, self.df)

        # Use ThreadPoolExecutor with a maximum of 16 worker threads.
        with ThreadPoolExecutor(max_workers=8) as executor:
            # Send HTTP requests and initiate the scraping process for each URL.
            result = executor.map(self.process_urls, urls)


