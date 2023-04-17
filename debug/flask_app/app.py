from flask import Flask, request, jsonify, render_template, send_file, Response

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/get', methods=['GET'])
def get():
	response = {'args': request.args}
	return jsonify(response), 200


@app.route('/post', methods=['POST'])
def post():
	request_content_type = request.headers['Content-Type'].split(";")[0].strip()
	if request_content_type == 'application/json':
		return request.get_json(), 200
	response = request.get_data()
	if request_content_type == "multipart/form-data" and isinstance(response, bytes):
		response = Response(response, mimetype='application/octet-stream')
	return response, 200


@app.route('/html', methods=['GET'])
def get_html():
	return render_template("html.html"), 200


@app.route('/image/jpeg', methods=['GET'])
def get_jpeg():
	filename = 'data/img.jpg'
	return send_file(filename, mimetype='image/jpeg')


@app.route('/image/png', methods=['GET'])
def get_png():
	filename = 'data/img.png'
	return send_file(filename, mimetype='image/jpeg')


@app.route('/cookies/set', methods=['GET'])
def set_cookies():
	args = request.args
	response = jsonify({"message": "set cookies", "args": args})
	for key, value in args.items():
		response.set_cookie(key, value)
	return response, 200


@app.route('/cookies', methods=['GET'])
def get_cookies():
	return jsonify(dict(request.cookies.to_dict())), 200


@app.route('/cookies/clear', methods=['GET'])
def clear_cookies():
	response = jsonify({"message": "clear all cookies"})
	for key in request.cookies.keys():
		response.delete_cookie(key)
	return response, 200


if __name__ == '__main__':
	app.run()
