'''importing required modules'''
import re
import pandas as pd
from googleapiclient.discovery import build


class Filter_:
    '''fitering youtube channels based on their
    postion frequency and subscribers count then language of the channels'''
    def __init__(self, df: pd.DataFrame, video_id: str, time_stamps: list, url: str) -> None:
        """
        Initializes a Filter_ object with channel information and video analysis data.

        Args:
            df (pd.DataFrame): A DataFrame containing channel information.
            video_id (str): The ID of the video to be analyzed.
            time_stamps (list): A list of time stamps of videos from the channel.
            url (str): The URL of the channel.

        Attributes:
            df (pd.DataFrame): A DataFrame containing channel information.
            video_id (str): The ID of the video to be analyzed.
            time_stamps (list): A list of time stamps of videos from the channel.
            url (str): The URL of the channel.
            API_KEY (str): The YouTube Data API key for making API requests.
            result (bool): The result of the channel filtering operation (True if the channel meets criteria, False otherwise).

        Returns:
            None
        """
        self.df = df
        self.video_id = video_id
        self.time_stamps = time_stamps
        self.url = url
        self.API_KEY = 'AIzaSyDoDMkxPhxHrFd-VJCe08y24l2i-csa00Y'
        # Perform channel filtering and store the result
        self.result = self.channel_filter()
    # checks how frequently creators upload videos on their channels
    def time_stamp_filter(self) -> bool:
        """
        Filters YouTube channel videos based on their time stamps to ensure content freshness.

        Returns:
            bool: True if the video upload frequency meets the specified criteria, False otherwise.
        """
        # Check if the latest video was posted within a month
        if 'month' in self.time_stamps[0]:
            return False

        # Combine all time stamps into a single string
        string = ' '.join(self.time_stamps)

        # Create a regex pattern to filter time stamp components (e.g., 'secs', 'minutes', 'hours', 'day')
        pattern = re.compile(r'secs?|minutes?|hours?|day$')

        # Count how many videos were posted per day and per month
        posts_per_day = len(re.findall(pattern, string))
        posts_per_month = len(re.findall(r'secs?|minutes?|hours?|days?|weeks?', string))

        # Check if the video upload frequency meets the specified criteria:
        # - Up to 2 videos per day
        # - Between 15 and 30 videos per month
        if posts_per_day <= 2 and (posts_per_month >= 15 and posts_per_month <= 60):
            return True
        else:
            return False
    # checks the language and only takes the channels post video in tamil or english
    def detect_language(self)->bool:
        """
           Detects the language of a YouTube video based on its default audio language.

           Returns:
               bool: True if the detected language is English (en) or Tamil (ta), False otherwise.
           """
        # Build a YouTube API service object
        youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        # Create a request to fetch video details
        request = youtube.videos().list(
            part="snippet",
            id=self.video_id
        )

        # Execute the request and get the response
        response = request.execute()

        try:
            # Attempt to retrieve the default audio language from the response
            audio_language = response['items'][0]['snippet']['defaultAudioLanguage']
        except:
            # If default audio language is not available, set it to an empty string
            audio_language = ''
        # Check if the default audio language is English or Tamil
        if 'en' in audio_language or 'ta' in audio_language:
            return True
        else:
            return False
    # checks whether channel meets all our filters
    def channel_filter(self)->bool:
        """
        This method filters YouTube channels based on specified criteria and returns the filter status.

        Returns:
            bool: True if the channel meets all criteria, False otherwise.
        """
        # Check if the 'urls' column contains the given URL
        condition = self.df['urls'].str.contains(self.url)

        # Extract the subscribers count of the channel
        subscribers_count = self.df.loc[condition, 'subscribers'].to_list()[0]

        # Check if the subscribers_count is within the required range (1000 to 250,000)
        if 1000 <= subscribers_count <= 250000:
            subscribers_count = True
        else:
            subscribers_count = False

        try:
            # Detect the language of the channel and return a boolean value
            language_filter = self.detect_language()
        except Exception as e:
            print(e, self.url)

        try:
            # Apply the time stamp filter and return a boolean value
            time_stamp_filter = self.time_stamp_filter()
        except Exception as e:
            print(e, self.url)

        # Check if the channels are in the right language, channels post video often,
        # and subscribers count is within range
        if (time_stamp_filter and language_filter) and subscribers_count:
            return True
        else:
            return False
