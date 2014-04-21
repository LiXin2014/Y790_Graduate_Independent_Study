
from bs4 import BeautifulSoup
import urllib2, csv

#url is categories page link, this function will get final products link
def getCategories(url, lists):
    baseLink = "http://www.biocompare.com"
    print baseLink+url
    if(isProductPage(baseLink+url)):
        print "is product"
        lists.append(baseLink+url)
    else:
        try:
            print "not product"
            page = urllib2.urlopen(baseLink+url)
            soup = BeautifulSoup(page.read())
            links = soup.findAll("div", {"class" : "directoryModule module"}).pop().find_all('a')
            for link in links:
                #if(len(list(link.descendants))==1):
                print "link: ",link
                newLink = link.get('href')
                print "newLink: ",newLink
                if(isProductPage(baseLink+newLink)):
                    lists.append(baseLink+newLink)
                else:
                    getCategories(newLink, lists)
                
        except :
           print "Got URLError for: \t", url
    return lists

#url is products page, this function will go to each product page
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

#get company information from each product page
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

def removeBlankLines(txt):
    return ''.join([x for x in txt.split("\n") if x.strip()!=''])

# if url is a product page, return true, otherwise  return false
def isProductPage(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    review = soup.findAll("a", {"title" : "Write a Review"})
    if(review.__len__()==0):
        return False
    else:
        return True
    
def getURLS():  
    lists = []
    url1 = "/Apoptosis/"
    lists.append(url1)
    url2 = "/Assay-Kits/"
    lists.append(url2)
    url3 = "/BioImaging-Microscopy/"
    lists.append(url3)
    url4 = "/Blood-Tissue-Products/"
    lists.append(url4)
    url5 = "/6541-Cell-Biology/"
    lists.append(url5)
    url6 = "/Cloning-and-Expression/"
    lists.append(url6)
    url7 = "/Immunochemicals/"
    lists.append(url7)
    url8 = "/Lab-Automation-High-Throughput/"
    lists.append(url8)
    url9 = "/Lab-Equipment/"
    lists.append(url9)
    url10 = "/Molecular-Biology/"
    lists.append(url10)
    url11 = "/Molecular-Diagnostics/"
    lists.append(url11)
    url12 = "/Nucleic-Acid-Electrophoresis/"
    lists.append(url12)
    url13 = "/Nucleic-Acid-Purification/"
    lists.append(url13)
    url14 = "/PCR-Real-Time-PCR/"
    lists.append(url14)
    url15 = "/Protein-Biochemistry/"
    lists.append(url15)
    url16 = "/RNAi-Technology-siRNA-miRNA-shRNA/"
    lists.append(url16)
    url17 = "/Life-Science-Services/"
    lists.append(url17)
    url18 = "/Software/"
    lists.append(url18)
    url19 = "/9112-Tissue-Dissociation/"
    lists.append(url19)
    url20 = "/Translational-Research/"
    lists.append(url20)
    return lists
    
                  
def main():
    f = csv.writer(open("apoptosis_biocompare1.csv", "w"))
    f.writerow(["company name", "website", "address", "source"])
    urls = getURLS()
    for url in urls:
        lists = []
        getCategories(url, lists)
        for link in lists:
            products = getProducts(link)
            if(len(products)!=0):
                    for product in products:
                        list = getInformation(product)
                        if(len(list)!=0):
                            print "list: ",list
                            f.writerow([list[0], list[1], list[2], list[3]])
            
    
if __name__ == "__main__":
    main()