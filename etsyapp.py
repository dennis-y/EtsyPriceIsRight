from flask import Flask, request, render_template, redirect
import requests
import json
import random
app = Flask(__name__)

LISTING_REQUEST = 'https://openapi.etsy.com/v2/listings/active?api_key=bui5d6m2sgsuw17bktb66oe3&limit=1000&fields=listing_id,price'
RADIUS = 5.0
price = -1.0
id = '-1'
total_items = -1
image_url = None


@app.route('/')
def hello_world():
    global price
    global image_url
    global id
    endpoint = LISTING_REQUEST
    response = requests.get(endpoint)
    data = response.json()['results']
    total_items = len(data)

    while True: # used to avoid case where price is not defined
        choice_index = random.randint(0, total_items - 1)
        price = float(data[choice_index]['price'])
        if price > 0.0:
            break
    id = str(data[choice_index]['listing_id'])

    endpoint2 = 'https://openapi.etsy.com/v2/listings/' + id + '/images?api_key=bui5d6m2sgsuw17bktb66oe3'
    response2 = requests.get(endpoint2)
    data2 = response2.json()['results']
    image_url = data2[0]['url_570xN']
    return render_template('index.html', img_src=image_url)

@app.route('/winner', methods=['POST'])
def check_guess():
    global price
    global image_url
    if request.form['p1guess'] is None or request.form['p1guess'] == "":
        return redirect('/')
    if request.form['p2guess'] is not None and request.form['p2guess'] != "":
        p1guess = float(request.form['p1guess'])
        p2guess = float(request.form['p2guess'])
        p1diff = abs(price - p1guess)
        p2diff = abs(price - p2guess)
        if (p2diff > p1diff):
            return render_template('winner.html',buy=True,img_src=image_url,price=price,winner='Player 1')
        else:
            return render_template('winner.html',buy=True,img_src=image_url,price=price,winner='Player 2')
    else:
        if abs(float(request.form['p1guess']) - price) < RADIUS:
            return render_template('winner.html',buy=True,img_src=image_url,price=price,winner='Player 1')
        else:
            if float(request.form['p1guess']) > price:
                return render_template('winner.html',buy=True, img_src=image_url,price=price,winner='Computer')
            else:
                return render_template('winner.html', img_src=image_url,price=price,winner='Computer')

@app.route('/replay', methods=['POST'])
def replay():
    return redirect('/')


@app.route('/buy', methods=['POST'])
def buy_it():
    global id
    redirect_url = 'http://www.etsy.com/listing/' + id
    return redirect(redirect_url)


if __name__ == '__main__':
    app.run(debug=True)
