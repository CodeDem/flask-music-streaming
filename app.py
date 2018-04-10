# Some necessary includes: Flask, SQLite and some system functions
from flask import Flask, g, render_template, redirect, request, Response
import sys
import os
from subprocess import *
# Tornado web server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import logging as log


# Just a debugging flag to switch off Flask and Tornado
web = True


def return_dict():
    dict_here = [
        {'id': 1, 'name': 'Claps', 'link': 'music/song.mp3', 'genre': 'General', 'rating': 5},
        {'id': 2, 'name': 'Bom Diggy','link': 'music/bom.mp3', 'genre': 'Bollywood', 'rating': 3},
        {'id': 3, 'name': 'Tera yaar hoon main', 'link': 'music/yaar.mp3', 'genre': 'Bollywood', 'rating': 2}
        ]

    return dict_here

# Initialize Flask.
if web:
    app = Flask(__name__)

if web:
    @app.route('/')
    def show_entries():
        general_Data = {
            'title': 'Music Player'}
        print(return_dict())
        stream_entries = return_dict()
        return render_template('design.html', entries=stream_entries, **general_Data)

    @app.route('/<int:stream_id>')
    def mpc_play(stream_id):
            def generate():
                data = return_dict()
                for item in data:
                    if item['id'] == stream_id:
                        song = item['link']
                with open(song, "rb") as fwav:
                    data = fwav.read(1024)
                    while data:
                        yield data
                        data = fwav.read(1024)
                        log.warning(data)
                        
            return Response(generate(), mimetype="audio/mp3")


#launch a Tornado server with HTTPServer.
if __name__ == "__main__":

    if web:
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(5000)
        IOLoop.instance().start()
