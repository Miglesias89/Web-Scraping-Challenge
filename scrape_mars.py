from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time
import requests
import re

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

#NASA Mars News

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    result = soup.find_all("div", class_= 'content_title')
    news_title = result[1].a.text

    news_p = soup.find('div', class_='article_teaser_body').text

#Featured Image

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    footer = soup.find("footer")
    link = footer.find('a')
    href = link['data-fancybox-href']
    featured_image= 'https://www.jpl.nasa.gov/' + href


# Twitter: Mars Weather 

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    text_weather = re.compile(r'sol')
    mars_weather = soup.find('span', text=text_weather)
    #print(mars_weather.text)


# Mars Facts

    url = "https://space-facts.com/mars/"
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    response = requests.get(url)

    mars_facts = soup.find('table', id = "tablepress-p-mars-no-2")

    mars_table = pd.read_html(url)[0]
    mars_table_df = mars_table
    mars_table_df.columns = ["Description", "Values"]
    #mars_table_df

    table = mars_table_df.to_html(classes="table table-striped")
    

# Mars Hemispheres

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_= 'item')

    hemisphere_image_url = []

    hemisphere_main_url = 'https://astrogeology.usgs.gov'

    for item in items:
        
        title = item.find('h3').text
        
        partial_img_url = item.find('a', class_= 'itemLink product-item')['href']
        
        browser.visit(hemisphere_main_url + partial_img_url)
        
        partial_img_html = browser.html
        
        soup = BeautifulSoup (partial_img_html, 'html.parser')
        
        img_url = hemisphere_main_url + soup.find('img', class_='wide-image')['src']
        
        hemisphere_image_url.append({"title": title, "img_url": img_url})
        
    hemisphere_image_url


    browser.quit()

#Mars Dictionary

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image,
        "mars_weather": mars_weather.text,
        "mars_table" : table,
        "hemisphere" : hemisphere_image_url

    }

    return mars_data



