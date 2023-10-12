'''importing required modules'''
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


class UpdateCsv:

    '''handles updating and filtering process on data\channaels.csv'''

    # Filters unprocessed URLs based on response status codes (100-599).
    def check_urls(self, urls: list, df: pd.DataFrame) -> list:
        """
        Filters a list of URLs based on their corresponding response codes in a DataFrame.

        This method checks if each URL in the given list exists in the DataFrame 'df' and has a response code between
        100 and 599 (inclusive). URLs that meet this criteria are considered as already processed and are excluded
        from the returned list. Only URLs that do not have a corresponding response code in the range [100, 599] are
        included in the returned list to avoid duplicate processing.

        Args:
            urls (list): A list of URLs to be filtered.
            df (pd.DataFrame): A DataFrame containing response codes and URLs for comparison.

        Returns:
            list: A filtered list of URLs that do not have a corresponding response code between 100 and 599 in the DataFrame
                  and are not considered processed.

        """
        # Filter URLs that do not have a corresponding response code between 100 and 599 in the DataFrame
        # and are not considered processed (already processed URLs have response codes in the range [100, 599])
        urls = [url for url in urls if
                df[(df['response'].between(100, 599, inclusive='both')) & (df['urls'] == url)].empty]
        return urls

    # gets contack details like whatsapp number ,contact number ,email id
    def get_contact_info(self, response) -> tuple[str, str, str]:
        """
        Extracts contact information (WhatsApp number, contact number, and email) from a web page's HTML response.

        Args:
            response (str): The HTML content of the web page.

        Returns:
            Tuple[str, str, str]: A tuple containing the extracted WhatsApp number, contact number, and email.
                                 If not found, empty strings are returned for each item.
        """
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')

        try:
            # Try to find the 'description' meta tag for the webpage
            description = soup.find('meta', {'itemprop': 'description'})['content']
        except Exception as e:
            description = ''
            print(e, url)

        # Find phone numbers using the regex pattern
        phone_match = re.findall(r'\b\d{10}\b|\d{5}\s\d{5}', description)
        whatsapp = phone_match[0] if phone_match else ''

        # Find email addresses using the regex pattern
        email_match = re.findall(r'\b[\w+%.-]+@[A-z0-9.-]+\.[A-z]{2,7}\b', description)
        email = email_match[0] if email_match else ''

        if whatsapp:
            # Check if 'whatsapp' is mentioned in the description and separate WhatsApp and contact numbers
            whatsapp_no = whatsapp if 'whatsapp' in description.lower() else ''
            contact_no = whatsapp.strip() if not whatsapp_no else ''
        else:
            whatsapp_no, contact_no = '', ''
        return whatsapp_no, contact_no, email

    # stores response status codes in to appropriate url
    def store_response(self,status_code: int, url: str, df: pd.DataFrame) -> None:
        """
           Stores the provided HTTP response status code in the specified DataFrame for the given URL.

           Parameters:
           - status_code (int): The HTTP response status code to be stored.
           - url (str): The URL associated with the response status code.
           - df (pd.DataFrame): The DataFrame where the response status code should be stored.

           Returns:
           - None

           This method checks if the provided URL exists in the DataFrame and, if found, updates the 'response'
           column in the corresponding row with the given status_code.
           """
        # Check if the URL is present in the DataFrame
        if url in df['urls'].values:
            # Get the index of the URL in the DataFrame
            index = df.index[df['urls'] == url].tolist()[0]
            # Update the 'response' column in the appropriate row
            df.at[index, 'response'] = status_code

    def update_subscribers(self,df: pd.DataFrame, url: str, subscriber_count: float) -> None:
        """
           Updates the subscriber count for the provided URL in the specified DataFrame.

           Parameters:
           - df (pd.DataFrame): The DataFrame where the subscriber count should be updated.
           - url (str): The URL associated with the subscriber count.
           - subscriber_count (float): The new subscriber count to be assigned to the URL.

           Returns:
           - None

           This method checks if the provided URL exists in the DataFrame and, if found, updates the 'subscribers'
           column in the corresponding row with the given subscriber_count.
           """
        # Check if the URL is present in the DataFrame
        if url in df['urls'].values:

            # Get the index of the URL in the DataFrame
            index = df.index[df['urls'] == url].tolist()[0]
            # Update the 'subscribers' column in the appropriate row
            df.at[index, 'subscribers'] = subscriber_count

    def email_check(self,url: str,df: pd.DataFrame,headers: dict,
                    cookies: dict, filter: bool, income: str) -> None:

        """
            Checks for the presence of a business inquiry email on a YouTube channel's 'about' page and updates the DataFrame.

            Parameters:
            - url (str): The URL of the YouTube channel.
            - df (pd.DataFrame): The DataFrame containing channel information.
            - headers (dict): HTTP headers for the request.
            - cookies (dict): Cookies for the request.
            - filter (bool): A flag indicating whether to apply filters for email detection.
            - income (str): The income category for the channel (updated only if 'filter' is True).

            Returns:
            - None

            This method checks the 'about' page of a YouTube channel for the presence of a business inquiry email.
            If an email is found, it updates the DataFrame with email-related information, including the presence
            of an email, email ID, WhatsApp number, contact number, and income category (if 'filter' is True).
            The DataFrame is then saved to a CSV file ('data\channels.csv').

            Note:
            - The 'filter' flag determines whether filters are applied during email detection.
            - The 'income' parameter specifies the approx income associated with the channel and is updated only if 'filter' is True.
            """

        # Changing the videos page URL to about page
        about_url = url.replace('/videos', '') + '/about'
        if filter:
            status = 'yes'
            response = requests.get(about_url, headers=headers, cookies=cookies)  # Getting response here
            # Looking for pattern that indicates a business enquiry email
            if re.search(r'[Ff]or\s?[Bb]usiness\s?[eiEI]n?q?u?i?r?i?e?s?|"text": "View email address"|@gmail',
                         response.text, re.M | re.I):
                email = 'yes'
                whatsapp, contact, email_id = self.get_contact_info(response)
                income = income
            else:
                email = 'no'
                whatsapp, contact, email_id = self.get_contact_info(response)
                income = income
        else:
            email = 'no'
            whatsapp, contact, email_id = ['', '', '']
            income = ''
            status = 'no'

        if url in df['urls'].values:
            # Get the index of the URL in the DataFrame
            index = df.index[df['urls'] == url].tolist()[0]
            # Update the 'status and email,email id,whatsapp,contact' columns in the appropriate row
            df.at[index, 'email'] = email
            df.at[index, 'email id'] = email_id
            df.at[index, 'whatsapp'] = whatsapp
            df.at[index, 'contact'] = contact
            df.at[index, 'income'] = income
            df.at[index,'satus']=status
        df.to_csv('data\channels.csv', index=False)