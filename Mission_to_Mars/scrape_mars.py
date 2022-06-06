import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # splinter browser setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ##########################################
    ############ Nasa Mars News ##############
    ##########################################
    
    ##designate URL for browser to visit
    url = "https://redplanetscience.com"
    
    # browser visit
    browser.visit(url)
    
    # Run BeautifulSoup to gather HTML for parsing
    soup = bs(browser.html, 'html.parser')
    
    # narrow down results to find article title and description #
    results = soup.find_all('div', id='news')
    for result in results:
        news_title = soup.find('div', class_='content_title').text
        news_p = soup.find('div', class_='article_teaser_body').text
        
        print(news_title)
        print('-'*50)
        print(news_p)
     
    ########################################## 
    ## JPL Mars Space Images—Featured Image ##
    ##########################################
    
    # Grab image URL for featured Mars image
    url2 = "https://spaceimages-mars.com"
    browser.visit(url2)

    # Grab HTML with BS
    soup2 = bs(browser.html, 'html.parser')
    
    # narrow down results to get desired URL
    results2 = soup2.find('div', class_='floating_text_area')
    link = results2.find('a', class_='showimg fancybox-thumbs')['href']
    featured_image_url = f'https://spaceimages-mars.com/{link}'
    print(featured_image_url)
    
    ########################################## 
    ############### Mars Facts ###############
    ##########################################
    
    # Using Pandas read_html to pull tables from galaxyfacts-mars.com
    mars_fact_url = 'https://galaxyfacts-mars.com'
    mars_facts = pd.read_html(mars_fact_url)[1]
    mars_facts_html = mars_facts.to_html(index=False)
    
    ########################################## 
    ############ Mars Hemispheres ############
    ##########################################

    
    ########################################################################
    # Hemisphere function to grab relevant info and create hemisphere dict #
    # Output will be a list containing one dictionary for each hemisphere. #
    # Dictionaries contain hemisphere name, image URL, thumbnail image     #
    ########################################################################

    # creating lists to store hemisphere names and images (incl. thumbnail)
    titles = []
    thumbnails = []
    img_urls = []
    
    # Grabbing high-res images and names for Mars hemispheres
    marhem_url = "https://marshemispheres.com/"
    browser.visit(marhem_url)
    
    # links list so that splinter has something to click on
    links = []

    # BeautifulSoup parsing, locating relevant info
    hemsoup = bs(browser.html, 'html.parser')
    hems = hemsoup.find_all('div', class_='item')
    
    # loop through all four hemispheres to grab their names and thumbnail images
    for hem in hems:
        # grab hemi title
        title = hem.h3.text
        
        # clickable link info appended to list
        links.append(title)
        
        # formatting to remove 'Enhanced', appending to list as title
        titles.append(title.replace(' Enhanced', ''))
        
        # locate thumbnail image for later use, append to list
        thumb = hem.img['src']
        thumb_url = f'https://marshemispheres.com/{thumb}'
        thumbnails.append(thumb_url)
    
    # loop through links list, clicking links with splinter to grab image URL
    for name in links:
        # browser clicking and set up
        browser.links.find_by_partial_text(name).click()
        soup = bs(browser.html, 'html.parser')
        
        # finding relevant link information
        hemi = soup.find('div', class_='downloads').find_all('li')
        link = hemi[0].a['href']
        
        # formatting as a complete URL, appending to list
        img_url = f'https://marshemispheres.com/{link}'
        img_urls.append(img_url)
        
        # return browser to index to click next link
        browser.visit(marhem_url)
        
    # list comp to create hemisphere dictionary for each hemisphere
    hemisphere_data = [{'title': titles[n],'img_url': img_urls[n],'thumb': thumbnails[n]} for n in range(len(titles))]

    # browser.quit()

    # mars dict to export data

    mars = {
        'hemisphere_data': hemisphere_data,
        'mars_facts': mars_facts_html,
        'news_title': news_title,
        'news_p': news_p,
        'featured_img': featured_image_url,
    }
    
    # Run hemispheres function to create hemisphere lists
    return mars