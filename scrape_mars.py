def scrape():
    from bs4 import BeautifulSoup
    import requests

    #You'll see these again later on because those were written first.
    #Then this was added to debug. Because something here keeps making a 
    #dict key of 0. 
    import re
    import time
    import pandas as pd
    from splinter import Browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #MARS NEWS
    #================================================
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url, allow_redirects=True)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Give me all the news article slides
    scraped_slides = soup.find_all("div", {'class':'slide'})


    # In[3]:


    #Refine and store all the article titles and brief summaries into mars_news 
    mars_news = []
    for slide in scraped_slides:
        title = slide.find('div', {'class':'content_title'}).find('a').text.strip()
        content = slide.find('div', {'class':'rollover_description_inner'}).text.strip()
        item = {'title': title, 'content': content}
        mars_news.append(item)



    #JPL Featured Space Image
    #================================================
    from splinter import Browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[5]:


    #go to the website
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url) 


    # In[6]:


    #click click click to find full image
    browser.click_link_by_partial_text('FULL')
    import time
    time.sleep(2)
    browser.click_link_by_partial_text('more info')


    # In[7]:


    #Get that URL
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_src = soup.find('img',{'class':"main_image"})['src']
    featured_image_url = "https://www.jpl.nasa.gov" + img_src


    # In[8]:


    #MARS WEATHER
    #================================================
    url = 'https://twitter.com/marswxreport?lang=en/'
    response = requests.get(url, allow_redirects=True)
    soup = BeautifulSoup(response.text, 'html.parser')


    # In[9]:


    #Get me the tweet with the latest weather
    import re
    mars_weather = soup.find(text=re.compile(r"InSight sol"))


    # In[10]:


    #MARS FACTS
    #================================================
    import pandas as pd
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    table = tables[1]

    transposed_table = table.T

    #Making the first row into column headers
    transposed_table.columns = transposed_table.iloc[0]
    transposed_table = transposed_table[1:]

    dict_table = transposed_table.to_dict(orient='records')
    mars_facts = dict_table


    # In[12]:


    #MARS HEMISPHERES
    #================================================
    hemisphere_image_urls = []
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url) 
    time.sleep(1)


    # In[13]:


    hemispheres = ['Cerberus','Schiaparelli','Syrtis','Valles']
    hemisphere_image_urls = []

    #Lets go! Run the loop and get all the goodies
    browser.visit(url) 
    for hemisphere in hemispheres:
        browser.click_link_by_partial_text(hemisphere)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2').text
        img_url = soup.find('a',text=re.compile(r"Sample"))['href']
        found = {'title':title, 'img_url':img_url}
        hemisphere_image_urls.append(found)
        browser.back()
        time.sleep(1)

    compiled = {\
        'mars_news':mars_news,\
        'featured_image_url':featured_image_url,\
        'mars_weather':mars_weather,\
        'mars_facts':mars_facts,\
        'hemisphere_image_urls':hemisphere_image_urls}

    browser.quit()


    # compiled = {
    #     'featured_image_url':featured_image_url}
    # #     'mars_weather':mars_weather,\
    # #     'mars_facts':mars_facts,\
    # #     'hemisphere_image_urls':hemisphere_image_urls}
    return compiled
