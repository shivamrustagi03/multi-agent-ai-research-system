import os
from langchain.tools import tool
import requests # Web Scrapping
from bs4 import BeautifulSoup
from tavily import TavilyClient 
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# To create an agent , We have to create Functions .

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Return Titles , Urls and Snippets"""
     # This triple string is used to tell LLM , What this tool is going to do  etc....
    results = tavily.search(query=query, max_results=5)
    
    # Now we want to save results in proper form .

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\n URL : {r['url']}\n Snippet: {r['content'][:300]}\n"
        )

    return "\n---\n".join(out)

print(web_search.invoke("What is the Recent Tools in AI")) 

@tool
def scrape_url(url: str)-> str:
    """Scrape and return clean text content from given URL for deeper reading"""
    try:
        resp = requests.get(url, timeout=8,headers={"Users-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text,"html.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL:{str(e)}" 

print(scrape_url.invoke("https://www.marketermilk.com/blog/ai-marketing-tools"))