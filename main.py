from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html', message="Hello world!")


@app.route('/about')
def about():
	return render_template('about.html', title='About', description='This is a flask demo app')
	

if (__name__ == "__main__"):
	app.run(debug=True)
