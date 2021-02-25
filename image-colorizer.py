from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')

def main():
	return render_template('main.html')

@app.route('/colorize', methods=['POST'])
def colorize():
	try:
		image = request.json['imageFile']

		return jsonify({"imageFile": image}), 200
	except Exception as e:
		return f"An Error Occured: {e}"

if __name__=="__main__":
	app.run()