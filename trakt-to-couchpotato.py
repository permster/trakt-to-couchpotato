#!/usr/bin/env python

# Check needed software dependencies
import sys
<<<<<<< HEAD
reload(sys)
sys.setdefaultencoding("utf-8")

=======
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1
if sys.version_info < (2, 7):
    print "Sorry, requires Python 2.7."
    sys.exit(1)

import json
import urllib2
<<<<<<< HEAD
# import base64
=======
import base64
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1
import hashlib
import logging
import os.path
import argparse
<<<<<<< HEAD
import ConfigParser
=======
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1

# argument parser
parser = argparse.ArgumentParser(description='Import trakt.tv movies into Couch Potato.')
parser.add_argument('-log', help='log file path')
args = parser.parse_args()

# declare variables
<<<<<<< HEAD
trakt_username = ''
trakt_clientid = ''
trakt_clientsecret = ''
trakt_accesstoken = ''
trakt_redirect_uri = ''
cp_apikey = ''
pb_token = ''
movies_added = []
err_count = 0
pb_url = 'https://api.pushbullet.com/v2/pushes'
pb_msg = ''
cp_urls = {
    'base': 'http://localhost:5050/api/',
    'app_available': '{0}/app.available',
    'category_list': '{0}/category.list/',
    'movie_add': '{0}/movie.add/?identifier={1}&category_id={2}'
}

trakt_urls = {
    'base': 'https://api-v2launch.trakt.tv/',
    'authorization': 'https://trakt.tv/oauth/authorize',
    'refresh_token': 'oauth/token',
    'users_list': 'users/{0}/lists/{1}',
    'users_lists': 'users/{0}/lists',
    'users_list_items': 'users/{0}/lists/{1}/items',
    'remove_users_list_items': 'users/{0}/lists/{1}/items/remove',
    'users_settings': 'users/settings'
}

# def md5(text):
# return hashlib.md5(text).hexdigest()

=======
trakt_apikey= ''
cp_apikey= ''
username =''
password = ''
cp_urls = {
           'base': 'http://localhost:5050/api/',
           'app_available': '%s/app.available',
           'category_list': '%s/category.list/',
           'movie_add': '%s/movie.add/?identifier=%s&category_id=%s'
           }

trakt_urls = {
        'base': 'https://api.trakt.tv/',
        'watchlist_shows': 'user/watchlist/shows.json/%s/%s',
        'get_watchlist_episodes': 'user/watchlist/episodes.json/%s/%s',
        'get_watchlist_movie': 'user/watchlist/movies.json/%s/%s',
        'get_user_list': 'user/list.json/%s/%s/%s',
        'get_user_lists': 'user/lists.json/%s/%s',
        'get_library_shows': 'user/library/shows/all.json/%s/%s',
        'get_library_movies': 'user/library/movies/all.json/%s/%s',
        'get_show_seasons': 'show/seasons.json/%s/%s',
        'get_show_season': 'show/season.json/%s/%s/%s',
        'post_list_add': 'lists/add/%s',
        'post_listitem_add': 'lists/items/add/%s',
        'post_listitem_delete': 'lists/items/delete/%s',
        'post_show_library': 'show/library/%s',
        'post_movie_library': 'movie/library/%s',
        'post_episode_library': 'show/episode/library/%s',
        'post_season_library': 'show/season/library/%s',
        }

# def md5(text):
#     return hashlib.md5(text).hexdigest()
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1

def sha1(text):
    return hashlib.sha1(text).hexdigest()

<<<<<<< HEAD

def readconfigfile(f):
    logger.info('Parsing configuration file.')
    config_object = ConfigParser.ConfigParser()
    try:
        config_object.readfp(f)
    except ConfigParser.Error, err:
        logger.exception('Cannot parse configuration file, error: {0}!'.format(err))
        return
    else:
        logger.info('Successfully parsed configuration file.')
        return config_object


def iscpavailable(url_path):
    url = None
    logger.info('Check to see if Couch Potato is available')
    logger.info('HTTP request: {0}'.format(url_path))

    try:
        request = urllib2.Request(url_path)
=======
def IsCPAvailable(url_path):
    logger.info('Check to see if Couch Potato is available')
    request = cp_urls['base'] + url_path % cp_apikey
    
    try:
        request = urllib2.Request(request)
        #request.add_header("Authorization", "Basic %s" % base64.encodestring('%s:%s' % (username, password)))
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1
        url = urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        if err.code == 404:
            pass
        else:
<<<<<<< HEAD
            logger.exception('urllib2 http error code : {0}'.format(err.code))
            logger.exception('urllib2 http error reason : {0}'.format(err.reason))
            return {"success": False}
    except urllib2.URLError, err:
        logger.exception('urllib2 url error reason : {0}'.format(err.reason))
