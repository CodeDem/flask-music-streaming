from flask import Flask,render_template, Response
import sys
# Tornado web server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

#Debug logger
import logging 
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


def return_dict():
    #Dictionary to store music file information
    dict_here = [
        {'id': 1, 'name': 'Acoustic Breeze', 'link': 'music/acousticbreeze.mp3', 'genre': 'General', 'chill out': 5},
        {'id': 2, 'name': 'Happy Rock','link': 'music/happyrock.mp3', 'genre': 'Bollywood', 'rating': 4},
        {'id': 3, 'name': 'Ukulele', 'link': 'music/ukulele.mp3', 'genre': 'Bollywood', 'rating': 4}
        ]
    return dict_here

# Initialize Flask.
app = Flask(__name__)


#Route to render GUI
@app.route('/')
def show_entries():
    general_Data = {
        'title': 'Music Player'}
    print(return_dict())
    stream_entries = return_dict()
    return render_template('simple.html', entries=stream_entries, **general_Data)

#Route to stream music
@app.route('/<int:stream_id>')
def streammp3(stream_id):
    def generate():
        data = return_dict()
        count = 1
        for item in data:
            if item['id'] == stream_id:
                song = item['link']
        with open(song, "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
                logging.debug('Music data fragment : ' + str(count))
                count += 1
                
    return Response(generate(), mimetype="audio/mp3")

#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    logging.debug("Started Server, Kindly visit http://localhost:" + str(port))
    http_server.listen(port)
    IOLoop.instance().start()
    
