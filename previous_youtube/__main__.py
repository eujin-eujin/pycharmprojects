import pandas as pd
from  time import  time
from youtube import  YouTube
from analyse import  ChannelAnalyzer
from helper import timing_decorator
import  numpy as np
import helper

@timing_decorator
def run_youtube(keyword):
    youtube = YouTube(keyword)

@timing_decorator
def run_analyser(df):
    analyzer = ChannelAnalyzer(df)

if __name__=='__main__':
    keywords = [
  "productivity tips",
  "how to be productive",
  "time management",
  "goal setting",
  "procrastination",
  "getting organized",
  "work-life balance",
  "remote work",
  "focusing",
  "creativity",
  "productivity for students",
  "productivity for entrepreneurs",
  "productivity for writers",
  "productivity for artists",
  "productivity for moms",
  "productivity for people with ADHD",
  "productivity for people with anxiety",
  "productivity for people with depression",
]
    # for keyword in keywords[1:]:
    #     print(f'we have started the youtbe module..')
    #     run_youtube(keyword)
    # df = pd.read_csv('channels.csv')
    # print(f'we have started the analyser module..')
    # run_analyser(df)
