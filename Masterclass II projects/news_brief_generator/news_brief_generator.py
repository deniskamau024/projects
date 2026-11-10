import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://newsapi.org/v2/everything"
api_key = os.getenv("NEWSAPI_API_KEY")

parameters = {
    "q":"sports",
    "language":"en",
    "pagesize":16,
    "apikey":api_key
}

response = requests.get(url,params=parameters)

if response.status_code == 200:
    news_data = response.json()
    articles = news_data.get("articles",[])

    print(f"------Fetched data: {len(articles)} Articles successfully")

    for index,articles in enumerate(articles,1):
        Title = articles.get("title","No Title")
        Source = articles.get("source",{}.get("name","unknown"))
        url = articles.get("url","#")


        print(f"{index} : {Title}")
        print(f"Source: {Source} | link: {url}/n")

elif response.status_code == 400:
    print(f"Bad request, check parameters:",{response.status_code})

elif response.status_code == 401:
    print(f"Unauthorized,please check your credentials:",response.status_code)

elif response.status_code == 404:
    print(f"Page not found:",response.status_code)

elif response.status_code == 429:
    print(f"Too many requests, please slow down:",response.status_code)

else:
    print(f"Server error:",response.status_code)

 
