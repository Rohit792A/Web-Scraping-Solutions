from flask import Flask,render_template,jsonify,request
# from werkzeug.urls import url_quote
from AutomatedScraping import creator,Create_excel
from Markup_LM.Markup import mode 
import json
# app = Flask(__name__)
app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/services.html")
def service():
    return render_template('services.html')

@app.route("/howitworks.html")
def howitworks():
    return render_template('howitworks.html')

@app.route("/getstarted.html")
def getstarted():
    return render_template('getstarted.html')

@app.route("/usecases.html")
def usecases():
    return render_template('usecases.html')

@app.route("/learnmore.html")
def learnmore():
    return render_template('learnmore.html')  

@app.route("/ecommerce.html")
def ecommerce():
    return render_template('ecommerce.html')  

@app.route("/finance.html")
def finance():
    return render_template('finance.html')  

@app.route("/realestate.html")
def realstate():
    return render_template('realestate.html') 


@app.route("/joblistings.html")
def joblistings():
    return render_template('joblistings.html') 

@app.route("/generativeai.html")
def generativeai():
    return render_template('generativeai.html') 

@app.route("/services_with_time.html", methods=['GET','POST'])
def services_with_time():
    if request.method == 'POST':
        url = request.form.get("url")
        count = request.form.get("count")
        counter = int(count)
        question1 = []
        for i in range(1,counter):
            ss = "question" + str(i)
            print(ss)
            question = request.form.get(ss)
            question1.append(question)
        # for question1 in zip(request.form.getlist('question')):
            print(question1)
            print(type(counter))
            counter -= 1
        df = mode(url,question1)
    return render_template('services_with_time.html')

@app.route("/forward/", methods=['POST'])
def move_forward():

    # print(rest,df)
    #Create_excel(df)
    
    # if request.method == 'POST':
    url = request.form.get("url")



# return "Schema saved successfully!"
#forward_message = "Moving Forward..."
    rest,df = creator(url)
    Create_excel(df)
    return rest

# @app.route("/set-schema.html", methods=['GET', 'POST'])
# def set_schema():
#     if request.method == 'POST':
#         schema = {
#             "properties": {},
#             "required": []
#         }

#         for key, value in request.form.items():
#             print(key, value)
#             if key.startswith("name"):
#                 schema["properties"][value] = {"type": request.form.get(f"type-{key.split('-')[-1]}", "string")}
#                 schema["required"].append(value)
#         with open('schema.json', 'w') as f:
#             json.dump(schema, f)
#         return "Schema saved successfully!"
#     return render_template('set-schema.html')


# @app.route('/process', methods=['POST'])
# def download_file():
#     result = request.form
#     print(result)
#     # rest = creator(url)
    
#     return render_template('services.html')

# @app.route("/forward/")
# @app.route("")
# def main():
#     return render_template('services.html')
    # result = []
    # for url1 in temp2[:10]:
    #     a = asyncio.run(scrape_with_playwright(
    #         url=url1,
    #         tags=["td","tr","th","h2"],
    #         schema=car_schema,
    #     ))
    #     result.append(a)

    

if __name__ == "__main__":
    app.run(debug=True)