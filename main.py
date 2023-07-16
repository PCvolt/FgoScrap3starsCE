import re
import requests
from bs4 import BeautifulSoup

# Using the <tbody> in https://gamepress.gg/grandorder/craft-essences

class CraftEssence:
    name = ""
    img_url = ""
    star_rating = 0

    def __init__(self, name, img_url, star_rating):
        self.name = name
        self.remove_invalid_chars()
        self.img_url = img_url
        self.star_rating = star_rating

    def remove_invalid_chars(self):
        pattern = r'[<>:"/\\|?*]'
        self.name = re.sub(pattern, '', self.name)

    def download(self):
        img_data = requests.get(self.img_url).content
        with open("img/" + self.name + ".png", "wb") as file:
            file.write(img_data)
            print("Image downloaded:", img_url)


### DEFINITIONS
def find_name(tr):
    a_tag = tr.find("span", class_="essence-list-title").find("a")
    name = a_tag.get_text(strip=True)
    return name

def find_img_url(tr):
    img_tag = tr.find("img", class_="essence-icon")
    img_url = img_tag["src"]
    return "https://gamepress.gg" + img_url

def find_star_rating(tr):
    star_rating = tr.find("div", class_="essence-deck").text
    if star_rating == "":
        star_rating = "0"
    return star_rating

def get_list_of_3stars_ce():
    # param craftEssenceList, then add
    return soup.find_all("i", class_="star-3")

### MAIN

with open("CE_list.txt", "rb") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")
tr_elements = soup.find_all("tr")

# Fill the list of all exising Craft Essences
craftEssenceList = []
for tr in tr_elements:
    name = find_name(tr)
    img_url = find_img_url(tr)
    star_rating = find_star_rating(tr)

    craftEssenceList.append(CraftEssence(name, img_url, int(star_rating)))

# Narrow it down to 3 stars
craftEssenceList3stars = []
for ce in craftEssenceList:
    if ce.star_rating == 3:
        craftEssenceList3stars.append(ce)

for ce3 in craftEssenceList3stars:
    ce3.download()
