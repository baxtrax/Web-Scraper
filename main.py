from time import sleep
import requests
from bs4 import BeautifulSoup

# Urls are in a dictionary, with this pattern:
# {"<url>": <"<category>"}
URLS = {"https://www.espn.com/nhl/story/_/id/38461866/nhl-stars-level-jason-robertson-filip-forsberg-troy-terry": "sports",
        "https://www.espn.com/mlb/story/_/id/38463265/aaron-judge-new-york-yankees-captain-2023-mlb-season-no-playoffs": "sports",
        "https://www.espn.com/nfl/story/_/id/38479964/los-angeles-rams-aaron-donald-not-slowing-down": "sports",
        "https://www.espn.com/fantasy/hockey/story/_/id/38373882/espn-nhl-2023-draft-how-play-win-fantasy-hockey-league-pro": "sports",
        "https://preppykitchen.com/french-macarons/": "food"}

# User agent headers makes a request look like it coming from a device.
# This specific user-agent is for a Windows Desktop that is using an edge browser
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}


# Files generated will be 01<index>_<category>.txt
def main():
    idx = 11 # Start index use for file creation
    for url in URLS:
        sleep(0.5) # Add wait to not overload the server

        # Get category and publisher
        categ = URLS[url]
        pub = url.split('/')[2]

        # Grab html from url
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # Logic handling will be different per publisher
        match pub:
            case "www.espn.com":
                author = soup.select('div.author')[0].text.split(',')[0]
                timestamp = soup.select('div.author')[0].select('span.timestamp')[0].text
                body = ''.join(t.text+'\n' for t in soup.select('div.article-body')[0].select('p'))
            case "preppykitchen.com":
                author = soup.select('span.entry-author-name')[0].text
                timestamp = soup.select('time.entry-time')[0].text
                body = ''.join(t.text+'\n' for t in soup.select('div.entry-content')[0].select('p'))

        # Write data to files
        with open(f"""output/01{idx}_{categ}.txt""", 'w') as file:
            file.write('Author: ' + author + '\n') 
            file.write('Date: ' + timestamp + '\n')
            file.write('Publication: ' + pub + '\n\n')
            file.write(body)

        idx+=1

main()