from flask import Flask, render_template, request
import requests
import json
import os
IMG_PATH = r'static/img/'

app = Flask(__name__, template_folder='views', static_url_path='/static')
app.debug = True

app.config['UPLOAD_FOLDER'] = IMG_PATH

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
		r = requests.post(url = 'http://127.0.0.1:3001/credible', data = {"claim_text": claim})
		if r.status_code != 200:
			app.logger.error("Request has failed!")
		else:
			res = r.json()
			app.logger.info(res)
		# send json to template
		return render_template("result.html", data=res["results"], claim=claim)
	else:
		return render_template("home.html")

@app.route('/index', methods=['GET'])
def index_html():
	if request.method == 'GET':
		return render_template('index.html')

@app.route("/fakeWebsite",methods=['POST', 'GET'])
def fakeWebsite():
	if request.method == 'POST':
		res = {}
		data = request.form['url']
		app.logger.info(data)

		r = requests.post(url = 'http://127.0.0.1:3001/websitecheck', data={"url": data})
		if r.status_code != 200:
			app.logger.error("Request has failed!")
		else:
			res = r.json()
			app.logger.info(res)
			print(res['data'])
			print(res)
		return  json.dumps(res)
	else:
		return render_template('fakeWebsite.html')

@app.route("/WebSpamCheckOld",methods=['POST', 'GET'])
def WebSpamCheckOld():
	if request.method == 'POST':
		res = {}
		data = request.form['url']
		app.logger.info(data)

		r = requests.post(url = 'http://127.0.0.1:3001/spamcheck', data={"url": data})
		if r.status_code != 200:
			app.logger.error("Request has failed!")
		else:
			res = r.json()
			app.logger.info(res)
			#print(res['data'])
		return  json.dumps(res)
	else:
		return render_template('WebSpamCheck.html')

@app.route("/WebSpamCheck",methods=['POST', 'GET'])
def WebSpamCheck():
	if request.method == 'POST':
		res = {}
		data = request.form['url']
		app.logger.info(data)

		r = requests.post(url = 'http://127.0.0.1:3001/spamcheck', data={"url": data})
		if r.status_code != 200:
			app.logger.error("Request has failed!")
		else:
			res['spam'] = r.json()
			app.logger.info(res)
		
		r = requests.post(url = 'http://127.0.0.1:3001/websitecheck', data={"url": data})
		if r.status_code != 200:
			app.logger.error("Request has failed!")
		else:
			res['phising'] = r.json()
			app.logger.info(res)
		
		return  json.dumps(res)
	else:
		return render_template('WebSpamCheck.html')

@app.route("/community", methods=['POST', 'GET'])
def community():
	if request.method == 'GET':
		return render_template('community_detection.html')
	else:
		res = {}
		data = request.form['user_name']
		app.logger.info(data)

		r = requests.post(url='http://127.0.0.1:3001/community', data={'user_name': data})
		if r.status_code != 200:
			app.logger.error("Request has failed!")
		else:
			res = r.json()
		return json.dumps(res)

@app.route("/fakeaccount", methods=['POST', 'GET'])
def fakeaccount():
	if request.method == 'GET':
		return render_template('fakeaccount_detection.html')
	else:
		res = {}
		data = request.form['user_name']
		app.logger.info(data)

		r = requests.post(url='http://127.0.0.1:3001/fakeaccount', data={'user_name': data})
		if r.status_code != 200:
			app.logger.error("Request has failed!")
		else:
			res = r.json()
		return json.dumps(res)

@app.route("/stance", methods=['POST', 'GET'])
def stance():
	if request.method == 'GET':
		return render_template('stance_detection.html')
	else:
		res = {}
		data = request.form['user_name']
		app.logger.info(data)

		r = requests.post(url='http://127.0.0.1:3001/stance', data={'user_name': data})
		if r.status_code != 200:
			app.logger.error("Request has failed!")
		else:
			res = r.json()
		return json.dumps(res)

@app.route("/credible", methods=['POST', 'GET'])
def credible():
	if request.method == 'POST':
		res = {}
		claim = request.form['claim']
		app.logger.info(claim)

		# send request to rest api
		r = requests.post(url = 'http://127.0.0.1:3001/credible', data = {"claim_text": claim})
		if r.status_code != 200:
			app.logger.error("Request has failed!")
		else:
			res = r.json()
			app.logger.info(res)
		# send json to template
		return json.dumps(res)
	else:
		return render_template("credible_resources.html")

@app.route("/fakeimage", methods=['POST', 'GET'])
def fakeimage():
    if request.method == 'POST':
        res = {}
        file = request.files['image']
        file.save(os.path.join(IMG_PATH, 'upload.png'))
        app.logger.info(file.filename)
        # send request to rest api

        # r = requests.post(url = 'http://127.0.0.1:3001/fakeimage', data = {"b64_image": ""})
		#
        # if r.status_code != 200:
        #     app.logger.error("Request has failed!")
        # else:
        #     res = r.json()
        return render_template("fake_image_result.html")
    else:
        return render_template("fake_image.html")

if __name__ == "__main__":
	app.run(debug=True,port=9000)
