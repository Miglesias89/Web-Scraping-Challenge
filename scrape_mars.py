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
    print(mars_weather.text)


# Mars Facts

    url = "https://space-facts.com/mars/"
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    response = requests.get(url)

    mars_facts = soup.find('table', id = "tablepress-p-mars-no-2")

    facts_table = str(mars_facts)

    mars_table = pd.read_html(facts_table)

    mars_table_df = mars_table[0]
    mars_table_df.columns = ["Description", "Values"]
    mars_table_df

# Mars Hemispheres

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    response = soup.find_all('div', class_="item")

    base_url = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/"

    for image in response: 
        hp_image = image.find('a', class_= "product-item").find('img', class_="thumb")
        
        hp_image = str(hp_image)
        
        hp_image = hp_image.split("_",1)
        
        hp_image = hp_image[1].split('_thumb.png"/>')
        
        image_url = base_url + hp_image[0] + '/full.jpg'
            
        image_title = image.find('div', class_="description").find('a', class_ = "product-item").find('h3').text
        
        image_dict = {'title': image_title,
                    'img_url': image_url}
        
        hemisphere_image_urls.append(image_dict)

    browser.quit()

#Mars Dictionary

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image,
        "mars_weather": mars_weather,
        "mars_table" : mars_table_df,
        "hemisphere" : image_dict

    }

    return mars_data



