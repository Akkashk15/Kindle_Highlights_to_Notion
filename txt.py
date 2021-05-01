from collections import defaultdict
import collections
import sys
import os
from notion.utils import get_embed_data 
import requests


name=sys.argv[1]
token_v2=sys.argv[2]
page_link=sys.argv[3]


with open('./uploads/'+name,mode='r', encoding='utf-8-sig') as f:
    lines = [line.rstrip() for line in f]
n=len(lines)

new_highlight=True
i=0
data={
}
while(i<n):
    if(lines[i]=="=========="):
        i=i+1
        new_highlight=True
        continue
    if(new_highlight):
        # contains book name
        temp=lines[i]
        book_name=""
        book_author=""
        m=len(temp)
        j=0
        while(j<m):
            if(temp[j]=='('):
                j=j+1
                while(j<m):
                    if(temp[j]==')'):
                        break
                    book_author+=temp[j]
                    j=j+1
                break
            else:
                book_name+=temp[j]
            j=j+1
        #second line contains details of highlights
        i=i+1
        #TODO
        #third line contains nothing
        i=i+1
        #fourth line contains actual highlight
        i=i+1

        highlight=""
        while(i<n):
            if(lines[i]=="=========="):
                break
            else:
                highlight+=lines[i]
                i=i+1
        data.setdefault(book_name, []).append(highlight)
        new_highlight=False
    else:
        i=i+1


import random
from notion.client import NotionClient
from notion.block import EmbedOrUploadBlock, HeaderBlock, TodoBlock, SubheaderBlock
from notion.block import BulletedListBlock
from notion.block import NumberedListBlock
from notion.block import PageBlock
from notion.block import ImageBlock
from notion.block import BasicBlock
from notion.block import CollectionViewBlock,VideoBlock


def get_collection_schema():
    return {        
        "title": {"name": "Name", "type": "title"},
        "text": {"name": "Author", "type": "text"},
        "%9:q": {"name": "Read", "type": "checkbox"},
        "4Jv$": {"name": "Pages", "type": "number"},
        "rate": {"name": "Rating", "type": "number"},
        "=d{|": {
            "name": "Categories",
            "type": "multi_select",
            "options": [
                {
                    "color": "Fiction",
                    "id": "79560dab-c776-43d1-9420-27f4011fcaec",
                    "value": "A",
                },
                {
                    "color": "Non-Fiction",
                    "id": "002c7016-ac57-413a-90a6-64afadfb0c44",
                    "value": "B",
                },
            ],
        },
    }

google_api_key=os.environ.get("GOOGLE_API_KEY")


def youtube_search(book_name):
    print(google_api_key)
    parms={"part":"snippet","maxResults":10,"q":book_name,"key":google_api_key}
    r=requests.get(url="https://www.googleapis.com/youtube/v3/search",params=parms)
    rj=r.json()
    video_id="dQw4w9WgXcQ"  
    for i in rj["items"]:
        try:
            type=repr(i["id"]["kind"])
            if(type=="youtube#channel"):
                continue
            video_id=repr(i["id"]["videoId"])
        except:
            pass
    if video_id.startswith("'") and video_id.endswith("'"):
        video_id = video_id[1:-1]
    if video_id.startswith('"') and video_id.endswith('"'):
        video_id = video_id[1:-1]
    video_id="https://www.youtube.com/watch?v="+video_id
    return video_id

def search(book_name):
    print(google_api_key)
    parms={"q":book_name,"key":google_api_key}
    r=requests.get(url="https://www.googleapis.com/books/v1/volumes",params=parms)
    rj=r.json()
    book_description='No book description found.'
    book_page_count=0
    book_author="Unknown"
    average_rating=0
    categories="Unknown"    

    image_link="https://mediamodifier.com/blog/wp-content/uploads/2020/02/11-square-book-cover-mockup.jpg"
    for i in rj["items"]:
        try:
            categories=repr(i["volumeInfo"]["categories"][0])
        except:
            pass
        try:
            average_rating=repr(i["volumeInfo"]["averageRating"])
        except:
            pass
        try:
            book_author=repr(i["volumeInfo"]["authors"][0])
        except:
            pass
        try:
            book_page_count=repr(i["volumeInfo"]["pageCount"])
        except:
            pass
        try:
            book_description=repr(i["volumeInfo"]["description"])
        except:
            pass     
        break
    return book_description,image_link,book_author,book_page_count,average_rating,categories


client = NotionClient(token_v2=token_v2)

# Access a database using the URL of the database page or the inline block
page = client.get_block(page_link)


page.title="Kindle Highlights"
page.set("format.page_cover","https://www.incimages.com/uploaded_files/image/1920x1080/getty_598063032_349381.jpg")
page.icon="https://i.pinimg.com/originals/2c/fc/93/2cfc93d7665f5d7728782700e50596e3.png"
cvb = page.children.add_new(CollectionViewBlock)
cvb.collection = client.get_collection(
    client.create_record("collection", parent=cvb, schema=get_collection_schema())
)
cvb.title = "Read them!"
view = cvb.views.add_new(view_type="table")
gallery_view = cvb.views.add_new(view_type="gallery")

for book in data.keys():
    print(book)
    #col=collection.
    row=cvb.collection.add_row()
    row.name=book    
    book_description,image_link,book_author,page_count,average_rating,book_categories=search(book)
    if image_link.startswith("'") and image_link.endswith("'"):
        image_link = image_link[1:-1]
    if image_link.startswith('"') and image_link.endswith('"'):
        image_link = image_link[1:-1]

    if book_author.startswith("'") and book_author.endswith("'"):
        book_author = book_author[1:-1]
    if book_author.startswith('"') and book_author.endswith('"'):
        book_author = book_author[1:-1]

    if book_categories.startswith("'") and book_categories.endswith("'"):
        book_categories = book_categories[1:-1]
    if book_categories.startswith('"') and book_categories.endswith('"'):
        book_categories = book_categories[1:-1]

    row.set_property("author",book_author)
    #print(page_count)
    row.set_property("pages",int(page_count))
    row.set_property("rating",float(average_rating))
    row.read=True

    row.categories=[book_categories]
    row.set("format.page_cover",image_link)
    

    row.children.add_new(SubheaderBlock,title="Book Description")
    row.children.add_new(BulletedListBlock,title=book_description)

    row.children.add_new(SubheaderBlock,title="Relevant Youtube Video")
    youtube_video=youtube_search(book)
    video = row.children.add_new(VideoBlock, width=300)
    video.set_source_url(youtube_video)

    row.children.add_new(SubheaderBlock,title="Book Highlights")
    for highlight in data[book]:
        newHighlight = row.children.add_new(NumberedListBlock, title=highlight)