=======
            logger.exception('urllib2 http error code : ' + str(err.code))
            logger.exception('urllib2 http error reason : ' + str(err.reason))
            return {"success": False}
    except urllib2.URLError, err:
        logger.exception('urllib2 url error reason : ' + str(err.reason))
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1
        return {"success": False}

    try:
        return json.load(url)
    except ValueError, e:
<<<<<<< HEAD
        logger.exception('Error in Couch Potato API: {0}'.format(e))
        return {"success": False}


def getsetcpdata(url_path, param1=None, param2=None):
    url = None
    logger.info('Calling Couch Potato API')
    if param1 is None and param2 is None:
        request = (cp_urls['base'] + url_path).format(cp_apikey)
    else:
        request = (cp_urls['base'] + url_path).format(cp_apikey, param1, param2)
    logger.info('HTTP request: {0}'.format(request))

    try:
        request = urllib2.Request(request)
=======
        logger.exception('Error in Couch Potato API: ' + e)
        return {"success": False}

def getsetCPData(url_path, param1=None, param2=None):
    logger.info('Calling Couch Potato API')
    if param1 is None and param2 is None:
        request = cp_urls['base'] + url_path % cp_apikey
    else:
        request = cp_urls['base'] + url_path % (cp_apikey, param1, param2)
    logger.info('HTTP request: "' + request)
    
    try:
        request = urllib2.Request(request)
        #request.add_header("Authorization", "Basic %s" % base64.encodestring('%s:%s' % (username, password)))
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1
        url = urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        if err.code == 404:
            pass
        else:
<<<<<<< HEAD
            logger.exception('urllib2 http error code : {0}'.format(err.code))
            logger.exception('urllib2 http error reason : {0}'.format(err.reason))
            return {"success": False}
    except urllib2.URLError, err:
        logger.exception('urllib2 url error reason : {0}'.format(err.reason))
        return {"success": False}

    try:
        return json.load(url)
    except ValueError, e:
        logger.exception('Error in Couch Potato API: {0}'.format(e))
        return {"success": False}


def istrakttokenexpired(url_path):
    logger.info('Checking Trakt.TV token expiration')
    logger.info('HTTP request: {0}'.format(url_path))

    request = urllib2.Request(url_path)
    request.add_header("Content-type", "application/json")
    request.add_header("trakt-api-version", 2)
    request.add_header("trakt-api-key", trakt_clientid)

    # need to provide this using auth response
    request.add_header("Authorization", "Bearer {0}".format(trakt_accesstoken))
    logger.debug('Request headers: {0}'.format(request.headers))

    try:
        urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        if err.code == 401:
            logger.warning('Token is expired or not valid')
            return 1
        else:
            logger.exception('urllib2 http error code : {0}'.format(err.code))
            logger.exception('urllib2 http error reason : {0}'.format(err.reason))
            return
    except urllib2.URLError, err:
        logger.exception('urllib2 url error reason : {0}'.format(err.reason))
        return
    finally:
            logger.debug('Request headers: {0}'.format(request.headers))


def refreshtrakttoken(url_path, post_data):
    url = None
    logger.info('Refreshing Trakt.TV access token')
    logger.info('HTTP request: {0}'.format(url_path))
    logger.debug('Post data: {0}'.format(post_data))

    try:
        request = urllib2.Request(url_path)
        request.add_header("Content-type", "application/json")
        url = urllib2.urlopen(request, json.dumps(post_data))
    except urllib2.HTTPError, err:
        logger.exception('urllib2 http error code : {0}'.format(err.code))
        logger.exception('urllib2 http error reason : {0}'.format(err.reason))
        return "HTTP Error {0}: {1}".format(err.code, err.reason)
    except urllib2.URLError, err:
        logger.exception('urllib2 url error reason : {0}'.format(err.reason))
        return

    try:
        trakt_return = json.load(url)
        if len(trakt_return) > 0:
            return trakt_return
        else:
            return url.getcode()
    except ValueError, e:
        logger.exception('Error in Trakt API: {0}'.format(e))
        return


