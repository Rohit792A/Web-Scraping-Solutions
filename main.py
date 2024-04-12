from flask import Flask,render_template,jsonify,request
from werkzeug.urls import url_quote
from AutomatedScraping import creator,Create_excel

# app = Flask(__name__)
app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/services.html")
def service():
    return render_template('services.html')

# @app.route("/services.html")
# def home():
#     return render_template('index.html')
# @app.route("/")
# def home():
#     return render_template('index.html')

@app.route("/forward/", methods=['POST'])
def move_forward():
    url = request.form.get("url")

    rest,df = creator(url)
    # print(rest,df)
    Create_excel(df)
    #forward_message = "Moving Forward..."
    return rest
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