from flask import Flask,request, render_template
import Searcher


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('search_text.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    root = 'B:\CS 121\Assignment3M3\TEST'
    processed_text = Searcher.UInterface(text,root)
    print(processed_text)
    if len(processed_text) == 1:
        return render_template('display.html', t=processed_text[0], data=[])
    else:
        return render_template('display.html', t=processed_text[:2], data=processed_text[2:])
    

if __name__ == '__main__':
    app.run()