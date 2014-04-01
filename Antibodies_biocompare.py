'''
Created on Mar 11, 2014

@author: Xin
'''
from bs4 import BeautifulSoup
import urllib2, csv

def getCategories(url):
    #url = "http://www.biocompare.com/1997-BrowseCategory/browse/gb1/9776/all"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    categories = soup.findAll("div", {"id" : "ctl05_ctl00_ctl00_guidedBrowseResults"})
    baseLink = "http://www.biocompare.com"
    list = []
    for category in categories:
        for eachCate in category.find_all('a'):
            eachCate = eachCate.get('href')
            #print baseLink+eachCate
            list.append(baseLink+eachCate)  
    print "inside categories",list 
    return list

def getDetailCategories(url):
    #url = "http://www.biocompare.com/1997-BrowseCategory/browse/gb1/9776/all"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    categories = soup.findAll("div", {"id" : "ctl05_ctl00_ctl00_guidedBrowseResults"})
    baseLink = "http://www.biocompare.com"
    list = []
    for category in categories:
        for eachCate in category.find_all('a'):
            eachCate = eachCate.get('href')
            #print baseLink+eachCate
            list.append(baseLink+eachCate)  
    print "inside detail categories",list            
    return list

def getProducts(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    links = soup.findAll("div", {"class" : "product"})
    baseLink = "http://www.biocompare.com"
    list = []
    for link in links:
        for eachLink in link.find_all('a'):
            eachOne = eachLink.get('href')
            #print baseLink+eachOne
            list.append(baseLink+eachOne)  
    print "inside product",list 
    return list

def removeBlankLines(txt):
    return ''.join([x for x in txt.split("\n") if x.strip()!=''])

def getInformation(url):
    print "inside get information from ", url
    list = []
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        #get the name of company
        name = soup.findAll("a", {"id" : "lnkVendorProfile"}).pop().get_text()
        list.append(name)
        #get the website of company
        website = soup.findAll("div", {"class" : "website"}).pop().get_text()
        website = removeBlankLines(website).replace("Website: ", "").replace("\t", "")
        list.append(website)
        #get the address of company
        address = soup.findAll("div", {"class" : "adr"})
        address = removeBlankLines(address.pop().get_text()).replace("\t", "").replace("\u000d", "")
        address = ', '.join(address.splitlines())
        list.append(address)
        source = "http://www.biocompare.com"
        list.append(source)
    except :
        print "Got URLError for: \t", url
    return list
    
   

def main():
    url = "http://www.biocompare.com/1997-BrowseCategory/browse/gb1/9776/all"
    f = csv.writer(open("antibodies_biocompare.csv", "w"))
    f.writerow(["company name", "website", "address", "source"])
    categories = getCategories(url)
    lists = []
    for link in categories:
        detailCategories = getDetailCategories(link)
        for link in detailCategories:
            products = getProducts(link)
            if(len(products)!=0):
                for product in products:
                    list = getInformation(product)
                    if(len(list)!=0):
                        #print list
                        lists.append(list)
                        f.writerow([list[0], list[1], list[2], list[3]])
#     print "start writing"
#     for item in lists:
#         if item[0] in sets:
#             continue
#         else:
#             f.writerow([item[0], item[1], item[2], item[3]])
#     
            
if __name__ == "__main__":
    main()