def getsettraktdata(url_path, post_data=None):
    url = None
    logger.info('Calling Trakt.TV API')
    logger.info('HTTP request: {0}'.format(url_path))

    request = urllib2.Request(url_path)
    request.add_header("Content-type", "application/json")
    request.add_header("trakt-api-version", 2)
    request.add_header("trakt-api-key", trakt_clientid)

    # need to provide this using auth response
    request.add_header("Authorization", "Bearer {0}".format(trakt_accesstoken))
    logger.debug('Request headers: {0}'.format(request.headers))

    try:
        if post_data is None:
            url = urllib2.urlopen(request)
        else:
            logger.debug('Post data: {0}'.format(post_data))
            url = urllib2.urlopen(request, json.dumps(post_data))
    except urllib2.HTTPError, err:
        logger.exception('urllib2 http error code : {0}'.format(err.code))
        logger.exception('urllib2 http error reason : {0}'.format(err.reason))
        return "HTTP Error {0}: {1}".format(err.code, err.reason)
    except urllib2.URLError, err:
        logger.exception('urllib2 url error reason : {0}'.format(err.reason))
        return

    try:
        trakt_return = json.load(url)
        if len(trakt_return) > 0:
            return trakt_return
        else:
            return url.getcode()
    except ValueError, e:
        logger.exception('Error in Trakt API: {0}'.format(e))
        return


def gettraktusername(url):
    logger.info('Attempting to retrieve Trakt username.')
    trakt_result = getsettraktdata(url)
    if isinstance(trakt_result, (dict, list)):
        logger.info('Success, username: {0}'.format(trakt_result['user']['username']))
        return trakt_result['user']['username']
    else:
        logger.exception('Error retrieving Trakt username, return: {0}'.format(trakt_result))
        return


def createtraktlist(url, data):
    logger.info('Attempting to create the "{0}" list'.format(data['name']))
    trakt_result = getsettraktdata(url, data)
    if trakt_result == 201:
        logger.info('Successfully created the list')
        return 1
    elif isinstance(trakt_result, (dict, list)):
        if trakt_result['name'] == data['name']:
            logger.info('Successfully created the list')
            return 1
    else:
        logger.exception('Error creating the list, return: {0}'.format(trakt_result))
        return


def istraktlist(url, listname):
    logger.info('Checking to see if a list with the name "{0}" already exists'.format(listname))
    trakt_result = getsettraktdata(url)
    if isinstance(trakt_result, (dict, list)):
        for rs in trakt_result:
            if rs['name'] == listname:
                logger.info('The list already exists')
                return 1
    elif trakt_result == 200:
        logger.info('The list does not exist')
        return
    else:
        _Exit(1, 'An unknown error occurred determining if the "{0}" Trakt.tv list exists --- Error: {1}'
              .format(listname, trakt_result))


def gettraktslug(url, listname):
    logger.info('Retrieving Trakt.TV slug for the "{0}" list'.format(listname))
    trakt_result = getsettraktdata(url)
    if isinstance(trakt_result, (dict, list)):
        for rs in trakt_result:
            if rs['name'] == listname:
                logger.info('Slug found: {0}'.format(rs['ids']['slug']))
                return rs['ids']['slug']
    elif trakt_result == 200:
        logger.info('Unable to find slug')
        return ''
    else:
        _Exit(1, 'An unknown error occurred determining the Trakt.tv list slug for {0} list --- Error: {1}'
              .format(listname, trakt_result))


def pushbullet_push(message=''):
    if pb_token is None:
        return

    url = None
    logger.info('Sending Pushbullet notification.')
    logger.info('Message body: {0}'.format(message))

    request = pb_url
    logger.info('HTTP request: {0}'.format(request))

    post_data = {'type': 'note',
                 'title': os.path.splitext(os.path.basename(__file__))[0],
                 'body': message
    }

    try:
        request = urllib2.Request(request)
        request.add_header("Content-Type", "application/json")
        request.add_header("Authorization", "Bearer {0}".format(pb_token))
        logger.debug('Request headers: {0}\nPost data: {1}'.format(request.headers, post_data))
=======
            logger.exception('urllib2 http error code : ' + str(err.code))
            logger.exception('urllib2 http error reason : ' + str(err.reason))
            return {"success": False}
    except urllib2.URLError, err:
        logger.exception('urllib2 url error reason : ' + str(err.reason))
        return {"success": False}
    
    try:
        return json.load(url)
    except ValueError, e:
        logger.exception('Error in Couch Potato API: ' + e)
        return {"success": False}

def getTraktData(url_path, add_param=None):
    if add_param is None:
        request = trakt_urls['base'] + url_path % (trakt_apikey, username)
    else:
        request = trakt_urls['base'] + url_path % (trakt_apikey, username, add_param)
    logger.info('HTTP request: "' + request)
    
    try:
        request = urllib2.Request(request)
        request.add_header("Authorization", "Basic %s" % base64.encodestring('%s:%s' % (username, password)))
        url = urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        if err.code == 404:
            pass
        else:
            logger.exception('urllib2 http error code : ' + str(err.code))
            logger.exception('urllib2 http error reason : ' + str(err.reason))
            return
    except urllib2.URLError, err:
        logger.exception('urllib2 url error reason : ' + str(err.reason))
        return
    
    try:
        return json.load(url)
    except ValueError, e:
        logger.exception('Error in Trakt API: ' + e)
        return

