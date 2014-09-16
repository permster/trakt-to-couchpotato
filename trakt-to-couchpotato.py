#!/usr/bin/env python

# Check needed software dependencies
import sys
if sys.version_info < (2, 7):
    print "Sorry, requires Python 2.7."
    sys.exit(1)

import json
import urllib2
import base64
import hashlib
import logging
import os.path
import argparse

# argument parser
parser = argparse.ArgumentParser(description='Import trakt.tv movies into Couch Potato.')
parser.add_argument('-log', help='log file path')
args = parser.parse_args()

# declare variables
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

def sha1(text):
    return hashlib.sha1(text).hexdigest()

def IsCPAvailable(url_path):
    logger.info('Check to see if Couch Potato is available')
    request = cp_urls['base'] + url_path % cp_apikey
    
    try:
        request = urllib2.Request(request)
        #request.add_header("Authorization", "Basic %s" % base64.encodestring('%s:%s' % (username, password)))
        url = urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        if err.code == 404:
            pass
        else:
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
        url = urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        if err.code == 404:
            pass
        else:
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
        url = urllib2.urlopen(request, json.dumps(post_data))
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

# enter main method
if __name__ == "__main__":

    # create logging object
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # create a file handler
    if args.log is not None and len(args.log) > 0:
        logfile = args.log
    else:
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

    # create Trakt lists (that don't already exist) for Couch Potato categories
    logger.info('Attempting to create Trakt lists (that don\'t already exist) for Couch Potato categories.')
    for category in category_list:
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
