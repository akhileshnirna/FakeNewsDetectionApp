from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='views')

@app.route("/")
def index():
    return render_template("template.html")

@app.route("/home", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        res = {}
        claim = request.form['claim']
        app.logger.info(claim)

        # send request to rest api
        r = requests.post(url = 'http://127.0.0.1:5000/credible', data = {"claim_text": claim})
        if r.status_code != 200:
            app.logger.error("Request has failed!")
        else:
            res = r.json()
            app.logger.info(res)
        # send json to template
        return render_template("result.html", data=res["results"], claim=claim)
    else:
        return render_template("home.html")

@app.route("/fakeWebsite",methods=['POST', 'GET'])
def fakeWebsite():
    if request.method == 'POST':
        res = {}
        data = request.form['url']
        app.logger.info(data)

        r = requests.post(url = 'http://127.0.0.1:5000/websitecheck', data={"url": data})
        if r.status_code != 200:
            app.logger.error("Request has failed!")
        else:
            res = r.json()
            app.logger.info(res)
            print(res['data'])
        return  render_template("result_test1.html", result = res['final'], url = res['url'])
    else:
        return render_template('fakeWebsite.html')

@app.route("/WebSpamCheck",methods=['POST', 'GET'])
def WebSpamCheck():
    if request.method == 'POST':
        res = {}
        data = request.form['url']
        app.logger.info(data)

        r = requests.post(url = 'http://127.0.0.1:5000/spamcheck', data={"url": data})
        if r.status_code != 200:
            app.logger.error("Request has failed!")
        else:
            res = r.json()
            app.logger.info(res)
            #print(res['data'])
        return  render_template("webspam_result.html", word_count = res['words_count'], title_len = res['title_len'], url = data, tld = res['tld_data'],
                                infer = res['tld_infer'], txt_to_anch = res['txt_to_anch'])
    else:
        return render_template('WebSpamCheck.html')

if __name__ == "__main__":
    app.run(debug=True,port=9000)