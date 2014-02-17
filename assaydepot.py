'''
Created on Feb 15, 2014

@author: Xin
'''

#problem: unicode italian letter 
from bs4 import BeautifulSoup
import urllib2, re, csv

def rightFormatOfP(des):
    d = des.contents
    text = des.get_text()
    if(len(d) != 0):
        if(d[0] == text):
            return True
        else:
            return False
        return False
    
def main():
    opener = urllib2.build_opener()
    opener.addheaders = [("User-agent", "xinlibot/0.1 (Xin Li)")]
    url = "https://www.assaydepot.com/providers"
    basicUrl = "https://www.assaydepot.com"
    f=csv.writer(open("assaydepot1.csv", "w"))
    f.writerow(["Name", "website", "address", "description", "source"])
    page = opener.open(url)
    soup = BeautifulSoup(page.read())
    letterPage = soup.findAll('a', href=re.compile('/providers\?letter=(.|other)$'))
    source = "https://www.assaydepot.com"
    for eachPage in letterPage:
        eachLink = eachPage.get('href')
        anotherPage = opener.open(basicUrl+eachLink)
        soup = BeautifulSoup(anotherPage.read())
        providers = soup.findAll("a", {"class" : "provider"})
        for link in providers:
            fullLink = basicUrl+link.get('href')
            vendorPage = opener.open(fullLink)
            soup = BeautifulSoup(vendorPage.read())
            try:
                name = soup.findAll('h1').pop().contents[0]
            except:
                print "bad character"
                continue
            description = soup.findAll('p')
            for des in description:
                if(rightFormatOfP(des)):
                    descrip = des.get_text() 
        
            tbody = soup.findAll('tbody')    
            tds = tbody.pop().findAll('td')
            try:
                website = str(tds[2].get_text())
                address = str(tds[3].get_text())
            except:
                print "bad tr string"
                continue
            try:
                #f.writerow([name, website, address])
                f.writerow([name, website, address, descrip, source])
            except:
                print "bad character"
                continue
            #f.writerow([descrip, source])
        
if __name__ == "__main__":
    main()
