#!/usr/bin/env python
#
#Copyright (c) 2012  Shane R. Spencer
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions: 
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software. 
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

"""I ate three cookies while programming this"""

import sys
import exceptions
import time
import logging
import pprint
import operator
import uuid

ID = uuid.uuid1()
DEBUG = True

import urllib
import urllib2
import cookielib

import xml.dom.minidom

import tempfile

cj = cookielib.MozillaCookieJar(tempfile.mktemp(), delayload=True)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def fetch(options, baseurl, action, actionid=None, **kwargs):
    url = baseurl + "mxml?"
    kwargs['action'] = action #save time

    kwargs['actionid'] = str(actionid) or str(uuid.uuid5(ID, str(uuid.uuid1())))

    try:
        cj.load(options.cookiefile)
    except:
        logging.debug("No cookie for you")

    response = opener.open(url + urllib.urlencode(kwargs))

    cj.save(options.cookiefile)

    body = response.read()

    dom = xml.dom.minidom.parseString(body)

    responses = dom.getElementsByTagName('generic')
    #actionid = None

    #print dom.toprettyxml()

    for response in responses:        
        attributes = dict(response.attributes.items())
        if attributes.get('response', 'Event') not in ['Success', 'Event']:
            raise exceptions.ValueError('Something bad')
        
        yield action, actionid, kwargs, attributes
    
def prettydebug(prefix, thing):
    id = str(uuid.uuid5(ID, str(uuid.uuid1())))
    for line in pprint.pformat(thing, indent=4).split('\n'):
        logging.debug(id + ": " + prefix + ": " + line)

#### Soft and overridable event handlers

#from handlers import * # Because you can

#### Hard event handlers

#def handle_event_userevent(action, actionid, actionkwargs, attributes):
#    """ Example return for UserEvent Events """
#    prettydebug('Process Userevent Function', 'Would like to call handle_event_userevent_%s and will try to do so' % str(attributes.get('userevent')).lower())
#    callable = globals().get('handle_event_userevent_%s' % str(attributes.get('userevent')).lower())
#    if callable:
#        callable(action, actionid, actionkwargs, attributes)
#    else:
#        ## DO SOMETHING PRODUCTIVE
#        pass


#def handle_action_login(action, actionid, actionkwargs, attributes):
#    """ Example return for Login """
#    logging.debug("Login command returned")

#def handle_action_corestatus(action, actionid, actionkwargs, attributes):
#    """ Example return for CoreStatus """
#    logging.debug("The CORE IS:")
#    for k, v in sorted(attributes.items()):
#        logging.debug("%s: %s" % (k, v))

#### Example Process events/actions

def process(action, globals=None):
    response = None
    for action, actionid, actionkwargs, attributes in action:
        prettydebug('Process Action', action)
        prettydebug('Process ActionID', actionid)
        prettydebug('Process ActionArgs', actionkwargs)
        prettydebug('Process Attributes', attributes)
        if attributes.get('event'):
            prettydebug('Process Function', 'Would like to call handle_event_%s and will try to do so' % str(attributes.get('event')).lower())
            callable = globals.get('handle_event_%s' % str(attributes.get('event')).lower())
            if callable:
                callable(action, actionid, actionkwargs, attributes)
        else:
            response = attributes.get('response'), attributes.get('message'), attributes.get('actionid')

            prettydebug('Process Function', 'Would like to call handle_action_%s and will try to do so' % action.lower())
            callable = globals.get('handle_action_%s' % action.lower())
            if callable:
                callable(action, actionid, actionkwargs, attributes)


    prettydebug('Process Response', response)
    return response

#### Example Run

def run(options):

    #### Do something

    process(fetch(options, options.url, 'Login', username=options.username, secret=options.secret), globals())
    process(fetch(options, options.url, 'Events', eventmask="on"), globals())
    process(fetch(options, options.url, 'SIPPeers', username=options.username, secret=options.secret), globals())
    process(fetch(options, options.url, 'CoreStatus', username=options.username, secret=options.secret), globals())

    while True:
        process(fetch(options, options.url, 'WaitEvent'), globals())

    #### End of do something

if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.set_defaults(verbose=None)
    parser.set_defaults(url="http://127.0.0.1:8088/")
    parser.set_defaults(host='127.0.0.1')
    parser.set_defaults(loglevel=logging.INFO)
    parser.set_defaults(cookiefile=None)

    parser.add_option("-v", action="store_true", dest="verbose")
    parser.add_option("-q", action="store_false", dest="verbose")
    parser.add_option("-b", type="string", dest="url")
    parser.add_option("-u", type="string", dest="username")
    parser.add_option("-s", type="string", dest="secret")
    parser.add_option("-c", type="string", dest="cookiefile")
    parser.add_option("-d", action="store_const", dest="loglevel", const=logging.DEBUG)

    (options, args) = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=options.loglevel,
        format='%(asctime)s %(process)d %(filename)s %(lineno)d %(levelname)s #| %(message)s',
        datefmt='%H:%M:%S')

    run(options)
