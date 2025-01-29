# goal is to
# 1. iterate through repo_data.csv and determine which links to reserve for chat and code models
#   1a. iterate through each repo and get all the diffs, see what changes were made etc
#   1b. split each repo's contents (text description and code) for chat and code models
# 2. format data into dataset for fine-tuning

import pandas as pd
import asyncio
import aiohttp
import chardet
from bs4 import BeautifulSoup

from cve_scraper import fetch_page

with open('repo_data.csv', 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

df = pd.read_csv('repo_data.csv', encoding=encoding)

descToLink = {}
codeRepos = []
chatRepos = []


for row in df.iterrows():
    desc = row[1].iloc[0]
    link = row[1].iloc[1]

    baseLink = str(string for string in link.split('/'))

    print(baseLink)
    break

