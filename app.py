import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from research import crawler

# CONFIGURATIONS
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def landing():
    return render_template('landing.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/research")
def research():
    return render_template('research.html')

@app.route("/research/send_email")
def send_email():
    crawler.collect_upcomming_sales('./Upcoming_sales.txt')
    crawler.send_data_by_email('./Upcoming_sales.txt') 
    response = { 'status' : '200'} 
    return jsonify(response)

@app.route("/tickets/data")
def data(): 
    return render_template('data.html')

@app.route("/tickets/buy")
def buy():
    return render_template('buy.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run()