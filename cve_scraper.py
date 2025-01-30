# goal of this script is to iterate through (tbd #) pages of the nvd database, 
# for each cve link, check if there is a github link, if there is, add it to a
# csv

import csv
import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup

# Regular expression to match GitHub commit URLs
github_commit_pattern = re.compile(r"https://github\.com/.*")

all_links = []

# Function to fetch and parse a page
async def fetch_page(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200 and "text/html" in response.headers.get("Content-Type", ""):
                return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

# Function to collect cve descriptions and GH links; returns empty links if no GH links are found
async def find_cve_descriptions(session, url_suffix):
    url = 'https://nvd.nist.gov/' + url_suffix
    html = await fetch_page(session, url)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    description = soup.find('p', {'data-testid': 'vuln-description'}).text

    repo_links = []

    for link in links:
        if github_commit_pattern.match(link):
            repo_links.append(link)

    if len(repo_links) < 2:
        return 'blank', None

    return [description], repo_links

# Main function to scrape the first page and its subsequent links
async def scrape_for_github_links(first_page_url):
    async with aiohttp.ClientSession() as session:
        # Fetch the first page
        html = await fetch_page(session, first_page_url)
        if not html:
            print("Failed to fetch the first page.")
            return

        # Parse the first page to get links
        soup = BeautifulSoup(html, 'html.parser')
        second_page_links = [a['href'] for a in soup.find_all('a', href=True)]
        cve_links = [link for link in second_page_links if link.startswith("/vuln/detail/CVE")]

        # Fetch and analyze the second pages for GitHub links
        # find_cve_descriptions(session, link) for link in cve_links
        tasks = []

        for link in cve_links:
            tasks.append(find_cve_descriptions(session, link))

        results = await asyncio.gather(*tasks)

        # Flatten the list of results
        all_current_links = []
        for sublist in results:
            for link in sublist:
                all_current_links.append(link)
        all_links.append(all_current_links)

# Run the scraper in four month increments
async def main():
    async with aiohttp.ClientSession():
        for year in range(0, 5):
            print(f"\nyear 202{year}: ")
            for start_month in range(1, 12, 4):
                end_month = start_month + 3

                if end_month < 10:
                    end_month = '0' + str(end_month)

                print(f"\t\n\nmonths {start_month} to {end_month}: ")

                curr_date_range = f"https://nvd.nist.gov/vuln/search/results?form_type=Advanced&results_type=overview&search_type=all&isCpeNameSearch=false&pub_start_date=0{start_month}%2F01%2F202{year}&pub_end_date={end_month}%2F01%2F202{year}&tags=Disputed"
                nvd = curr_date_range
                await scrape_for_github_links(nvd)
                print("completed")

asyncio.run(main())

# all_links now populated with... all the links
with open("repo_data.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['Description', 'Links'])
        for section in all_links:
            for index in range(0, len(section), 2):
                if section[index][0] != 'blank' and section[index + 1]:
                    desc = section[index][0]
                    links = section[index + 1][0]
                    writer.writerow([desc, links])

print("NVD Data stored in \'repo_data.csv\'")
