from flask import Flask, request, render_template, make_response, jsonify
import sys, random, json, requests
from bs4 import BeautifulSoup

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

# parse the game page's relevant info and return as JSON
@app.route('/game/<int:gameID>')
def show_game_info(gameID):
    if gameID >= 0 and gameID < GAME_LIST_LENGTH:
        requestURL = BASE_GAME_URL + str(gameID)
        rawHTML = requests.get(requestURL)
        data = rawHTML.text
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

        # app.logger.info("title:" + title);
        # app.logger.info("gameLink:" + gameLink);
        # app.logger.info("developer:" + developer);
        # app.logger.info("developerLink:" + developerLink);
        # app.logger.info("genres:" + genres);
        # app.logger.info("platforms:" + platform);
        # app.logger.info("description:" + description);
        # app.logger.info("pictureURL:" + pictureURL);

        return jsonify(title=title,
                       gameLink=gameLink,
                       developer=developer,
                       developerLink=developerLink,
                       genres=genres,
                       platform=platform,
                       description=description,
                       pictureURL=pictureURL,
                       )
    return "<h1> Please enter a valid gameID </h1>"
# set cookies if not already done
def set_cookies(resp):
    if 'listOrder' in request.cookies:
        # print('found cookie, it is ' + request.cookies.get('listOrder'), file=sys.stderr)
        print('found cookie', file=sys.stderr)
    else: # set cookie if not already set
        print('did not find cookie', file=sys.stderr)
        # get the random dictionary order list
        cookieOrder = generate_random_list()
        resp.set_cookie('listOrder', cookieOrder)
        resp.set_cookie('nextToShow', "0")
    # app.logger.info(request.cookies.get('listOrder'))

# generates a csv of randomly shuffled integers from 0 to GAME_LIST_LENGTH
def generate_random_list():
    array = []
    for i in range(0, GAME_LIST_LENGTH):
        array.append(i)
    # random.shuffle(array)

    result = json.dumps(array)
    return result

if __name__ == '__main__':
    app.run()

