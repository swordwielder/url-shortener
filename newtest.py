from flask import Flask, render_template, request, redirect, url_for
import json
import os.path

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('page.html')


@app.route('/shortenurl', methods=['GET', 'POST'])
def shortenurl():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as url_storage:
                urls = json.load(url_storage)
        if request.form['shortcode'] in urls.keys():
            return redirect(url_for('home'))
        urls[request.form['shortcode']] = request.form['url']
        with open('urls.json', 'w') as url_storage:
            json.dump(urls, url_storage)
        return render_template('shortenurl.html', shortcode=request.form['shortcode'])
    elif request.method == 'GET':
        return redirect(url_for('home'))
    else:
        return 'Not a valid request method for this route'


@app.route('/<string:shortcode>')
def shortcode_redirect(shortcode):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_storage:
            urls = json.load(url_storage)
            if shortcode in urls.keys():
                return redirect(urls[shortcode])

if __name__ == '__main__':
    app.run(debug=True)