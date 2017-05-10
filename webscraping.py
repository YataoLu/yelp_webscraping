# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 19:14:00 2016

@author: Yatao Lu - G30068641


this program is about web scrapying and it scrpe the data from yelp.com
 for the maexcian and chinese resturant nearby 
"""
import urllib.request
from bs4 import BeautifulSoup as bs


outputFileName = "chinese.csv"
def extractIntegerFromString(someString):
    ret = None
    for s in someString.split():
        if(s.isdigit()):
            ret = s
    return ret

def findTagWithClass(parent, tagName, className):
    ret = None
    for div in parent.findAll(tagName):
        if(div.get('class') != None):
            if(div['class'][0] == className):
                ret = div
                break
    return ret

def scrapUrl(url, writer):
    numProcessed = 0
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = response.read()
    response.close()

    soup = bs(data, "html.parser")

    listItems = soup.findAll('li')
    for tag in listItems:
        if(tag.get('class') != None):
            if(tag['class'][0] == 'regular-search-result'):
                goodData = True
                numProcessed = numProcessed + 1
                try:
                    #bizListingTag = tag.contents[1].contents[1]
                    mainAttrTag = tag.contents[1].contents[1].contents[1]
                    secAttrTag = tag.contents[1].contents[1].contents[3]
                    mediaStoryTag = mainAttrTag.contents[1].contents[3]

                    nameTag = mainAttrTag.contents[1].contents[3].h3.span.a.span
                    name = nameTag.text
                    name = name.replace(',', '')

                    #for div in mediaStoryTag.findAll('div'):
                    #    print(div['class'])
                    ratingReviewTag = findTagWithClass(mediaStoryTag, 'div', 'biz-rating')
                    if(ratingReviewTag != None):
                        #print(ratingReviewTag.prettify())
                        ratingTag = ratingReviewTag.div.i
                        rating = ratingTag['title'][0:3]
                        reviewTag = ratingReviewTag.span
                        reviewString = reviewTag.get_text()
                        review = extractIntegerFromString(reviewString)
                    else:
                        rating = '0'
                        review = 0
                    priceRangeTag = findTagWithClass(mediaStoryTag, 'div', 'price-category')
                    if(priceRangeTag != None):
                        bulletAfterTag = findTagWithClass(priceRangeTag, 'span', 'bullet-after')
                        if(bulletAfterTag != None):
                            priceRange = len(bulletAfterTag.span.text)
                        else:
                            priceRange = 0
                    else:
                        priceRange = 0



                    if(secAttrTag.address == None):
                        streetAddress = None
                        city = None
                        state = None
                        zipCode = None
                    else:
                        addressTag = secAttrTag.address
                        if(addressTag.br == None):
                            streetAddress = None;
                            cityStateZipString = addressTag.contents[0].strip()
                            cszComps = cityStateZipString.split(',')
                            city = cszComps[0].strip()
                            city = city.replace(',', '')
                            szComps = cszComps[1].split()
                            state = szComps[0].strip()
                            state = state.replace(',', '')
                            zipCode = szComps[1].strip()
                            zipCode = zipCode.replace(',', '')
                        else:
                            streetAddress = addressTag.contents[0].strip()
                            streetAddress = streetAddress.replace(',', '')
                            cityStateZipString = addressTag.br.text
                            cszComps = cityStateZipString.split(',')
                            city = cszComps[0].strip()
                            city = city.replace(',', '')
                            szComps = cszComps[1].split()
                            state = szComps[0].strip()
                            state = state.replace(',', '')
                            zipCode = szComps[1].strip()
                            zipCode = zipCode.replace(',', '')

                    #print(secAttrTag.prettify())
                    spans = secAttrTag.findAll('span')
                    for span in spans:
                        if(span['class'][0] == 'biz-phone'):
                            phoneTag = span
                    phoneNumber = phoneTag.text.strip()
                    phoneNumber = phoneNumber.replace(',', '')
                    #print(phoneNumber)
                except Exception as e:
                    print(e)
                    goodData = False

                if(goodData):
                    s = '{},{},{},{},{},{},{},{},{}\n'.format(name, streetAddress, city, state, zipCode, phoneNumber, review, rating, priceRange)
                    writer.write(s)

    if(numProcessed == 0):
        print('hit end')
        return True
    else:
        return False



#urlPrefix = 'https://www.yelp.com/search?find_desc=mexican+food&find_loc=Washington,+DC&start='
urlPrefix = 'https://www.yelp.com/search?find_desc=chinese+food&find_loc=Washington,+DC&start='
start = 0
hitEnd = False
with open(outputFileName, "w") as writer:
    s = 'Restaurant name,Street address,City,State,Zip,Phone,Number of reviews, Rating, Price range\n'
    writer.write(s)
    url = urlPrefix + str(start)
    #scrapUrl(url, writer)
    while(hitEnd == False):
    #for i in range(0,10):
        print('processing {}-{}'.format(start, start + 9))
        url = urlPrefix + str(start)
        hitEnd = scrapUrl(url, writer)
        start = start + 10
