from selenium import webdriver 
from selenium.webdriver.chrome.options import Options  #importing the neccery file loaded the data with pandas and got 2 series asin and country
from bs4 import BeautifulSoup                          
import pandas as pd
from time import sleep
import re
import json 
from datetime import datetime as dt
chrome_options = Options()
chrome_deriver_path = r"C:\Users\anand nishad\Desktop\driver\chromedriver.exe"   # path of the chrome driver where it is save your directory 
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_deriver_path,options=chrome_options)



def remove_unwanted_values(s1):
    return s1.replace(" ","").replace("\u200f","").replace("\u200e","")


data = pd.read_csv(r"C:\Users\anand nishad\Downloads\Amazon Scraping.csv")    # file directory of the file of the data please change to your directory
asin = data["Asin"]
country = data["country"]                                                      
data_list = []
ct= 0
for i,j in zip(asin, country):
    if ct == 0:
        start_time = dt.now()
    elif(ct == 100):
        print(dt.now()-start_time,"---time took to complete 100 urls")       #  getting the time of a every 100 links
        ct = -1
    ct+=1

    start_url = f"https://www.amazon.{j}/dp/{i}"          # running the for loop over the link passing the country and asin in f string 
    try:
        
        driver.get(start_url)                             # getting the url with the selenium
        # print(start_url)
        # sleep(6)
        soup = BeautifulSoup(driver.page_source,"lxml")   # creating thr soup of source page
        name = soup.find("title").text
        # print(name)
        if "404" in name:                                 # getting all the links which show 404
            print("404  "+start_url)
            # continue
        print(name)
        s = re.split('condition=new"> <span',str(soup))   # getting the price from the soup
        price = re.search(r">(.*?)</span> </a> </span>",s[1]).group(1)
        print(price)
        product_details = soup.find("ul",class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list").find_all("span",class_="a-list-item")
        emp_string = ""                                    
        for i in product_details:
            i = remove_unwanted_values(i.text)            # getting the  product details fassing it into other funtion remove_unwanted_values to filter data
            emp_string+="".join(i.split("\n"))+",  "
        print(emp_string)

        ima = soup.find("div",{"id":"leftCol"}).find("img").get("data-a-dynamic-image")
        string_ = eval(ima)                               # getting the image link since there are more than on link 
        for i in string_:
            print(i)
            imag_data = i
            break
        data_list.append({start_url:{"Product Title":name,"Product Image URL":imag_data,"Price of the Product":price,"Product Details":emp_string}})
        # print({start_url:{"Product Title":name,"Product Image URL":imag_data,"Price of the Product":price,"Product Details":emp_string}})
        assert j in driver                               # append all the dictionrys in teh list and will later to convert in json
        
    except Exception as e:
        print(e)
driver.quit()

final_data = json.dumps(data_list, indent = 4)           # converting the list into json file
with open("amazon_products.json", "w") as outfile:
    outfile.write(final_data)                            #  it will save the file named as amazon_products in your loacal code