def postTraktData(url_path, post_data):
    request = trakt_urls['base'] + url_path % trakt_apikey
    logger.info('HTTP request: "' + request)
    
    try:
        request = urllib2.Request(request)
        request.add_header("Content-Type", "application/json")
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1
        url = urllib2.urlopen(request, json.dumps(post_data))
    except urllib2.HTTPError, err:
        if err.code == 404:
            pass
        else:
<<<<<<< HEAD
            logger.exception('urllib2 http error code : {0}'.format(err.code))
            logger.exception('urllib2 http error reason : {0}'.format(err.reason))
            return
    except urllib2.URLError, err:
        logger.exception('urllib2 url error reason : {0}'.format(err.reason))
        return

    try:
        pb_return = json.load(url)
        if len(pb_return) > 0:
            logger.info('Successfully sent Pushbullet notification.')
        else:
            logger.exception('Error sending Pushbullet notification.')
        return
    except ValueError, e:
        logger.exception('Error in Pushbullet API: {0}'.format(e))
        return


def _Exit(err=0, message=''):
    if len(message) == 0:
        if err > 0:
            message = 'Error {0} occured, please check the log file:\n{1}'.format(err, logfile)
        else:
            message = 'The script has successfully completed.'

    if len(movies_added) > 0:
        message = 'The following movie(s) were added to Couch Potato:\n\n- {0}' \
            .format('\n- '.join(map(str, movies_added)))
    else:
        if err > 0:
            logger.error('Error {0} --- {1}'.format(err, message))

        elif err_count > 0:
            message = '{0}  However, {1} warning(s) were recorded.'.format(message, err_count)
            logger.warning(message)
        else:
            logger.info(message)

    if len(pb_msg) > 0:
        message = '{0}\n\nMore information:{1}'.format(message, pb_msg)

    # Pushbullet push
    if err >= 0:
        pushbullet_push(message)
    else:  # suppress pushbullet for normal exits
        logger.info('Normal exit, Pushbullet notification suppressed.')
    logger.info('Exiting the script.')
    logger.info('-' * 80)
    sys.exit(err)

=======
            logger.exception('urllib2 http error code : ' + str(err.code))
            logger.exception('urllib2 http error reason : ' + str(err.reason))
            return
    except urllib2.URLError, err:
        logger.exception('urllib2 url error reason : ' + str(err.reason))
        return
    
    try:
        return json.load(url)
    except ValueError, e:
        logger.exception('Error in Trakt API: ' + e)
        return

def createTraktList(url, data):
    trakt_result = postTraktData(url, data)
    if trakt_result['status'] == 'success':
        logger.info('Successfully created the "' + data['name'] + '" list has been created --- ' + trakt_result['message'])
    else:
        if 'already exists' in trakt_result['error']:
            logger.info('The "' + data['name'] + '" list already exists --- ' + trakt_result['error'])
        else:
            logger.error('Error creating the "' + data['name'] + '" list --- ' + trakt_result['error'])
            return
    return 1
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1

# enter main method
if __name__ == "__main__":

    # create logging object
    logger = logging.getLogger(__name__)
<<<<<<< HEAD
    if __debug__:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

=======
    logger.setLevel(logging.INFO)
    
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1
    # create a file handler
    if args.log is not None and len(args.log) > 0:
        logfile = args.log
    else:
