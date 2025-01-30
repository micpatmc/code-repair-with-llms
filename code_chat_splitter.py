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


async def fetch_page(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200 and "text/html" in response.headers.get("Content-Type", ""):
                return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

async def getIssueData(session, baseLink):
    html = await fetch_page(session, baseLink)
    if not html:
        return
    
    codeData = []
    chatData = []

    soup = BeautifulSoup(html, 'html.parser')
    #https://github.com/phpmyadmin/phpmyadmin/issues?q=is%3Aissue%20state%3Aclosed

    return codeData, chatData

async def main():
    with open('repo_data.csv', 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    df = pd.read_csv('repo_data.csv', encoding=encoding)

    descToLink = {}
    codeData = []
    chatData = []

    async with aiohttp.ClientSession() as session:
        for row in df.iterrows():
            desc = row[1].iloc[0]
            link = row[1].iloc[1]

            baseLink = []
            listedLink = link.split('/')

            for string in range(0, 5):
                baseLink.append(listedLink[string])

            baseLink.append('issues?q=is%3Aissue state%3Aclosed')
            baseLink = '/'.join(baseLink)
            print(baseLink)
            break

            codeData, chatData = getIssueData(session, baseLink)
            break

