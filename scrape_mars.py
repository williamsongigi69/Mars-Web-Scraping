#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

# Part 2


def scrape():

    mars = {}

    # # NASA Mars News - BeautifulSoup

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_news = bs(response.text, 'html.parser')

    # print(soup_news.prettify())

    # collect the latest News Title
    results_t = soup_news.find_all('div', class_='content_title')

    #strip the string from tags
    news_title = results_t[-1].text

    # print(news_title)
    # print(type(news_title))


    # collect the latest Paragraph for title
    results_p = soup_news.find_all('div', class_='rollover_description_inner')

    # strip the string from tags
    news_p = results_p[-1].text

    # print(news_p)
    # #ensure it is a string
    # print(type(news_p))

    # adding variables to the Python dictionary
    mars['news_title'] = news_title
    mars['news_paragraph'] = news_p

    # # JPL Mars Space Images - Featured Image


    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    # check location for my chrome driver
    # get_ipython().system('which chromedriver')


    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)


    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)


    html_jpl = browser.html
    soup_jpl = bs(html_jpl, 'html.parser')

    #print to ensure it worked

    # print(soup.prettify())
    # found the 'Full Image' button by using Inspect on the website.

    # <footer>
    #<a class="button fancybox"
    # data-description="This before-and-after pair of images of the same patch of ground in front of NASA's Mars Exploration Rover Opportunity 13 days apart documents the arrival of a bright rock onto the scene."
    # data-fancybox-group="images" data-fancybox-href="/spaceimages/images/mediumsize/PIA17761_ip.jpg"
    # data-link="/spaceimages/details.php?id=PIA17761"
    # data-title="Rock That Appeared in Front of Opportunity on 'Murray Ridge'" id="full_image">
    # FULL IMAGE
    # </a>
    # </footer>


    image = soup_jpl.find('footer').find('a')
    link = image['data-fancybox-href']


    # create dynamic url and store it in a variable
    feature_image_url = f"https://www.jpl.nasa.gov{link}"

    # adding variables to the Python dictionary
    mars['feature_image_url'] = feature_image_url

    ####### # # Mars Weather - Beatiful Soup


    # URL of page to be scraped
    url_tweet = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    response_tweet = requests.get(url_tweet)
    soup_tweet = bs(response_tweet.text, 'html.parser')
    # print(soup_tweet.prettify())


    tweet = soup_tweet.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    # access latest tweet and store in a variable
    mars_weather = tweet[0].text

    # adding variables to the Python dictionary
    mars['mars_tweet'] = mars_weather

   ###### # # Mars Facts - Pandas for scrapping

    url_facts = 'https://space-facts.com/mars/'

    # We can use the `read_html` function in Pandas to automatically scrape any tabular data from a page.

    tables = pd.read_html(url_facts)

    # Access the table within a the list
    df = tables[0]

    #save html
    df.to_html('facts_table.html')


    ######## Mars Hemispheres - SPLINTER


    # Getting ready for Splinter
    url_usgs = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(url_usgs)

    hemisphere_image_urls = []

    # HTML object
    html_usgs = browser.html

    # Parse HTML with Beautiful Soup
    soup_usgs = bs(html_usgs, 'html.parser')

    for x in range(0,4):

        browser.visit(url_usgs)

        # Get the title name
        hemosphere_name = soup_usgs.find_all('h3')[x].text

        hemisphere_image_urls_title = {'title': hemosphere_name}
        hemisphere_image_urls.append(hemisphere_image_urls_title)

    #     Get the image url by navigating to new page with Splinter

        browser.click_link_by_partial_text(hemosphere_name)

        image_page = browser.url
        response_usgs_image = requests.get(image_page)
        soup_usgs_image = bs(response_usgs_image.text, 'html.parser')

        hemosphere_image = soup_usgs_image.find_all('img', class_='wide-image')
        hemosphere_image = hemosphere_image[0]['src']
        hemosphere_image_complete = f'https://astrogeology.usgs.gov{hemosphere_image}'

        hemisphere_image_urls_img = {'img_url': hemosphere_image_complete}
        hemisphere_image_urls.append(hemisphere_image_urls_img)


   # adding variables to the Python dictionary
    mars['hemisphere_image_urls'] = hemisphere_image_urls

    ######
    return mars