<<<<<<< HEAD
        # logfile = os.path.splitext(os.path.basename(__file__))[0] + '.log'
        logfile = '{0}//{1}.log'.format(os.path.dirname(os.path.realpath(__file__)),
                                        os.path.splitext(os.path.basename(__file__))[0])
    handler = logging.FileHandler(logfile)
    if __debug__:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    if __debug__:
        logger.info('Debug logging enabled')
    else:
        logger.info('Debug logging disabled')

    # read config file
    filepath = '{0}//config.ini'.format(os.path.dirname(os.path.realpath(__file__)))
    try:
        configfile = open(filepath, 'r')
    except IOError as e:
        _Exit(1, 'I/O error({0}): {1}'.format(e.errno, e.strerror))
    else:
        logger.info('Configuration file exists at the following path: {0}'.format(filepath))
        logger.info('Attempting to parse config file contents.')

    # configfile = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), 'config.ini')
    config = readconfigfile(configfile)
    configfile.close()
    if isinstance(config, ConfigParser.ConfigParser):
        # trakt config settings
        if config.has_section('trakt'):
            if config.has_option('trakt', 'clientid'):
                trakt_clientid = config.get('trakt', 'clientid')
            if config.has_option('trakt', 'clientsecret'):
                trakt_clientsecret = config.get('trakt', 'clientsecret')
            if config.has_option('trakt', 'accesstoken'):
                trakt_accesstoken = config.get('trakt', 'accesstoken')
            if config.has_option('trakt', 'refreshtoken'):
                trakt_refreshtoken = config.get('trakt', 'refreshtoken')
            if config.has_option('trakt', 'redirecturi'):
                trakt_redirect_uri = config.get('trakt', 'redirecturi')

        # couch potato settings
        if config.has_section('couchpotato'):
            if config.has_option('couchpotato', 'apikey'):
                cp_apikey = config.get('couchpotato', 'apikey')
            if config.has_option('couchpotato', 'apiurl'):
                cp_urls['base'] = config.get('couchpotato', 'apiurl')  # hard code the url of CP server api

        # pushbullet settings
        if config.has_section('pushbullet'):
            if config.has_option('pushbullet', 'token'):
                pb_token = config.get('pushbullet', 'token')
            if config.has_option('pushbullet', 'apiurl'):
                pb_url = config.get('pushbullet', 'apiurl')
    else:
        _Exit(1, 'Unable to parse config file!')

    # check for Couch Potato availability
    cp_available = iscpavailable(cp_urls['base'] + cp_urls['app_available'].format(cp_apikey))
    if cp_available['success']:
        logger.info('Success, Couch Potato is available.')
    else:
        _Exit(2, 'Couch Potato does not appear to be available.')

    # get category data from Couch Potato
    logger.info('Attempting to retrieve category information from Couch Potato.')
    cp_categories = getsetcpdata(cp_urls['category_list'])
    category_list = None
    if cp_categories['success']:
        logger.info('At least one or more categories was found, querying for name and id.')
        category_list = []
        for rs in cp_categories['categories']:  # changed from 'list' to 'categories' (CPS API change)
            category_list.append({
                'name': rs['label'],
                'id': rs['_id']  # changed from 'id' to '_id' (CPS API change)
            })
            # changed from 'id' to '_id' and %d to %s for unicode _id value (CPS API change)
            logger.info('name:{0}, id:{1}'.format(rs['label'], rs['_id']))
        if len(category_list) > 0:
            logger.info('Success, found {0} categories.'.format(len(category_list)))
        else:
            _Exit(2, 'Unable to build category list from Couch Potato.')
    else:
        _Exit(2, 'Error retrieving Couch Potato category information. Error: {0}'.format(cp_categories['error']))

    # verify Trakt authentication
    # check for 401 - unauthorized
    # if unauthorized perform a refresh token process
    if istrakttokenexpired(trakt_urls['base'] + trakt_urls['users_settings']):
        logger.warning("Trakt.TV access token is expired, attempting to refresh the token")
        data = {
            'refresh_token': trakt_refreshtoken,
            'client_id': trakt_clientid,
            'client_secret': trakt_clientsecret,
            'redirect_uri': trakt_redirect_uri,
            'grant_type': 'refresh_token'
            }
        trakt_result = refreshtrakttoken(trakt_urls['base'] + trakt_urls['refresh_token'], data)
        if isinstance(trakt_result, (dict, list)):
            # write access token and refresh token into config file
            trakt_accesstoken = trakt_result['access_token']
            trakt_refreshtoken = trakt_result['refresh_token']
            config.set('trakt', 'accesstoken', trakt_accesstoken)
            config.set('trakt', 'refreshtoken', trakt_refreshtoken)
            with open(filepath, 'w') as myconfig:
                config.write(myconfig)
        else:
            _Exit(3, "Unable to refresh access token")
    else:
        logger.info("Trakt.TV access token is valid")

    # get Trakt username
    trakt_username = gettraktusername(trakt_urls['base'] + trakt_urls['users_settings'])
    if len(trakt_username) == 0:
        _Exit(3, 'Unable to retrieve Trakt username.')
