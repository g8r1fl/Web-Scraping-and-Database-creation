from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # Visit mars.nasa.gov/news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # get latest news title and summary paragraph
    title_list = soup.find_all('div', class_='content_title').text
    news_title = title_list[1].text
    news_p = soup.find('div', class_='rollover_description_inner').text

    mars_news = {
        'news_title': news_title, 'news_p': news_p
    }

    # Close the browser after scraping
    # browser.quit()

# Get Mars featured image
    # open browser again for next webpage scrape
    # browser = init_browser()

    # Visit mars.nasa.gov/news
    url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url2)

    time.sleep(1)

    # Scrape page into Soup
    # HTML object
    html = browser.html
    base2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # find the parent div of the image
    img_url = soup.find('div', class_='floating_text_area')
    # find the href within the div
    ref = img_url.find('a')['href']
    # build the final link for the featured image
    featured_image_url = base2 + ref

    # add data to dictionary
    mars_news['featured_image_url'] = featured_image_url

    # Close the browser after scraping
    # browser.quit()

# Get Mars facts table
    # open browser again for next webpage scrape
    # browser = init_browser()

    # Visit mars.nasa.gov/news
    url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)

    time.sleep(1)

    # read tables from web and put in dataframe
    tables = pd.read_html(url3)
    table = tables[0]
    table.columns = ['','Mars']

    # cast dataframe to html
    table.to_html('table.html', index=False)

    # add data to dictionary
    mars_news['table'] = 'table.html'

    browser.quit()

    # return results
    return mars_news

