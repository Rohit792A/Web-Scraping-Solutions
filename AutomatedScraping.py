import asyncio
import pprint
import pandas as pd

from autoscraper import AutoScraper

from bs4 import BeautifulSoup

import nest_asyncio
nest_asyncio.apply()

from playwright.async_api import async_playwright


from pydantic import BaseModel

import os

# from dotenv import load_dotenv
# load_dotenv()
import langchain
from langchain.chains import (create_extraction_chain,
                              create_extraction_chain_pydantic)
from langchain_openai import ChatOpenAI


# -------------------------------------------------------------------------------------------
openai_api_key = "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"

# -------------------------------------------------------------------------------------------


def remove_unwanted_tags(html_content, unwanted_tags=["script", "style"]):
    """
    This removes unwanted HTML tags from the given HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)



def remove_unessesary_lines(content):
    # Split content into lines
    lines = content.split("\n")

    # Strip whitespace for each line
    stripped_lines = [line.strip() for line in lines]

    # Filter out empty lines
    non_empty_lines = [line for line in stripped_lines if line]

    # Remove duplicated lines (while preserving order)
    seen = set()
    deduped_lines = [line for line in non_empty_lines if not (
        line in seen or seen.add(line))]

    # Join the cleaned lines without any separators (remove newlines)
    cleaned_content = "".join(deduped_lines)

    return cleaned_content


def extract_tags(html_content, tags: list[str]):
    """
    This takes in HTML content and a list of tags, and returns a string
    containing the text content of all elements with those tags, along with their href attribute if the
    tag is an "a" tag.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_parts = []

    for tag in tags:
        elements = soup.find_all(tag)
        for element in elements:
            # If the tag is a link (a tag), append its href as well
            if tag == "a":
                href = element.get('href')
                if href:
                    text_parts.append(f"{element.get_text()} ({href})")
                else:
                    text_parts.append(element.get_text())
            else:
                text_parts.append(element.get_text())

    return ' '.join(text_parts)



# edit tags to div, tr, th, li, ul, etc...
async def ascrape_playwright(url, tags: list[str] = ["h1", "h2", "h3", "span"]) -> str:
    """
    An asynchronous Python function that uses Playwright to scrape
    content from a given URL, extracting specified HTML tags and removing unwanted tags and unnecessary
    lines.
    """
    # print("Started scraping...")
    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url)

            page_source = await page.content()

            results = remove_unessesary_lines(extract_tags(remove_unwanted_tags(
                page_source), tags))
          #  print("Content scraped")
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    return results

# -------------------------------------------------------------------------------------------------

car_schema = {
    "properties": {
        "name": {"type": "string"},
        "Price": {"type": "number"},
        "Fuel Type": {"type": "string"},
        "Transmission": {"type": "string"},
        "Mileage": {"type": "number"},
        "Engine Size": {"type": "number"},
        "Seating Capacity": {"type": "number"},
        "Size": {"type": "number"},
        "Fuel Tank": {"type": "number"}

    },
    "required": ["name", "Price","Fuel Type","Transmission","Mileage","Engine Size","Seating Capacity","Size","Fuel Tank"],
}

# ------------------------------------------------------------------------------------------------------------------------------------



llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613",
                 openai_api_key=openai_api_key)


def extract(content: str, **kwargs):
    """
    The `extract` function takes in a string `content` and additional keyword arguments, and returns the
    extracted data based on the provided schema.
    """

    # This part just formats the output from a Pydantic class to a Python dictionary for easier reading. Feel free to remove or tweak this.
    if 'schema_pydantic' in kwargs:
        response = create_extraction_chain_pydantic(
            pydantic_schema=kwargs["schema_pydantic"], llm=llm).run(content)
        response_as_dict = [item.dict() for item in response]

        return response_as_dict
    else:
        return create_extraction_chain(schema=kwargs["schema"], llm=llm).run(content)
    


wsj_url = "https://www.cartrade.com/hyundai-cars/creta/"

token_limit = 2000


async def scrape_with_playwright(url: str, tags, **kwargs):
        html_content = await ascrape_playwright(url, tags)

        # print("Extracting content with LLM")

        html_content_fits_context_window_llm = html_content[:token_limit]

        extracted_content = extract(**kwargs,
                                    content=html_content_fits_context_window_llm)

        # pprint.pprint(extracted_content)
        return extracted_content



#added code for multiple URL
#to fetch all the different urls from the web page


 

def creator(temp_url):

    # UrlToScrap="https://www.cartrade.com/new-car-launches/"
    UrlToScrap=temp_url
    WantedList= ["https://www.cartrade.com/hyundai-cars/creta/"]
    InfoScraper = AutoScraper()
    x = InfoScraper.build(UrlToScrap, wanted_list=WantedList)

    # temp = []
    # for i in x :
    #   UrlToScrap= i
    #   WantedList= ["https://www.cartrade.com/hyundai-cars/creta/"]

    #   InfoScraper = AutoScraper()
    #   k = InfoScraper.build(UrlToScrap, wanted_list=WantedList)
    #   temp.extend(k)

    # temp2  = {}
    # temp2 = list(set(temp))



    result = []
    # for url1 in temp2[:2]:
    url1="https://www.cartrade.com/hyundai-cars/creta/"
    a = asyncio.run(scrape_with_playwright(
            url=url1,
            tags=["td","tr","th","h2"],
            # schema_pydantic=SchemaNewsWebsites,
            schema=car_schema,
        ))
    #   result.append(ascrape_playwright)
    result.append(a)
    # print(result)
    df = pd.DataFrame.from_records(result)
    temporary = df.to_html(classes='table table-striped table-hover')
   

    # for i in range(len(result)):
    #   # Initialise data to lists
    #   # temp[0] = temp[0] + temp[i]

    #     df = pd.DataFrame.from_records(result[i])
    #   df.to_csv('C:\Users\ASUS\Desktop\Projects'+str(i)+'.csv', index=False)
    
    return temporary,result
      # Export DataFrames to Excel using ExcelWriter
def Create_excel(result):
    with pd.ExcelWriter('output.xlsx') as excel_writer:
        # df = pd.DataFrame.from_records(result)
        # df.to_excel(excel_writer, sheet_name='Sheet1', index=False)
        for i in range(len(result)):
            df = pd.DataFrame.from_records(result[i])
            df.to_excel(excel_writer, sheet_name='Sheet'+str(i), index=False)

# if __name__ == "__main__":
#     main()
