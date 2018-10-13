# Importing important libraries
import cfscrape
from bs4 import BeautifulSoup as soup
import re


def get_link(text):
    return re.search("(?P<url>https?://[^\s]+.jpg)", text).group("url")


def scrape(link, fileName):
    # Bypassing CloudFare DDos Protection using 3rd party module called 'cfscrape'
    scraper = cfscrape.create_scraper()
    pageHTML = scraper.get(link).content

    # Grabbing HTML source code
    pageSoup = soup(pageHTML, 'html.parser')

    # Finding the desired container from the pageSoup
    containers = pageSoup.findAll('div', {'class': 'item_film_list'})

    # Opening file for writing csv

    # Using utf8 encoding due to compatibility issue in Windows
    f = open(fileName, 'w', encoding='utf8')

    # Defining headers of csv file
    headers = 'Title, Link, ThumbnailLink, Genre\n'

    # Writing headers
    f.write(headers)

    # Running loop for each container
    for container in containers:
        # Video link
        vidLink = container.a['href']

        # Thumbnail source
        thumbContainer = container.findAll('img', {'class': 'thumb'})

        # Getting the thumbnail URL
        thumbUrl = get_link(str(thumbContainer[0])).strip()

        # Title of the Video
        title = container.h3.span.text

        # Genre
        genresSplit = container.p.text.split('\n')
        genres = genresSplit[2]

        print('title: ' + title)
        print('vidLink: ' + vidLink)
        print('thumbUrl: ' + thumbUrl)
        print('genres: ' + genres)
        print('\n\n')

        # Writing extrated values in csv file
        f.write(title + ',' + vidLink + ',' + thumbUrl + ',' + genres.replace(',', '|') + '\n')

    # Safely closing the file
    f.close()


if __name__ == '__main__':
    scrape("https://kissanime.ac/kissanime.html", "KissanimeFrontPage.csv")