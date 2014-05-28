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

# declare variables
trakt_apikey= ''
cp_apikey= ''
username =''
password = ''
cp_urls = {
           'base': 'http://localhost:5050/api/',
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
            raise
    
    try:
        return json.load(url)
    except ValueError, e:
        logger.exception('Error in Couch Potato API: ' + e)
        return

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
            raise
    
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
            raise
    
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
            logger.warning('Unable to create the "' + data['name'] + '" list --- ' + trakt_result['error'])
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
    handler = logging.FileHandler(os.path.splitext(os.path.basename(__file__))[0] + '.log')
    handler.setLevel(logging.INFO)
    
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # add the handlers to the logger
    logger.addHandler(handler)

    # get category data from Couch Potato
    logger.info('Attempting to retrieve category information from CouchPotato.')
    cp_categories = getsetCPData(cp_urls['category_list'])
    if cp_categories['success'] == True:
        logger.info('At least one or more categories was found, querying for name and id.')
        category_list = []
        for rs in cp_categories['list']:
            category_list.append({
                             'name': rs['label'],
                             'id': rs['id']
                             })
            logger.info('name:' + rs['label'] + ', id:%d' % rs['id'])
        if len(category_list) > 0:
            logger.info('Success, found %d categories.' % len(category_list))
        else:
            logger.error('Unable to build category list from Couch Potato.')
            sys.exit(2)
    else:
        logger.error('Error retreiving category information. Error: ' + cp_categories['error'])
        sys.exit(2)

    # create Trakt lists (that don't already exist) for Couch Potato categories
    logger.info('Attempting to create Trakt lists (that don''t already exist) for Couch Potato categories.')
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
        logger.info('Attempting to create Trakt archive lists (that don''t already exist).')
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
        logger.info('Retreiving details for the "' + category['name'] + '" list.')
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
        logger.info('Attempting to add movie(s) into CouchPotato wanted list.')
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
                        logger.info('Success, the movie has been added to the archive list --- %d' % trakt_result['inserted'])
                    else:
                        logger.error('Error, unable to add the movie to the archive list.')
                
            else:
                logger.error(movie['title'] + ' was not added.  Error: ' + cp_result['error'])

    else:
        logger.warning('No movies found in Trakt list, exiting.')
        
    logger.info('-' * 80)