=======
        #logfile = os.path.splitext(os.path.basename(__file__))[0] + '.log'
        logfile = os.path.dirname(os.path.realpath(__file__)) + '\\' + os.path.splitext(os.path.basename(__file__))[0] + '.log'
    handler = logging.FileHandler(logfile)
    handler.setLevel(logging.INFO)
    
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # add the handlers to the logger
    logger.addHandler(handler)

    # check for Couch Potato availability
    cp_available = IsCPAvailable(cp_urls['app_available'])
    if cp_available['success'] == True:
        logger.info('Success, Couch Potato is available.')
    else:
        logger.error('Couch Potato does not appear to be available.')
        sys.exit(2)

    # get category data from Couch Potato
    logger.info('Attempting to retrieve category information from Couch Potato.')
    cp_categories = getsetCPData(cp_urls['category_list'])
    if cp_categories['success'] == True:
        logger.info('At least one or more categories was found, querying for name and id.')
        category_list = []
        for rs in cp_categories['categories']: # changed from 'list' to 'categories' (CPS API change)
            category_list.append({
                             'name': rs['label'],
                             'id': rs['_id']        # changed from 'id' to '_id' (CPS API change)
                             })
            logger.info('name:' + rs['label'] + ', id:%s' % rs['_id'])   # changed from 'id' to '_id' and %d to %s for unicode _id value (CPS API change)
        if len(category_list) > 0:
            logger.info('Success, found %d categories.' % len(category_list))
        else:
            logger.error('Unable to build category list from Couch Potato.')
            sys.exit(2)
    else:
        logger.error('Error retrieving category information. Error: ' + cp_categories['error'])
        sys.exit(2)
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1

    # create Trakt lists (that don't already exist) for Couch Potato categories
    logger.info('Attempting to create Trakt lists (that don\'t already exist) for Couch Potato categories.')
    for category in category_list:
