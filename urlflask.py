import json, os
from django.shortcuts import render
from flask import Flask, request, render_template,jsonify


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    #data = request.form['urllink'] 
    #print(data)

    return render_template('./page.html')




if __name__ == '__main__':
    app.run(debug=True)