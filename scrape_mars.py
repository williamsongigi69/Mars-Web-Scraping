import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from selenium import webdriver
import requests as req
import re

from splinter import browser
from selenium import webdriver


def scrape():
#scrape the NASA Mars News SIte, collect news title, paragraph text, assign
#to variables for later reference
    url = "https://mars.nasa.gov/news/"
    response = req.get(url)
    soup = bs(response.text, 'html5lib')

#scrape the title and accompanying paragraph
    news_title = soup.find("div", class_="content_title").text
    paragraph_text = soup.find("div", class_="rollover_description_inner").text

#Visit the URL for JPL's Space images
#splinter to navigate the site and find the image url for the current featured
#image and assign it to featured_image_url (use .jpg)

#set up splinter
    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

#stir soup for scraping
    html = browser.html
    soup = bs(html, "html.parser")

#have webdriver click links to get to the full image I want
    browser.click_link_by_partial_text('FULL IMAGE')

#had to add this, wasn't working and docs recommended waiting between clicks
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

#stir new soup for scraping the image url
    new_html = browser.html
    new_soup = bs(new_html, 'html.parser')
    temp_img_url = new_soup.find('img', class_='main_image')
    back_half_img_url = temp_img_url.get('src')

    recent_mars_image_url = "https://www.jpl.nasa.gov" + back_half_img_url

#get mars weather. THE INSTRUCTIONS SAY SPECIFICALLY TO SCRAPE THE DATA
#stir soup
    twitter_response = req.get("https://twitter.com/marswxreport?lang=en")
    twitter_soup = bs(twitter_response.text, 'html.parser')

#use find_all to get all the tweets on the page, scan the 10 most recent for "Sol"
    tweet_containers = twitter_soup.find_all('div', class_="js-tweet-text-container")
    for i in range(10):
        tweets = tweet_containers[i].text
        if "Sol " in tweets:
            mars_weather = tweets
            break

#Mars Facts....visit webpage, use pandas to scrape the page for facts,
#convert pandas table to html table string.
    request_mars_space_facts = req.get("https://space-facts.com/mars/")

#use pandas to scrape html table data
    mars_space_table_read = pd.read_html(request_mars_space_facts.text)
    df = mars_space_table_read[0]

#set the index to the titles of each statistic/value
    df.set_index(0, inplace=True)
    mars_data_df = df

#convert new pandas df to html, replace "\n" to get html code
    mars_data_html = mars_data_df.to_html()
    mars_data_html.replace('\n', '')
    mars_data_df.to_html('mars_table.html')

#..Visit the USGS Astrogeology site to obtain hgih resolution images for
#....each of Mar's hemispheres
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_req = req.get(usgs_url)

#..You will need to click each of the links to the hemispheres in order
#....to find full res image

#had trouble doing this with splinter, decided to just do a bunch of loops for img urls
    soup = bs(usgs_req.text, "html.parser")
    hemi_attributes_list = soup.find_all('a', class_="item product-item")
#list to keep the dictionaries that have title and image url
    hemisphere_image_urls = []
    for hemi_img in hemi_attributes_list:
        #get the img title
        img_title = hemi_img.find('h3').text
        #print(img_title)
        #get the link to stir another soup, this is the page with the actual image url
        link_to_img = "https://astrogeology.usgs.gov/" + hemi_img['href']
        #print(link_to_img)
        img_request = req.get(link_to_img)
        soup = bs(img_request.text, 'lxml')
        img_tag = soup.find('div', class_='downloads')
        img_url = img_tag.find('a')['href']
        hemisphere_image_urls.append({"Title": img_title, "Image_Url": img_url})

    mars_data = {
     "News_Title": news_title,
     "Paragraph_Text": paragraph_text,
     "Most_Recent_Mars_Image": recent_mars_image_url,
     "Mars_Weather": mars_weather,
     "mars_h": hemisphere_image_urls
     }

    return mars_data
