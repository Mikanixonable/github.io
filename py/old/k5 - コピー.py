import json
import glob
import os
import codecs
from PIL import Image

def makeName(name):
    return os.path.splitext(os.path.basename(name))[0]

def new(illust,illusts):
    png = {
        "name":os.path.splitext(os.path.basename(illust))[0],
        "title":"",
        "description":"",

        "date":"",
        "licence":"",
        "link":"",
        "series":[],
        "tags":[],
        "colors":[],
    }
    illusts.append(png)

def update(illust,illusts):
    img = Image.open("./illusts/{}.png".format(illust["name"]))
    illust["width"] = img.width
    illust["height"] = img.height



f = codecs.open('./json/illusts.json', "r", "utf-8")
illusts = json.load(f)
nameList = [illust1.get('name') for illust1 in illusts]
f.close()

nameList2 = list(map(makeName, glob.glob("./illusts/*.png")))
newList = [x for x in nameList2 if x not in nameList]
print(newList)

for illust in nameList2:
    new(illust,illusts)

for illust in illusts:
    update(illust,illusts)


f = codecs.open('./json/illusts.json', "w", "utf-8")
json.dump(illusts, f, indent = 2, ensure_ascii=False)
f.close()
