from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import html
from bs4 import BeautifulSoup
from urllib.parse import quote


class BypassedSearch(object):
    
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--incognito')
        self.driver = webdriver.Chrome(options=options)

    def searchusingscraper(self, name):
        trackName = quote(name)

        if trackName:
            url = 'https://www.youtube.com/results?search_query='
            generatedURL = url+trackName
            self.driver.get(generatedURL)
            time.sleep(3)
            divs = self.driver.find_element_by_xpath("//body/ytd-app/div[@id='content']/ytd-page-manager[@id='page-manager']/ytd-search[@class='style-scope ytd-page-manager']/div[@id='container']/ytd-two-column-search-results-renderer[@class='style-scope ytd-search']/div[@id='primary']/ytd-section-list-renderer[@class='style-scope ytd-two-column-search-results-renderer']/div[@id='contents']/ytd-item-section-renderer[@class='style-scope ytd-section-list-renderer']/div[3]")
            content = self.driver.execute_script("return arguments[0].innerHTML;", divs)
        else:
            print("URL not Generated")

            return "Failed To Generate URL"
        
        page = BeautifulSoup(content, 'html5lib')
        atags = page.findAll('a', attrs={'id': 'video-title'})
        
        videoLibrary = []
        cleanId = ''

        for eachTag in atags:
            if eachTag.get('href') != '' and '&list=' not in eachTag.get('href'):
                filteredTags = {}
                if '=' in eachTag.get('href'):  # Filtering out channels from the search
                    filteredTags['Name'] = eachTag.get('title')
                    cleanId = eachTag.get('href')
                    cleanId = cleanId.split("=")
                    filteredTags['VideoUrl'] = cleanId[1]
                    videoLibrary.append(filteredTags)
                    
        actualMatch = [] 
        relativeMatch = []

        for each in videoLibrary: # Title Matching
            if html.unescape(each['Name'].lower()) == name.lower():
                actualMatch.append(each['VideoUrl'])
            else:
                relativeMatch.append(each['VideoUrl'])

        if actualMatch:
            return actualMatch[0]  # return videoId from Here
        elif relativeMatch:
            return relativeMatch[0]  # return videoId from Here
        else:
            return "Video Not Found"

# byps = BypassedSearch()
# ur = byps.searchusingscraper('Tale of Us - Vinewood Blues')
# print(ur)