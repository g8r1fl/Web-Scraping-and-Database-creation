# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
# import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.mars_db
collection = db.articles


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    # Visit mars.nasa.gov/news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_="list_text")
    news_title = results[0].find('a').text
    news_p= soup.find('div', class_="article_teaser_body").text


    url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url2)
    # HTML object
    html2 = browser.html
    base = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    # Parse HTML with Beautiful Soup
    soup = bs(html2, 'html.parser')
    # find the parent div of the image
    img_url = soup.find('div', class_='floating_text_area')
    # find the href within the div
    ref = img_url.find('a')['href']
    # build the final link for the featured image
    featured_image_url = base + ref

    url3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url3)
    table = tables[0]
    # found solutions https://stackoverflow.com/questions/11346283/renaming-columns-in-pandas #2192
    table.columns = ['Description','Mars']
    table = table.to_html(index=False)
    # table_data = []
    # for i in range(len(table)):
    #     dict {}
    #     dict['description'] = table.loc[i, 0]
    #     dict['value'] = 

    # URL of page to be scraped
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base2 = 'https://astropedia.astrogeology.usgs.gov/download/'
    browser.visit(url4)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_='item')
    title_obj = [i.h3.text for i in results]
    href_obj = [base2 + i.a['href'][12:] + '.tif/full.jpg' for i in results]

    hemisphere_image_urls = []
    for i in range(len(title_obj)):
        dict = {}
        dict['title'] = title_obj[i]
        dict['img_url'] = href_obj[i]
        hemisphere_image_urls.append(dict)
    
    browser.quit()
    

    mars_news = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'hemisphere_image_urls': hemisphere_image_urls,
        'table': table
    }
    # return results
    return mars_news




