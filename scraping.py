# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set-up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page. search elements with div tag and list_text attribute, add 1 sec delay
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up HTML parser, assign varable to look for div tag and its descendent.
# . selects classes so div.list_text pinpoints the div tag with class of list_text.
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# begin scraping. chain .find to variable. This says look inside the variable for specific data.
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

# Find the relative image url. img tag nexted within this HTML so its included. .get('src') pulls the link to the image
# We are telling beautifulsoup to look inside img tag for an image with a class of fancybox-image. 
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

### Mars Facts

# create new dataframe from HTML table. Pandas read_html() searches and returns list of tables.
# Specifying index of 0, we are telling Pandas to pull only first table or first item in the list and turns into df.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

#copied from above
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df
# add .to_html() to convert df back to html ready code
df.to_html()

# end automated browsing session
browser.quit()

