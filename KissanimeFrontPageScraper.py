# Importing important libraries
import cfscrape
from bs4 import BeautifulSoup as soup

URL = 'https://kissanime.ac/kissanime.html'
# Bypassing CloudFare DDos Protection using 3rd party module called 'cfscrape'
scraper = cfscrape.create_scraper()
pageHTML = scraper.get(URL).content

# Grabbing HTML source code
pageSoup = soup(pageHTML,'html.parser')

# Finding the desired container from the pageSoup
containers = pageSoup.findAll('div',{'class':'item_film_list'})

# Opening file for writing csv
fileName = 'KissanimeFrontPage.csv'

# Using utf8 encoding due to compatibility issue in Windows
f = open(fileName,'w',encoding = 'utf8')

# Defining headers of csv file
headers = 'Title, Link, ThumbnailLink, Genre\n'

# Writing headers
f.write(headers)

# Running loop for each container
for container in containers:

    # Video link
    vidLink = container.a['href']

    # Thumbnail source
    thumbContainer = container.findAll('img',{'class':'thumb'})

    # Converting the type from bs4.element.Tag to str
    paragraphs = []
    for x in thumbContainer:
        paragraphs.append(str(x))
    paragraphSplit = paragraphs[0].split(';')
    url = paragraphSplit[4].split('=//')
    finalUrl = url[1].split('"')
    thumbUrl = finalUrl[0]

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
    f.write(title + ',' + vidLink + ',' + thumbUrl + ',' + genres.replace(',' , '|') + '\n')

# Safely closing the file
f.close()
