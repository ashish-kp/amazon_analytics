import requests
from bs4 import BeautifulSoup

# Setting the useragent so that Amazon.in doesn't drop our http requests.
headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  
}
def getKeywords():
    keyList = []
    keyCount = 1
    while True:
        key = str(input(str(keyCount) + ") "))
        if(key == ''):
            break
        else:
            if not all(chr.isalnum() or chr.isspace() for chr in key):
                print("The entered string contains not alphanumeric characters...")
            else:
                key = key.strip()
                key = key.replace(' ', '+')
                keyList.append(key)
                keyCount = keyCount + 1
    return keyList

def getUrls(keyList):
    totPages = 20 # When you enter a keyword in amazon.in's search, it will produce 20 pages of products... 
    urls = []
    for key in keyList:
        for pageNumber in range(1, totPages + 1):
            url = 'https://www.amazon.in/s?k=' + key + \
                '&ref=nb_sb_noss_2&page=' + str(pageNumber)
            page = requests.get(
                url, headers=headers)
            soup = BeautifulSoup(page.content, 'html5lib')
            productsUrl = soup.findAll('h2', {"class": ['a-size-mini', 'a-spacing-none', 'a-color-base', 's-line-clamp-2']})
            print(productsUrl)
            urls.append(productsUrl)
    return productsUrl

keyList = getKeywords()
urls = getUrls(keyList)
print(urls)