#!/usr/bin/python

"""
Nerea Del Olmo Sanz - GITT
PRACTICA 1
"""


import webapp
import urllib


class shortenUrlApp (webapp.webApp):

    # Declare the dictionary whose keys are the real URL
    dict_realURL = {}

    # Declare the dictionary whose keys are the shorten URL
    dict_shortenedURL = {}

    # Declare and initialize the index for shorten
    index = 0

    def parse(self, request):
        """Returns the resource name, NOT including '/' """
        verb = request.split(' ', 2)[0]
        resource = request.split(' ', 2)[1].replace('/', ' ').split(' ', 1)[1]

        if verb == "POST":
            body = request.split('\r\n\r\n', 1)[1].split('=')[1]
            body = body.replace('%3A%2F%2F', '://')
        elif verb == "GET":
            body = ""
        return (verb, resource, body)

    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Finds the HTML text corresponding to the resource name.
        """

        (verb, resource, body) = parsedRequest

        form = '<form action="" method="POST">'
        form += 'Type the url to shorten: <input type="text" name="value">'
        form += '<input type="submit" value="Send form">'
        form += '</form><br>'

        if verb == "GET":
            urlList = "<b>Real URLs: </b><br>"
            urlList += str(self.dict_realURL.keys()) + "<br><br>"
            urlList += "<b>Shortened URLs: </b><br>"
            urlList += str(self.dict_shortenedURL.keys()) + "<br>"

            if resource == "":
                httpCode = "200 OK"
                htmlBody = "<html><body>" \
                    + form \
                    + urlList \
                    + "</body></html>"
            else:
                try:
                    resource = int(resource)

                    if resource in self.dict_shortenedURL.keys():
                        URL = self.dict_shortenedURL[resource]
                        httpCode = "302 FOUND\nLocation:" + URL
                        htmlBody = ""
                    else:
                        httpCode = "404 Not Found"
                        htmlBody = "<html><body><h1>ERROR 404: Not found<br>" \
                            + "The resource is not a shortened URL</h1>" \
                            + form \
                            + urlList \
                            + "</body></html>"
                except ValueError:
                    httpCode = "404 Not Found"
                    htmlBody = "<html><body><h1>ERROR! Invalid resource</h1>" \
                        + form \
                        + urlList \
                        + "</body></html>"

        elif verb == "POST":
            URL = urllib.unquote(body)

            if not URL.startswith("http"):
                URL = "http://" + URL

            if not URL in self.dict_realURL:
                self.dict_realURL[URL] = self.index
                self.dict_shortenedURL[self.index] = URL
            else:
                self.index = self.dict_realURL[URL]

            shortenedURL = "http://localhost:1234/" + str(self.index)

            urlList = "<b>Real URLs: </b><br>"
            urlList += str(self.dict_realURL.keys()) + "<br><br>"
            urlList += "<b>Shortened URLs: </b><br>"
            urlList += str(self.dict_shortenedURL.keys()) + "<br>"

            httpCode = "200 OK"
            htmlBody = "<html><body><h3>The URL: " \
                + '<a href="' + URL + '"target="_blank">' + str(URL) + "</a>" \
                + " has been shorten as: " \
                + '<a href="' + str(self.index) + '"target="_blank">' \
                + str(shortenedURL) + "</a></h3><br><br><br>" \
                + form \
                + urlList \
                + "</body></html>"
            self.index = self.index + 1
        return (httpCode, htmlBody)

if __name__ == "__main__":
    practica1 = shortenUrlApp("localhost", 1234)
