#!/usr/bin/env python

# Check needed software dependencies
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

if sys.version_info < (2, 7):
    print "Sorry, requires Python 2.7."
    sys.exit(1)

import json
import urllib2
# import base64
import hashlib
import logging
import os.path
import argparse

# argument parser
parser = argparse.ArgumentParser(description='Import trakt.tv movies into Couch Potato.')
parser.add_argument('-log', help='log file path')
args = parser.parse_args()

# declare variables
trakt_username = 'permster'
trakt_clientid = '8fea463b20f6ef6bb40ca8112b0e06ca7c2839fecd6406c07a6981d701d955b0'
trakt_accesstoken = '6783d9b5994a3a7782e89be4adb6f7c0045554c882179e0d05eb8f079a3f0ddb'
cp_apikey = '0b5e7a4883354826a9afb70463b16fcf'
pb_token = 'v1gxdOJLbQoxzCSvBsl5dAQDxvI1cx50QwujBCeBWZgui'
movies_added = []
err_count = 0
pb_msg = ''
cp_urls = {
    'base': 'http://localhost:5050/api/',
    'app_available': '{0}/app.available',
    'category_list': '{0}/category.list/',
    'movie_add': '{0}/movie.add/?identifier={1}&category_id={2}'
}

if __debug__:
    cp_urls['base'] = 'http://192.168.7.10:5050/api/'

trakt_urls = {
    'base': 'https://api-v2launch.trakt.tv/',
    'users_list': 'users/{0}/lists/{1}',
    'users_lists': 'users/{0}/lists',
    'users_list_items': 'users/{0}/lists/{1}/items',
    'remove_users_list_items': 'users/{0}/lists/{1}/items/remove'
}

# def md5(text):
# return hashlib.md5(text).hexdigest()


def sha1(text):
    return hashlib.sha1(text).hexdigest()


def iscpavailable(url_path):
    url = None
    logger.info('Check to see if Couch Potato is available')
    request = (cp_urls['base'] + url_path).format(cp_apikey)

    try:
        request = urllib2.Request(request)
        url = urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        if err.code == 404:
            pass
        else:
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
        url = urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        if err.code == 404:
            pass
        else:
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


def getsettraktdata(url_path, post_data=None):
    url = None
    logger.info('Calling Trakt.TV API')
    logger.info('HTTP request: {0}'.format(url_path))

    try:
        request = urllib2.Request(url_path)
        request.add_header("Content-type", "application/json")
        request.add_header("trakt-api-version", 2)
        request.add_header("trakt-api-key", trakt_clientid)
        request.add_header("Authorization", "Bearer {0}".format(trakt_accesstoken))
        if post_data is None:
            url = urllib2.urlopen(request)
        else:
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
    url = None
    logger.info('Sending Pushbullet notification.')
    logger.info('Message body: {0}'.format(message))

    request = 'https://api.pushbullet.com/v2/pushes'
    logger.info('HTTP request: {0}'.format(request))

    post_data = {'type': 'note',
                 'title': os.path.splitext(os.path.basename(__file__))[0],
                 'body': message
    }

    try:
        request = urllib2.Request(request)
        request.add_header("Content-Type", "application/json")
        request.add_header("Authorization", "Bearer {0}".format(pb_token))
        url = urllib2.urlopen(request, json.dumps(post_data))
    except urllib2.HTTPError, err:
        if err.code == 404:
            pass
        else:
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


# enter main method
if __name__ == "__main__":

    # create logging object
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    if args.log is not None and len(args.log) > 0:
        logfile = args.log
    else:
        # logfile = os.path.splitext(os.path.basename(__file__))[0] + '.log'
        logfile = '{0}//{1}.log'.format(os.path.dirname(os.path.realpath(__file__)),
                                        os.path.splitext(os.path.basename(__file__))[0])
    handler = logging.FileHandler(logfile)
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    # check for Couch Potato availability
    cp_available = iscpavailable(cp_urls['app_available'])
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

    # create Trakt lists (that don't already exist) for Couch Potato categories
    logger.info('Attempting to create Trakt lists (that don\'t already exist) for Couch Potato categories.')
    for category in category_list:
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
                        'imdb': movie['imdb_id']
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



