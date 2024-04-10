import requests
from bs4 import BeautifulSoup
import torch
import pickle

#to fetch all the different urls from the web page
from autoscraper import AutoScraper

model_pkl_file = "model.pkl" 
processor_pkl_file = "processor.pkl" 

# load model from pickle file
with open(model_pkl_file, 'rb') as file:  
    model = pickle.load(file)

with open(processor_pkl_file, 'rb') as file:  
    processor = pickle.load(file)


def remove_unwanted_tags(html_content, unwanted_tags=["script", "style","img","svg","input","a","iframe","link"]):
    """
    This removes unwanted HTML tags from the given HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    for car in soup.find_all('div', class_="keySpecs"):
      return str(car)

    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)

def tellMe(soup,question):
  html_string = remove_unwanted_tags(soup.prettify())
# html_string = "<title>My name is yaman</title>"

# question = "what aryan's phone number?"

  encoding = processor(html_string, questions=question, max_length= 512, truncation = True, return_tensors="pt")

  with torch.no_grad():
      outputs = model(**encoding)

  answer_start_index = outputs.start_logits.argmax()
  answer_end_index = outputs.end_logits.argmax()

  predict_answer_tokens = encoding.input_ids[0, answer_start_index : answer_end_index + 1]
  answer = processor.decode(predict_answer_tokens).strip()
  return answer


# flag = 0
def main():

  UrlToScrap="https://www.cartrade.com/new-car-launches/"
  WantedList= ["https://www.cartrade.com/hyundai-cars/creta/"]
  InfoScraper = AutoScraper()
  x = InfoScraper.build(UrlToScrap, wanted_list=WantedList)
  
  temp = []
  for i in x :
    UrlToScrap= i
    WantedList= ["https://www.cartrade.com/hyundai-cars/creta/"]
  
    InfoScraper = AutoScraper()
    k = InfoScraper.build(UrlToScrap, wanted_list=WantedList)
    temp.extend(k)
  temp2  = {}
  temp2 = list(set(temp))
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }
  answer = []
  for urls in temp2:
    answer1 = []
    url = urls
  # url = "https://sidekickcompany.com/clients/cinaryan/index.html"
    response = requests.get(url, headers=headers)
    # print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # print("yes")
    # else:
      # print("no")
    questions = ["tell me the price of the car?"]
    for question in questions:
      answer1.append(tellMe(soup,question))
    answer.append(answer1)
  print(answer)
  return answer


if __name__ == "__main__":
   main()
