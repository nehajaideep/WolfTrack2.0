import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re

URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"
page = requests.get(URL)
soup = BeautifulSoup(page.text, "html.parser")

def extract_job_title_from_result(soup): 
    jobs = []
    div=soup.find(name="div", attrs={"id":"mosaic-provider-jobcards"})
    a_ele_list=div.findAll("a",href=True)
    for a_ele in a_ele_list:
        ele=a_ele.find("h2", {"class": re.compile("jobTitle*")})
        if(ele!=None):
            title=ele.text
            href=a_ele["href"]