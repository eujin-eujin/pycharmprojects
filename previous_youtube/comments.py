import re
import json
import sys
import pandas as pd
import  requests
from bs4 import  BeautifulSoup




class Comments:
    COOKIES = {
        'GPS': '1',
        'YSC': 'TXRhCJzSu2M',
        'VISITOR_INFO1_LIVE': '1bw7X-fLsbY',
        'PREF': 'tz=Asia.Calcutta&f4=4000000',
        'CONSISTENCY': 'AFxCXmdussDPJzeG8RoGqnoNUzfyFXLxgl3UI2N5RoH-cphTyhtGRMnZRBxxs9WZWO9y4Y8ZJtEcXr3hqbDmlobQtml6WWTfyBHGz4ZcSKSqsDEUyJhY3G48pvxVPrKtoi-5qlXZoXL5_kp7l_IZcZY',
    }
    HEADERS = {
        'authority': 'www.youtube.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        # 'cookie': 'GPS=1; YSC=TXRhCJzSu2M; VISITOR_INFO1_LIVE=1bw7X-fLsbY; PREF=tz=Asia.Calcutta&f4=4000000; CONSISTENCY=AFxCXmdussDPJzeG8RoGqnoNUzfyFXLxgl3UI2N5RoH-cphTyhtGRMnZRBxxs9WZWO9y4Y8ZJtEcXr3hqbDmlobQtml6WWTfyBHGz4ZcSKSqsDEUyJhY3G48pvxVPrKtoi-5qlXZoXL5_kp7l_IZcZY',
        'dnt': '1',
        'origin': 'https://www.youtube.com',
        'referer': 'https://www.youtube.com/watch?v=dxVaP0-aFIE',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"115.0.5790.110"',
        'sec-ch-ua-full-version-list': '"Not/A)Brand";v="99.0.0.0", "Google Chrome";v="115.0.5790.110", "Chromium";v="115.0.5790.110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-goog-visitor-id': 'CgsxYnc3WC1mTHNiWSjYj6KmBg%3D%3D',
        'x-youtube-bootstrap-logged-in': 'false',
        'x-youtube-client-name': '1',
        'x-youtube-client-version': '2.20230731.00.00',
    }
    def __init__(self,video_url):
        self.video_url = video_url
        self.channeldata = []
        self.main()

    def get_token(self):
        cookies = {
            'GPS': '1',
            'YSC': 'TXRhCJzSu2M',
            'VISITOR_INFO1_LIVE': '1bw7X-fLsbY',
            'PREF': 'tz=Asia.Calcutta&f4=4000000',
            'CONSISTENCY': 'AFxCXmdussDPJzeG8RoGqnoNUzfyFXLxgl3UI2N5RoH-cphTyhtGRMnZRBxxs9WZWO9y4Y8ZJtEcXr3hqbDmlobQtml6WWTfyBHGz4ZcSKSqsDEUyJhY3G48pvxVPrKtoi-5qlXZoXL5_kp7l_IZcZY',
        }
        headers = {
            'authority': 'www.youtube.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            # 'cookie': 'GPS=1; YSC=TXRhCJzSu2M; VISITOR_INFO1_LIVE=1bw7X-fLsbY; PREF=tz=Asia.Calcutta&f4=4000000; CONSISTENCY=AFxCXmdussDPJzeG8RoGqnoNUzfyFXLxgl3UI2N5RoH-cphTyhtGRMnZRBxxs9WZWO9y4Y8ZJtEcXr3hqbDmlobQtml6WWTfyBHGz4ZcSKSqsDEUyJhY3G48pvxVPrKtoi-5qlXZoXL5_kp7l_IZcZY',
            'dnt': '1',
            'origin': 'https://www.youtube.com',
            'referer': 'https://www.youtube.com/watch?v=UJeSWbR6W04&t=22s',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"115.0.5790.110"',
            'sec-ch-ua-full-version-list': '"Not/A)Brand";v="99.0.0.0", "Google Chrome";v="115.0.5790.110", "Chromium";v="115.0.5790.110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'same-origin',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'x-goog-visitor-id': 'CgsxYnc3WC1mTHNiWSjYj6KmBg%3D%3D',
            'x-youtube-bootstrap-logged-in': 'false',
            'x-youtube-client-name': '1',
            'x-youtube-client-version': '2.20230731.00.00',
        }
        response = requests.get(self.video_url,headers=headers,cookies=cookies)
        soup = BeautifulSoup(response.text, 'lxml')
        script_tag = soup.find('script', string=re.compile(r'var ytInitialData ='))
        json_data = re.search(r'var ytInitialData =\s?(.*)?;', script_tag.text)
        data = json.loads(json_data.group(1))
        token = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][3][
            'itemSectionRenderer']['contents'][0]['continuationItemRenderer']['continuationEndpoint'][
            'continuationCommand']['token']
        return token

    def get_comments(self,token):
        '''---api setup'''
        api_url = 'https://www.youtube.com/youtubei/v1/next?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false'

        json_data = {
            'context': {
                'client': {
                    'hl': 'en',
                    'gl': 'IN',
                    'remoteHost': '103.172.89.198',
                    'deviceMake': '',
                    'deviceModel': '',
                    'visitorData': 'CgsxYnc3WC1mTHNiWSjYj6KmBg%3D%3D',
                    'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36,gzip(gfe)',
                    'clientName': 'WEB',
                    'clientVersion': '2.20230731.00.00',
                    'osName': 'Windows',
                    'osVersion': '10.0',
                    'originalUrl': 'https://www.youtube.com/watch?v=UJeSWbR6W04&t=22s',
                    'platform': 'DESKTOP',
                    'clientFormFactor': 'UNKNOWN_FORM_FACTOR',
                    'configInfo': {
                        'appInstallData': 'CNiPoqYGEIKlrwUQndv-EhCF2f4SEOuTrgUQrLevBRD6vq8FEPOorwUQvbauBRD956gYEJHPrwUQtMmvBRC1pq8FEJrRrwUQksuvBRDUoa8FENuvrwUQ3M-vBRCPw68FEKnErwUQzK7-EhC4i64FEN62rwUQ4LavBRDnuq8FEJCjrwUQ4tSuBRClwv4SEO6irwUQjMuvBRDM364FEOat_hIQieiuBRCEtq8FEJbOrwUQ_rWvBRC41a8FEPi1rwUQ6sOvBRCMt68FEOSz_hI%3D',
                    },
                    'browserName': 'Chrome',
                    'browserVersion': '115.0.0.0',
                    'acceptHeader': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'deviceExperimentId': 'ChxOekkyTWpJd016YzJNakU1TWpRMk1EUTRNdz09ENiPoqYGGNiPoqYG',
                    'screenWidthPoints': 1029,
                    'screenHeightPoints': 571,
                    'screenPixelDensity': 2,
                    'screenDensityFloat': 1.5,
                    'utcOffsetMinutes': 330,
                    'userInterfaceTheme': 'USER_INTERFACE_THEME_LIGHT',
                    'connectionType': 'CONN_CELLULAR_4G',
                    'memoryTotalKbytes': '8000000',
                    'mainAppWebInfo': {
                        'graftUrl': 'https://www.youtube.com/watch?v=UJeSWbR6W04&t=22s',
                        'pwaInstallabilityStatus': 'PWA_INSTALLABILITY_STATUS_UNKNOWN',
                        'webDisplayMode': 'WEB_DISPLAY_MODE_BROWSER',
                        'isWebNativeShareAvailable': True,
                    },
                    'timeZone': 'Asia/Calcutta',
                },
                'user': {
                    'lockedSafetyMode': False,
                },
                'request': {
                    'useSsl': True,
                    'internalExperimentFlags': [],
                    'consistencyTokenJars': [
                        {
                            'encryptedTokenJarContents': 'AFxCXmdussDPJzeG8RoGqnoNUzfyFXLxgl3UI2N5RoH-cphTyhtGRMnZRBxxs9WZWO9y4Y8ZJtEcXr3hqbDmlobQtml6WWTfyBHGz4ZcSKSqsDEUyJhY3G48pvxVPrKtoi-5qlXZoXL5_kp7l_IZcZY',
                            'expirationSeconds': '600',
                        },
                    ],
                },
                'clickTracking': {
                    'clickTrackingParams': 'CI4CELsvGAMiEwjE6NHWzbqAAxUSg9gFHVMEACA=',
                },
                'adSignalsInfo': {
                    'params': [
                        {
                            'key': 'dt',
                            'value': '1690863577513',
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
                            'value': '2',
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
                            'value': '1013',
                        },
                        {
                            'key': 'brdim',
                            'value': '0,0,0,0,1280,0,1280,680,1029,571',
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
                },
            },
            'continuation': '  var ytInitialPlayerResponse ',
        }
        json_data['continuation'] = token
        response = requests.post(api_url, headers=self.HEADERS, cookies=self.COOKIES, json=json_data)
        data = json.loads(response.text)
        try:
            comments  =  data['onResponseReceivedEndpoints'][1]['reloadContinuationItemsCommand']['continuationItems'][:-1]
            new_token = \
            data['onResponseReceivedEndpoints'][1]['reloadContinuationItemsCommand']['continuationItems'][len(data[
            'onResponseReceivedEndpoints'][1]['reloadContinuationItemsCommand']['continuationItems'])-1][
                'continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
        except   Exception as e:
            try:
                comments = data['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems'][:-1]
                new_token = \
                data['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems'][len(data[
                'onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems'])-1][
                    'continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
            except Exception as e :
                comments = data['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems']
                print(e)
                print(token)
                new_token = ''
        self.save_comments(comments)
        if new_token =='':
            df = pd.DataFrame(self.channeldata)
            csv = df.to_csv('youtubechanneldata1.csv',index=False)
            sys.exit()


        '''--pagination---'''
        self.get_comments(new_token)

    def save_comments(self,comments):
        all_json_data  = []
        try:
            for comment in comments:
                try:
                    channel_id = comment['commentThreadRenderer']['comment']['commentRenderer'][
                        'authorCommentBadge']['authorCommentBadgeRenderer'][
                        'authorText']['accessibility']['accessibilityData']['label']
                    json_data_ = {'channel_id': channel_id.split(',')[0], 'status': channel_id.split(',')[1]}

                except Exception as e:
                    channel_id = comment['commentThreadRenderer']['comment']['commentRenderer']['authorText'][
                        'simpleText']
                    json_data_ = {'channel_id': channel_id, 'status': ""}

                try:
                    replies = comment['commentThreadRenderer']['replies'][
                        'commentRepliesRenderer']['viewReplies']['buttonRenderer']['text']['runs'][0]['text']
                    json_data_['replies'] = replies
                except Exception as e:
                    replies = ''
                    json_data_['replies'] = replies
                self.channeldata.append(json_data_)
                print(json_data_)


        except Exception as e:
            print(e)

    def main(self):
        token = self.get_token()
        self.get_comments(token)


if __name__=='__main__':
    url = 'https://www.youtube.com/watch?v=dxVaP0-aFIE'
    comment = Comments(url)

