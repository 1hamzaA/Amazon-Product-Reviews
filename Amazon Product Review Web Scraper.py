## Import Libraries

import requests
from bs4 import BeautifulSoup 
import pandas as pd
from selenium import webdriver

## Setup Webdriver 

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("C:/Users/xxx/chromedriver.exe")


## Create Functions for Extracting Target Data

def getAmazonSearch(search_query):
    url="https://www.amazon.co.uk/s?k="+search_query
    page = driver.get(url)
    return driver.page_source
    print(url)
    print(page)


def Searchasin(asin):
    url="https://www.amazon.co.uk/dp/"+asin
    page = driver.get(url)
    return driver.page_source

def Searchreviews(review_link):
    url="https://www.amazon.co.uk"+review_link
    page = driver.get(url)
    return driver.page_source


# Create list of products (using ASINs) for which reviews shall be extracted
    
ASINS=[]
response=getAmazonSearch('cricket+bat')  # Searching Amazon for Cricket Bats
soup=BeautifulSoup(response, "lxml")

for i in soup.findAll("div",{'class':"sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20"}):
    ASINS.append(i['data-asin'])   
for i in soup.findAll("div",{'class':"sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"}):
    ASINS.append(i['data-asin'])    


# Create list of urls for product review pages

ProductReviewLinks=[]

for i in range(len(ASINS)):
    print(str(i+1)+":"+str(len(ASINS)))
    response=Searchasin(ASINS[i])
    soup=BeautifulSoup(response, "lxml")
    for i in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
        ProductReviewLinks.append(i['href'])    
print(ProductReviewLinks) 

      
# Extracting various data from product review pages


ProductName=[]
SellerName=[]
ReviewRating=[]
ReviewComment=[]

for j in range(len(ProductReviewLinks)):
    for k in range(1):
        response=Searchreviews(ProductReviewLinks[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response, "lxml")
        
        for i in soup.findAll("a",{'data-hook':"product-link"}):                     # Extracting Product Listing Name
            print(i)
            
            for j in soup.findAll("a",{'class':"a-size-base a-link-normal"}):        # Extracting Product Seller Name
                print(j)
            
                for k in soup.findAll("i",{'data-hook':"review-star-rating"}):       # Extracting Product Review Rating
                    print(k)    
                    
                    for l in soup.findAll("span",{'data-hook':"review-body"}):       # Extracting Product Review Text
                        print(l)
                        
                        ProductName.append(i.text.split("\n"))  
                        SellerName.append(j.text.split("\n")) 
                        ReviewRating.append(k.text.split("\n"))  
                        ReviewComment.append(l.text.split("\n"))  
                        

# Reshaping all extracted data into a datafram    
            
df = pd.DataFrame({'Product Title': ProductName, 'Seller Name': SellerName, 'Review':ReviewComment, 'Rating':ReviewRating})
df=  df.apply(lambda x: x.replace('[','').replace(']','')) 

print(df)
df = df.reset_index()
df.to_csv(r'C:\Users\xxx\Raw Data.csv', index=False)    
