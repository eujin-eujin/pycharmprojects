from time import time
import pandas as pd
import numpy as np
from search import SearcResult
from videoinfo import  VideoInfo
import os


# this decorator function is to tell us  time taken for running the function
def timing_decorator(func):
    def wrapper(*arg,**kwargs):
        start_time = time()
        func(*arg,**kwargs) # calls the orginal function
        end_time = time()
        execution_time = (end_time-start_time)/60
        print(f'time taken for running the {func.__name__} is : {execution_time:.3f} mins')
    return  wrapper

@timing_decorator
def start_search_results(keywords):
    print(f'{"*"*10}started SearchResult{"*"*10}')
    SearcResult(keywords)
    print(f'{"*"*10}finished SearchResult{"*"*10}')

@timing_decorator
def start_videinfo():
    print(f'{"*" * 10}started VideoIfno{"*" * 10}')
    VideoInfo()
    print(f'{"*" * 10}finished VideoInfo{"*" * 10}')


def rename_channels_csv():
    """
    Rename the 'channels.csv' file in the 'data' folder to the next available number, such as 'channels4.csv,' 'channels5.csv,' and so on.

    The function checks for existing files in the 'data' folder with names in the format 'channelsX.csv' and determines the next available number.
    If no such files exist, it starts with 'channels1.csv.'

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    data_dir = 'data'  # data folder path
    base_filename = 'channels.csv'

    # Find the highest numbered file in the format "channelsX.csv"
    existing_files = [f for f in os.listdir(data_dir) if f.startswith(base_filename[:-4])]

    if existing_files:
        highest_number = max([int(f[len(base_filename) - 4]) for f in existing_files])
        new_filename = f'{base_filename[:-4]}{highest_number + 1}.csv'
    else:
        new_filename = 'channels1.csv'

    # Rename the file
    try:
        os.rename(os.path.join(data_dir, base_filename), os.path.join(data_dir, new_filename))
    except Exception as error_msg:
        print(error_msg)




if __name__=='__main__':
    s_time = time()
    # start_search_results()
    # start_videinfo()
    e_time  = time()
    rename_channels_csv()
    # print(f'time taken for executing this script is :{(e_time-s_time)/60:.3f}')