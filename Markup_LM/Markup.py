import requests
from bs4 import BeautifulSoup
import torch
import pickle
from collections import Counter
import pandas as pd

#to fetch all the different urls from the web page
from autoscraper import AutoScraper

model_pkl_file = "Markup_LM\model.pkl" 
processor_pkl_file = "Markup_LM\processor.pkl" 

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


# Ask url
def give_answer(url,question1):

  UrlToScrap=url
  WantedList= [UrlToScrap]
  InfoScraper = AutoScraper()
  x = InfoScraper.build(UrlToScrap, wanted_list=WantedList)
  
  temp = []
  for i in x :
    UrlToScrap= i
    WantedList= [url]
  
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
    # questions = ["tell me the price of the car?"]
    questions = question1
    for question in questions:
      answer1.append(tellMe(soup,question))
    answer.append(answer1)
  print(answer)
  return answer


def mode(url,question1):
  answer = give_answer(url,question1)
  mode_of_attr = []

  """Return the mode of the length of the strings in a nested list."""
  for i in range(len(answer[0])):
    # Get the lengths of all the strings in the nested list.
    lengths = [len(s[i]) for s in answer]

    # Create a Counter object to count the occurrences of each length.
    counts = Counter(lengths)

    # Find the length with the highest count.
    mode = counts.most_common(1)[0][0]

    mode_of_attr.append(mode)
  mode_length = mode_of_attr

  for i in range(len(mode_length)):
     if mode_length[i] < 11:
        mode_length[i] = 13

  final_answer = []

  for item in answer :
    tempo = []
    for i in range(len(item)):

      if len(item[i])>(mode_length[i]-10) and len(item[i])<(mode_length[i]+20):

        tempo.append(item[i])
    final_answer.append(tempo)
  

  with pd.ExcelWriter('output_markup.xlsx', engine='xlsxwriter') as excel_writer:
    output_markup = pd.DataFrame.from_records(final_answer)
    output_markup.columns = ['Car Name', 'price']
    output_markup.to_excel(excel_writer, sheet_name='Sheet1', index=False)
  return output_markup


# if __name__ == "__main__":
#    main()
