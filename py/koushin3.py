#サイトマップ生成用のページ格納辞書meta4.jsonのビルドプログラム
import json
import bs4
import glob
import os
import math
import datetime
import codecs
import re

def md2title(file_path,subject):
    try:
        # ファイルを開いて内容を読み込む
        with open(file_path, 'r', encoding='utf-8') as file:
            markdown_text = file.read()
        # 正規表現を使用してタイトルを抽出
        match = re.search(rf'{subject}:\s+(.*?)\s+', markdown_text)
        if match:
            title = match.group(1)
            return title
        else:
            return str(subject)
    except FileNotFoundError:
        return str(subject)
    
def main(file,files):
   #UnixTimeStamp取得
    ctime = math.floor(os.path.getctime(file)) #1679250555
    mtime = math.floor(os.path.getmtime(file))
    #UnixTimeStampの日付化
    cdate = datetime.datetime.fromtimestamp(ctime).date() #2023-03-20
    mdate = datetime.datetime.fromtimestamp(mtime).date()

    #タイトルの取得、タイトルがなければファイル名を入れる
    if os.path.splitext(file)[1] == ".html":

        soup = bs4.BeautifulSoup(open(file, mode= "r",encoding="utf-8"), 'html.parser')
        try: 
            title = str(soup.title.string)
        except AttributeError:
            title = "untitled"
        #説明の取得
        try: 
            content = soup.meta.get("content")
        except AttributeError:
            content = ""
        #ジャンルの取得
        try: 
            genre = soup.meta.get("genre")
        except AttributeError:
            genre = ""
        

        page = {
        "name":os.path.splitext(os.path.basename(file))[0],
        "ctime":str(ctime),
        "mtime":str(mtime),
        "cdate":str(cdate),
        "mdate":str(mdate),
        "title":title,
        "content":content,
        "genre":genre
        }
        dic.append(page)

    else:
        print("md")
        page = {
        "name":os.path.splitext(os.path.basename(file))[0],
        "ctime":str(ctime),
        "mtime":str(mtime),
        "cdate":str(cdate),
        "mdate":str(mdate),
        "title":md2title(file,"title"),
        "content":"content",
        "genre":md2title(file,"categories")
        }
        dic.append(page)

    

dic = []
files = glob.glob("*.html")
files += glob.glob("*.md")
for file in files:
    main(file,files)

json1 = codecs.open('./json/meta.json', "w", "utf-8")
json.dump(dic, json1, indent = 2, ensure_ascii=False)
json1.close()