<<<<<<< HEAD
        cat_name = str(category['name'])
        data = {
            'name': cat_name,
            'description': '',
            'privacy': 'private'
        }

        # if not istraktlist((trakt_urls['base'] + trakt_urls['users_lists']).format(trakt_username), category['name']):
        if not istraktlist((trakt_urls['base'] + trakt_urls['users_lists']).format(trakt_username), cat_name):
            if not createtraktlist((trakt_urls['base'] + trakt_urls['users_lists']).format(trakt_username), data):
                _Exit(3, 'Unable to create Trakt.TV list "{0}"'.format(cat_name))

        # create archive Trakt list (that don't already exist)
        # logger.info('Attempting to create Trakt archive lists (that don\'t already exist).')
        data['name'] += '_archive'
        if not istraktlist((trakt_urls['base'] + trakt_urls['users_lists']).format(trakt_username), data['name']):
            if not createtraktlist((trakt_urls['base'] + trakt_urls['users_lists']).format(trakt_username), data):
                _Exit(3, 'Unable to create Trakt.TV list "{0}"'.format(data['name']))

    # query trakt.tv for matching list slugs
    logger.info('Attempting to retrieve slug information for custom Trakt.tv lists.')
    i = 0
    for category in category_list:
        list_slug = gettraktslug((trakt_urls['base'] + trakt_urls['users_lists']).format(trakt_username),
                                 category['name'])
        if len(list_slug) > 0:
            i += 1
            category['slug'] = list_slug
        else:
            logger.warning('Unable to obtain slug information for {0}'.format(category['name']))

        list_slug = gettraktslug((trakt_urls['base'] + trakt_urls['users_lists']).format(trakt_username),
                                 category['name'] + '_archive')
        if len(list_slug) > 0:
            i += 1
            category['slug_archive'] = list_slug
        else:
            logger.warning('Unable to obtain slug information for {0}'.format(category['name']))

    if i > 0:
        logger.info('Success, retrieved {0} slug(s).'.format(i))
    else:
        _Exit(4, 'Error occured or no slug information was retrieved from Trakt.tv.')

    # query trakt.tv for list details using slug
    logger.info('Attempting to retrieve list items from Trakt.tv.')
    movies = []
    for category in category_list:
        logger.info('Retrieving items from the "{0}" list.'.format(category['name']))
        trakt_list_items = getsettraktdata((trakt_urls['base'] + trakt_urls['users_list_items'])
                                           .format(trakt_username, category['slug']))
        if isinstance(trakt_list_items, (dict, list)):
            i = 0
            for item in trakt_list_items:
                if item['type'] == 'movie':
                    i += 1
                    movies.append({
                        'title': item['movie']['title'],
                        'imdb_id': item['movie']['ids']['imdb'],
                        'cp_cat_id': category['id'],
                        'trakt_name': category['name'],
                        'trakt_slug': category['slug'],
                        'trakt_slug_archive': category['slug_archive']
                    })
            logger.info('Success, retrieved {0} movie(s) from the list.'.format(i))
        elif trakt_list_items == 200:
            pass
        else:
            _Exit(5, 'Error occured or no list information was retrieved from Trakt.tv.')

    if isinstance(movies, (dict, list)) and len(movies) > 0:
        logger.info('Total movie(s) retrieved: {0}.'.format(len(movies)))
    else:
        # no movies waiting to be added to Couch Potato (success)
        logger.warning('No movies found in any Trakt list(s), exiting.')
        _Exit(-1)  # Exit without pushbullet notification (this is a normal exit)

    # add movies into Couch Potato wanted list
    logger.info('Attempting to add movie(s) into Couch Potato wanted list.')
    for movie in list(movies):
        if len(movie['imdb_id']) > 0:
            cp_result = getsetcpdata(cp_urls['movie_add'], movie['imdb_id'], movie['cp_cat_id'])
            if cp_result['success']:
                movies_added.append(movie['title'])
                logger.info('Success, {0} has been added.'.format(movie['title']))
            else:
                err_count += 1
                logger.error('{0} was not added.  Error: {1}'.format(movie['title'], cp_result['error']))
                del movies[movies.index(movie)]
        else:
            err_count += 1
            logger.error('{0} was not added.  No IMDB ID was found for the movie'.format(movie['title']))
            pb_msg = '{0}\n{1} was not added.  No IMDB ID was found for the movie'.format(pb_msg, movie['title'])
            del movies[movies.index(movie)]

    if len(movies) > 0:
        logger.info('Total movie(s) added to Couch Potato: {0}.'.format(len(movies)))
    else:
        logger.warning('No movies were added to Couch Potato, exiting.')
        _Exit()

    # remove movie from Trakt list
    logger.info('Attempting to remove movie(s) from Trakt lists.')
    for movie in list(movies):
        logger.info('Removing {0} from the Trakt list (slug) "{1}".'.format(movie['title'], movie['trakt_slug']))
        data = {
            'movies': [
                {
                    'ids': {
                        'imdb': str(movie['imdb_id'])
                    }
                }
            ]
        }

        trakt_result = getsettraktdata(
            (trakt_urls['base'] + trakt_urls['remove_users_list_items']).format(trakt_username, movie['trakt_slug']),
            data)
        if isinstance(trakt_result, (dict, list)):
            if trakt_result['deleted']['movies'] > 0:
                logger.info('Success, the movie has been removed')
            else:
                err_count += 1
                logger.debug('Error, {0}'.format(trakt_result))
                logger.error('Error, unable to remove the movie.')
                del movies[movies.index(movie)]
                pb_msg = '{0}\nUnable to remove {1} from the Trakt list (slug) "{2}"\n'.format(pb_msg, movie['title'],
                                                                                               movie['trakt_slug'])
        else:
            _Exit(6, 'Error occured removing the item from the Trakt list.')

    if len(movies) > 0:
        logger.info('Total movie(s) removed from Trakt lists: {0}.'.format(len(movies)))
    else:
        logger.warning('No movies were removed from Trakt lists, exiting.')
        _Exit()

    # now we can add the movie into the archive list
    logger.info('Attempting to add movie(s) into Trakt archive lists.')
    for movie in movies:
        if movie['trakt_slug_archive'] is not None:
            logger.info(
                'Adding {0} to the archive Trakt list (slug) "{1}".'.format(movie['title'],
                                                                            movie['trakt_slug_archive']))
            data = {
                "movies": [
                    {
                        "ids": {
                            "imdb": movie['imdb_id']
                        }
                    }
                ]
            }

            trakt_result = getsettraktdata(
                (trakt_urls['base'] + trakt_urls['users_list_items']).format(trakt_username,
                                                                             movie['trakt_slug_archive']), data)
            if isinstance(trakt_result, (dict, list)):
                if trakt_result['added']['movies'] > 0:
                    logger.info('Success, the movie has been added to the archive list')
                elif trakt_result['existing']['movies'] > 0:
                    logger.info('Success, the movie was already in the archive list')
                else:
                    err_count += 1
                    logger.error('Error, unable to add the movie to the archive list.')
                    pb_msg = '{0}\nError, unable to add {1} to the archive list (slug) "{2}"\n'\
                        .format(pb_msg, movie['title'], movie['trakt_slug_archive'])
            else:
                _Exit(7, 'Error occurred adding the movies to the Trakt archive list.')

