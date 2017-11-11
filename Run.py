from flask import Flask, request, render_template, make_response
import sys, random, json

app = Flask(__name__)

#### CONFIGURE BELOW ####
# set to false on deploy
app.debug = True
# the current number of games in the showcase
GAME_LIST_LENGTH = 77
# base url to grab featured game content
BASE_GAME_URL = 'https://unity3d.com//showcase/gallery/more/Default/featured/weight/1/'

#########################

@app.route('/')
def index():
    index = 0
    resp = make_response(render_template('base.html', index = index))
    set_cookies(resp)
    return resp

# set cookies if not already done
def set_cookies(resp):
    if 'listOrder' in request.cookies:
        print('found cookie, it is ' + request.cookies.get('listOrder'), file=sys.stderr)
    else: # set cookie if not already set
        print('did not find cookie', file=sys.stderr)
        # get the random dictionary order list
        cookieOrder = generate_random_list()
        # print('cookie order is ' + cookieOrder, file=sys.stderr)
        resp.set_cookie('listOrder', cookieOrder)
        resp.set_cookie('nextToShow', '0')

# generates a randomly shuffled list of integers from 0 the specified length
def generate_random_list():
    array = []
    for i in range(0, GAME_LIST_LENGTH):
        array.append(str(i))
    random.shuffle(array)

    dict = {}
    for i in range (0, GAME_LIST_LENGTH):
        dict[str(i)] = array[i]
    result = json.dumps(dict)
    return result

if __name__ == '__main__':
    app.run()