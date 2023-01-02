# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd 
import datetime as dt 

def scrape_all():
    # Initiate headless driver
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    # Set executable path and initialize the chrome browser in splinter 
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #browser = Browser('chrome', **executable_path)

    # Since these are pairs 
    news_title, news_paragraph= mars_news(browser)
    hemisphere_image_urls=hemisphere(browser)
    # Run all scraping functions and store results in dictionary 
    data={
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


## > SCRAPE MARS NEWS <

def mars_news(browser):

    # visit NASA website 
    url= 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Optional delay for website 
    # Here we are searching for elements with a specific combination of tag (ul) and (li) and attriobute (item_lit) and (slide)
    # Ex. being <ul class= "item_list">
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # HTML Parser. Convert the brpwser html to a soup object and then quit the browser
    html= browser.html 
    news_soup= soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        #slide_elem looks for <ul /> tags and descendents <li />
        # the period(.) is used for selecting classes such as item_list
        slide_elem= news_soup.select_one('ul.item_list li.slide')

        # Chained the (.find) to slide_elem which says this variable holds lots of info, so look inside to find this specific entity
        # Get Title
        news_title=slide_elem.find('div', class_= 'content_title').get_text()
        # Get article body
        news_p= slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None,None

    return news_title, news_p


## > SCRAPE FEATURED IMAGES <

def featured_image(browser):

    # Visit URL 
    url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mar'
    browser.visit(url)

    # Find and click the full_image button
    full_image_elem= browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that 
    # is_element_present_by_text() method to search for an element that has the provided text
    browser.is_element_present_by_text('more info', wait_time=1)

    # will take our string 'more info' and add link associated with it, then click
    more_info_elem=browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html=browser.html
    img_soup=soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url 
        # The 'figure.lede' references the <figure /> tag and its class=lede
        # the 'a' is the next tag nested inside the <figure /> tag, as well as the 'img' tag 
        # the .get('src') pulls the link to the image

        # WE are telling soup to go to figure tag, then within that look for an 'a' tag then within that look for a 'img' tag
        img_url_rel= img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None
    # Need to get the FULL URL: Only had relative path before
    img_url= f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url


## > SCRAPE FACTS ABOUT MARS <

def mars_facts():
    
    # Add try/except for error handling
    try:
        # Creating DF by telling function to look for first html table in site it encounters by indexing it to zero
        df=pd.read_html('http://space-facts.com/mars/')[0]

    # BaseException, catches multiple types of errors
    except BaseException:
        return None
    
    # Assigning columns, and set 'description' as index 
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    #Convert back to HTML format, add bootstrap
    return df.to_html()


## > SCRAPE HEMISPHERE <

def hemisphere(browser):
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    hemisphere_image_urls = []

    imgs_links= browser.find_by_css("a.product-item h3")

    for x in range(len(imgs_links)):
        hemisphere={}

        # Find elements going to click link 
        browser.find_by_css("a.product-item h3")[x].click()

        # Find sample Image link
        sample_img= browser.find_link_by_text("Sample").first
        hemisphere['img_url']=sample_img['href']

        # Get hemisphere Title
        hemisphere['title']=browser.find_by_css("h2.title").text

        #Add Objects to hemisphere_img_urls list
        hemisphere_image_urls.append(hemisphere)

        # Go Back
        browser.back()
    return hemisphere_image_urls

if __name__== "__main__":
    # If running as script, print scrapped data
    print(scrape_all())

    
# # Import Splinter, BeautifulSoup, and Pandas
# from splinter import Browser
# from bs4 import BeautifulSoup as soup
# import pandas as pd
# import datetime as dt
# from webdriver_manager.chrome import ChromeDriverManager


# def scrape_all():
#     # Initiate headless driver for deployment
#     executable_path = {'executable_path': ChromeDriverManager().install()}
#     browser = Browser('chrome', **executable_path, headless=True)

#     news_title, news_paragraph = mars_news(browser)

#     # Run all scraping functions and store results in a dictionary
#     data = {
#         "news_title": news_title,
#         "news_paragraph": news_paragraph,
#         "featured_image": featured_image(browser),
#         "facts": mars_facts(),
#         "last_modified": dt.datetime.now(),
#         'Cerberus Hemisphere Enhanced': https://marshemispheres.com/images/full.jpg,
#         'Schiaparelli Hemisphere Enhanced': https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg,
#         'Syrtis Major Hemisphere Enhanced': https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg,
#         'Valles Marineris Hemisphere Enhanced': https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg
#     }


#     # Stop webdriver and return data
#     browser.quit()
#     return data


# def mars_news(browser):

#     # Scrape Mars News
#     # Visit the mars nasa news site
#     url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
#     browser.visit(url)

#     # Optional delay for loading the page
#     browser.is_element_present_by_css('div.list_text', wait_time=1)

#     # Convert the browser html to a soup object and then quit the browser
#     html = browser.html
#     news_soup = soup(html, 'html.parser')

#     # Add try/except for error handling
#     try:
#         slide_elem = news_soup.select_one('div.list_text')
#         # Use the parent element to find the first 'a' tag and save it as 'news_title'
#         news_title = slide_elem.find('div', class_='content_title').get_text()
#         # Use the parent element to find the paragraph text
#         news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

#     except AttributeError:
#         return None, None

#     return news_title, news_p


# def featured_image(browser):
#     # Visit URL
#     url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
#     browser.visit(url)

#     # Find and click the full image button
#     full_image_elem = browser.find_by_tag('button')[1]
#     full_image_elem.click()

#     # Parse the resulting html with soup
#     html = browser.html
#     img_soup = soup(html, 'html.parser')

#     # Add try/except for error handling
#     try:
#         # Find the relative image url
#         img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

#     except AttributeError:
#         return None

#     # Use the base url to create an absolute url
#     img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

#     return img_url

# def mars_facts():
#     # Add try/except for error handling
#     try:
#         # Use 'read_html' to scrape the facts table into a dataframe
#         df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

#     except BaseException:
#         return None

#     # Assign columns and set index of dataframe
#     df.columns=['Description', 'Mars', 'Earth']
#     df.set_index('Description', inplace=True)

#     # Convert dataframe into HTML format, add bootstrap
#     return df.to_html(classes="table table-striped")
# #----------------Mars Hemisphere Scraping------------------------------
# def hemisphere_scrape(browser) :
#     # 1. Use browser to visit the URL 
#     url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#     browser.visit(url)
#     browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
#     # 2. Create a list to hold the images and titles.
#     hemisphere_image_urls = []
#     # 3. Write code to retrieve the image urls and titles for each hemisphere.
#     # Parse the html with beautifulsoup
#     html = browser.html
#     hemi_soup = soup(html, 'html.parser')

#     # Get the links for each of the 4 hemispheres
#     hemi_links = hemi_soup.find_all('h3')
#     # hemi_links

#     # loop through each hemisphere link
#     for hemi in hemi_links:
#         # Navigate and click the link of the hemisphere
#         img_page = browser.find_by_text(hemi.text)
#         img_page.click()
#         html= browser.html
#         img_soup = soup(html, 'html.parser')
#         # Scrape the image link
#         img_url = 'https://astrogeology.usgs.gov/' + str(img_soup.find('img', class_='wide-image')['src'])
#         # Scrape the title
#         title = img_soup.find('h2', class_='title').text
#         # Define and append to the dictionary
#         hemisphere = {'img_url': img_url,'title': title}
#         hemisphere_image_urls.append(hemisphere)
#         browser.back()
#         # print(hemisphere_image_urls)
#     return hemisphere_image_urls

# #----------------Ending Code ------------------------------------------
# if __name__ == "__main__":
#     # If running as script, print scraped data
#     print(scrape_all())

# if __name__ == "__main__":

#     # If running as script, print scraped data
#     print(scrape_all())