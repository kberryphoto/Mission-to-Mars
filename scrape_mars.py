#!/usr/bin/env python
# coding: utf-8

# In[102]:


import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time


# In[103]:

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


# In[104]:

mars_list = {}

def scrape_mars_news():
    try:

        # Initialize browser 
        browser = init_browser()

        url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        browser.visit(url1)


        # In[105]:


        html = browser.html
        soup = bs(html, 'lxml')
        #print(soup.prettify())


        # In[107]:


        #Get the Title and Teaser for each post
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        mars_list['news_title'] = news_title
        mars_list['news_p'] = news_p

        return mars_list

    finally:
        browser.quit()


# In[ ]:





# In[42]:


#Find the Featured Image
def scrape_mars_feat_img():
    try:

        # Initialize browser 
        browser = init_browser()
        url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url2)


        # In[43]:


        html = browser.html
        soup = bs(html, 'html.parser')


        # In[15]:


        browser.click_link_by_id('full_image')


        # In[16]:


        time.sleep(3)
        html = browser.html
        soup = bs(html, 'html.parser')


        # In[19]:


        x = soup.find('div', class_="fancybox-inner fancybox-skin fancybox-dark-skin fancybox-dark-skin-open")


        # In[27]:


        featured_image_url = x.find('img')['src']

        mars_list['featured_image_url'] = featured_image_url 

        return mars_list

    finally:
        browser.quit()

# In[ ]:





# In[98]:


#Mars Weather

def scrape_mars_weather():
    try:
        # Initialize browser 
        browser = init_browser()
        url3= 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url3)


        # In[99]:


        html = browser.html
        soup = bs(html, 'html.parser')


        # In[100]:


        mars_weather = soup.find_all('div', class_='js-tweet-text-container')
        for tweet in mars_weather: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

        mars_list['weather_tweet'] = weather_tweet

        return mars_list

    finally:
        browser.quit()
# In[ ]:





# In[34]:


#Mars Facts

def scrape_mars_facts():
    
    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)


    # In[35]:


    html = browser.html
    soup = bs(html, 'html.parser')


    # In[36]:


    tables = pd.read_html(url4)
    tables


    # In[38]:


    df = tables[0]
    df.columns = ['Parameter', 'Facts']
    df.head()


    # In[39]:


    html_table = df.to_html()

    mars_list['html_table'] = html_table

    return mars_list




# In[ ]:





# In[58]:


#Mars Hemispheres

def scrape_mars_hemi():
    try:
        # Initialize browser 
        browser = init_browser()
        url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url4)


        # In[59]:


        html = browser.html
        soup = bs(html, 'html.parser')


        # In[76]:


        #Store the name of the moons
        titlelist = []
        results = soup.find_all('div', class_='description')

        for result in results:
            title = result.find('h3')
            title_text = title.text
            titlelist.append(title_text)
        #titlelist


        # In[84]:


        #Iterate through all pages
        img_url = []
        for moon in titlelist:
            #Start at base url
            url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
            browser.visit(url4)
            html = browser.html
            soup = bs(html, 'html.parser')
            try:
                time.sleep(3)
                browser.click_link_by_partial_text(moon)  
                # HTML object
                html = browser.html
                # Parse HTML with Beautiful Soup
                soup = bs(html, 'html.parser')
                moonurl = soup.find('div', class_='wide-image-wrapper').find('a')['href']
                img_url.append(moonurl)
            except:
                print('Scraping Complete')
        img_url


        # In[89]:


        #Merge the two dictionaries
        hemisphere_image_urls = []
        keys = ['title', 'img_url']
        hemisphere_image_urls = [{key: '' for key in keys} for link in img_url]
        hemisphere_image_urls


        # In[91]:


        x = 0
        for text in titlelist:
            hemisphere_image_urls[x]['title'] = text
            x += 1


        # In[92]:


        x = 0
        for link in img_url:
            hemisphere_image_urls[x]['img_url'] = link
            x += 1


        # In[93]:


        mars_list['hemisphere_image_urls'] = hemisphere_image_urls

        return mars_list

    finally:
        browser.quit()


# In[ ]:




