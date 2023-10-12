'''importing required modules'''
import json
import re
from time import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor



class VideoInfo:

    def __init__(self):

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
        self.video_titles = []
        self.video_views = []
        self.send_request()

    def process_urls(self,url:str)->None:
        # Send an HTTP GET request to the provided URL with headers and cookies.
        response = requests.get(url, headers=self.HEADERS, cookies=self.COOKIES)
        # Check if the requested URL matches the final URL (no redirects) and if there are no redirections.
        if (url == response.url) & (not response.history):
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
                video_title =[title['richItemRenderer'][
                 'content']['videoRenderer']['title']['runs'][0]['text'] for title in content[:-1]]
                self.video_titles += video_title
            except Exception as e:
                print(e)
            try:
                video_views = [ view['richItemRenderer']['content']['videoRenderer']['viewCountText']['simpleText'] for view in content[:-1]]
                self.video_views += video_views
            except Exception as e:
                print(e)
            try:
                # Extract a token for pagination, if available.
                token = content[-1]['continuationItemRenderer']['continuationEndpoint'][
                    'continuationCommand']['token']
            except:
                token = ''
            while token:
                try:
                    self.api_json_data['continuation'] = token
                    new_response = requests.post(
                        self.api_url,
                        params=self.api_params,
                        cookies=self.api_cookies,
                        headers=self.api_headers,
                        json=self.api_json_data,
                    )

                    # Parse the JSON content of the new response.
                    json_content = json.loads(new_response.text)
                    all_video_titles = json_content['onResponseReceivedActions'][
                        0]['appendContinuationItemsAction']['continuationItems']
                    video_titles = [ title['richItemRenderer'][
                    'content']['videoRenderer']['title']['runs'][0]['text'] for title in all_video_titles[:-1]]
                    self.video_titles += video_titles

                    video_views = [
                        view['richItemRenderer']['content']['videoRenderer']['viewCountText']['simpleText'] for view
                        in all_video_titles[:-1]]
                    self.video_views += video_views
                except:
                    video_titles = ''
                try:
                    new_token = all_video_titles[-1]['continuationItemRenderer'][
                    'continuationEndpoint']['continuationCommand']['token']
                except:
                    new_token = None
                token = new_token

    def send_request(self)->None:
        urls = ["https://www.youtube.com/@PiXimperfect/videos"]


        # Use ThreadPoolExecutor with a maximum of 16 worker threads.
        with ThreadPoolExecutor(max_workers=8) as executor:
            # Send HTTP requests and initiate the scraping process for each URL.
            result = executor.map(self.process_urls, urls[:1])


if __name__=='__main__':
    s_time  = time()
    df = pd.read_csv(r'youtubebot/data/channels.csv')
    df = df[df['keywords']!='மிகவும் கம்மியான விலையில்']
    print(df.shape[0])
    # video_views = VideoInfo().video_views
    # video_titles = VideoInfo().video_titles
    # print(video_titles)
    # view_counts = [int(re.sub(r'views?|,','',view)) for view in video_views]
    # print(f'minimum views : {min(view_counts)}',f'maximum views {max(view_counts)}',sep='\n')
    # e_time = time()
    # print(f'time taken for running this script is {(e_time-s_time)/60}mins')