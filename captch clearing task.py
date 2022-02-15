from selenium import webdriver     # importing necesst librery an modules
import requests
import pytesseract
import cv2
from bs4 import BeautifulSoup
from time import sleep

path = r"C:\Users\anand nishad\Desktop\driver\chromedriver.exe"   # please change the to your path of the your address
website = "https://www.amazon.com/errors/validateCaptcha"
driver = webdriver.Chrome(path)
driver.get(website)
html = driver.page_source
soup = BeautifulSoup(html,"lxml")
# print(soup)
image = soup.find("img").get("src")                  
image_source = requests.get(image).content                        #downloading the image to pass in tessect in order to get into text
with open('anand.jpg','wb') as f:
    f.write(image_source)
img = cv2.imread('anand.jpg')
img = cv2.resize(img, (200, 70))

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'    # please add your path of pytessseract
the_captch_words = pytesseract.image_to_string(img)
print(the_captch_words)                                                       # teh converted text will print here 
sleep(4)
driver.find_element_by_id("captchacharacters").send_keys(the_captch_words)
driver.find_element_by_class_name("a-button-text").click()