# Exit script
_Exit()
=======
        data = {
                'username': username,
                'password': sha1(password),
                'name': category['name'],
                'description': '',
                'privacy': 'private'
                }
        createTraktList(trakt_urls['post_list_add'], data)
        
        # create archive Trakt list (that don't already exist)
        logger.info('Attempting to create Trakt archive lists (that don\'t already exist).')
        data['name'] = data['name'] + '_archive'
        createTraktList(trakt_urls['post_list_add'], data)

    # query trakt.tv for matching list slugs
    logger.info('Attempting to retrieve slug information for custom Trakt.tv lists.')
    trakt_lists = getTraktData(trakt_urls['get_user_lists'])
    if len(trakt_lists) > 0:
        i = 0
        for rs in trakt_lists:
            for category in category_list:
                if rs['name'] == category['name']:
                    # get slug so we can get list details
                    i += 1
                    category['slug'] = rs['slug']
        logger.info('Success, retrieved %d slug(s).' % len(category_list))
    else:
        logger.error('Error occured or no information was retrieved.')
        sys.exit(4)
    
    # query trakt.tv for list details using slug
    logger.info('Attempting to retrieve list details from Trakt.tv.')
    movies = []
    for category in category_list:
        logger.info('Retrieving details for the "' + category['name'] + '" list.')
        trakt_list_details = getTraktData(trakt_urls['get_user_list'], category['slug'])
        if len(trakt_list_details) > 0:
            i = 0
            for item in trakt_list_details['items']:
                if item['type'] == 'movie':
                    i += 1
                    movies.append({
                            'title': item['movie']['title'],
                            'imdb_id': item['movie']['imdb_id'],
                            'cp_cat_id': category['id'],
                            'trakt_slug': category['slug']
                           })
            logger.info('Success, retrieved %d movie(s) from list.' % i)
        else:
            logger.error('Error occured or no information was retrieved.')
            sys.exit(5)

    if len(movies) > 0:
        logger.info('Total movie(s) retrieved: %d.' % len(movies))
    
        # add movies into Couch Potato wanted list
        logger.info('Attempting to add movie(s) into Couch Potato wanted list.')
        for movie in movies:
            cp_result = getsetCPData(cp_urls['movie_add'], movie['imdb_id'], movie['cp_cat_id'])
            if cp_result['success'] == True:
                logger.info('Success, ' + movie['title'] + ' has been added.')
                
                # remove movie from Trakt list
                logger.info('Removing ' + movie['title'] + ' from the Trakt list (slug) "' + movie['trakt_slug'] + '".')
                data = {
                        'username': username,
                        'password': sha1(password),
                        'slug': movie['trakt_slug'],
                        'items': [
                                  {
                                   'type': 'movie',
                                   'imdb_id': movie['imdb_id'],
                                   'title': movie['title']
                                   }
                                  ]
                        }
                trakt_result = postTraktData(trakt_urls['post_listitem_delete'], data)
                if trakt_result['status'] == 'success':
                    logger.info('Success, the movie has been removed --- ' + trakt_result['message'])
                else:
                    logger.error('Error, unable to remove the movie.')
                
                # add movie to archive Trakt list
                # first have to get the slug for the archive list
                logger.info('Attempting to retrieve slug information for custom Trakt.tv archive list.')
                trakt_lists = getTraktData(trakt_urls['get_user_lists'])
                if len(trakt_lists) > 0:
                    trakt_list = None
                    for rs in trakt_lists:
                        if rs['slug'] == movie['trakt_slug']:
                            # get slug so we can get list details
                            trakt_list = rs['name'] + '_archive'
                            break
                    
                    if trakt_list is not None:
                        for rs in trakt_lists:
                            if rs['name'] == trakt_list:
                                trakt_list = rs['slug']
                                break
                    
                    if trakt_list is not None:
                        logger.info('Success, retrieved ' + trakt_list + ' slug.')
                    else:
                        logger.error('Error, unable to determine the archive list slug.')
                else:
                    logger.error('Error occured or no information was retrieved.')
                    sys.exit(4)
                
                # now we can add the movie into the archive list
                if trakt_list is not None:
                    logger.info('Adding ' + movie['title'] + ' to the archive Trakt list (slug) "' + trakt_list + '".')
                    data = {
                            'username': username,
                            'password': sha1(password),
                            'slug': trakt_list,
                            'items': [
                                      {
                                       'type': 'movie',
                                       'imdb_id': movie['imdb_id'],
                                       'title': movie['title']
                                       }
                                      ]
                            }
                    trakt_result = postTraktData(trakt_urls['post_listitem_add'], data)
                    if trakt_result['status'] == 'success':
                        if trakt_result['inserted'] == 0:
                            logger.info('Success, the movie was already in the archive list --- %d changes made' % trakt_result['inserted'])
                        else:
                            logger.info('Success, the movie has been added to the archive list --- added %d' % trakt_result['inserted'])
                    else:
                        logger.error('Error, unable to add the movie to the archive list.')
                
            else:
                logger.error(movie['title'] + ' was not added.  Error: ' + cp_result['error'])

    else:
        logger.warning('No movies found in Trakt list, exiting.')
        
    logger.info('-' * 80)
>>>>>>> d07dc186797f001b72a00b999b2e47a36c86d3d1
