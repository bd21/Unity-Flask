import json, random, requests

from bs4 import BeautifulSoup
from flask import Flask, request, render_template, make_response, jsonify

app = Flask(__name__)

#### CONFIGURE BELOW ####

# set to true to display games in a random order
SHUFFLE_GAMES = True
# set to false on deploy
app.debug = False
# the current number of games in the showcase
GAME_LIST_LENGTH = 77
# base url to grab featured game content
BASE_GAME_URL = 'https://unity3d.com//showcase/gallery/more/Default/featured/weight/1/'

#########################

@app.route('/')
def index():
    resp = make_response(render_template('base.html'))
    set_cookies(resp)
    return resp

# get and parse the given game's relevant info and return as JSON
# return error message if invalid gameID
@app.route('/game/<int:gameID>')
def show_game_info(gameID):
    if gameID < 0 or gameID >= GAME_LIST_LENGTH:
        return "<h1> Please enter a valid gameID </h1>"

    requestURL = BASE_GAME_URL + str(gameID)
    rawHTML = requests.get(requestURL)
    data = rawHTML.text

    # extract data from html
    soup = BeautifulSoup(data, "lxml")
    title = soup.find_all('h3', {'class':"mb10 title"})[0].text
    gameLink = soup.find('a').attrs['href']
    developer = soup.find_all('a', {'class':'developer'})[0].text
    developerLink = soup.find_all('a', {'class':'developer'})[0].attrs['href']
    genres = soup.find_all('p', {'class':'mb10 genres'})[0].text
    platforms = soup.find_all('div', {'class':'tip'})
    platform = platforms[0].text
    for i in range(1, len(platforms)):
        platform += ", " + platforms[i].text
    description = soup.find_all('div', {'class':'mb15 description clear'})[0].text
    description = description.replace('Read more', '')
    pictureURL = soup.find_all('img', {'class':'ic'})[0].attrs['src']

    return jsonify(title=title,
                   gameLink=gameLink,
                   developer=developer,
                   developerLink=developerLink,
                   genres=genres,
                   platform=platform,
                   description=description,
                   pictureURL=pictureURL)

# set cookies if not already done
def set_cookies(resp):
    if 'listOrder' not in request.cookies:
        cookieOrder = generate_random_list()
        resp.set_cookie('listOrder', cookieOrder)
        resp.set_cookie('nextToShow', "0")

# generates an array of randomly shuffled integers from 0 to GAME_LIST_LENGTH
# and return as JSON array
def generate_random_list():
    array = []
    for i in range(0, GAME_LIST_LENGTH):
        array.append(i)
    if SHUFFLE_GAMES:
        random.shuffle(array)
    app.logger.info("generated array: " + str(array));
    result = json.dumps(array)
    return result

if __name__ == '__main__':
    app.run()