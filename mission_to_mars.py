# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set up the executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

#assign the summary and title text to variables to reference later
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

table_scrape_df = pd.read_html('https://galaxyfacts-mars.com')[0]
table_scrape_df.columns=['description', 'Mars', 'Earth']
table_scrape_df.set_index('description', inplace=True)
table_scrape_df

# lists table element with all the nested values
table_scrape_df.to_html()


url = 'https://marshemispheres.com/'

browser.visit(url)


hemisphere_image_urls=[]
links = browser.find_by_css("a.product-item img")
for i in range(len(links)):
    hemisphere={}
    browser.find_by_css("a.product-item img")[i].click()
    sample=browser.links.find_by_text("Sample").first
    hemisphere["img_url"]=sample["href"]
    hemisphere["title"]=browser.find_by_css("h2.title").text
    hemisphere_image_urls.append(hemisphere)
    browser.back()


hemisphere_image_urls

# quit the scraping
browser.quit()