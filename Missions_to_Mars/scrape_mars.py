from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html 
    soup = bs(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text

    
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)

    browser.click_link_by_partial_text('more info')
    html = browser.html
    image_soup = bs(html, 'html.parser')

    feat_img_url = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{feat_img_url}'
    print(featured_image_url)

   

    MarsFacts_url = 'https://space-facts.com/mars/'
    browser.visit(MarsFacts_url)
    time.sleep(2)
    html = browser.html
    table = pd.read_html(html)
    facts_df = table[0]
    facts_df.columns =['Description', 'Value']
    facts_df = mars_facts.set_index('Description')
    facts_df = mars_facts.to_html(classes="table table-striped")

   
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    hemisphere_image_urls = []
    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")


    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})



    browser.quit()

    return mars_data


