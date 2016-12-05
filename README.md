trakt-to-couchpotato
=====

trakt-to-couchpotato is a simple Python script aimed at adding Trakt custom list contents to your Couch Potato wanted list.  The built-in Couch Potato automation does not give the ability to set the category or pull from multiple Trakt lists.  This script helps to alleviate that.

## Usage:
Minimal knowledge of the Trakt API helps to get started: http://docs.trakt.apiary.io/

Before running be sure to edit the config.ini file with your specific information.
* Trakt client id
* Trakt client secret
* Trakt access token
* Trakt refresh token
* Couch Potato url (optional) (default - http://localhost:5050/api)
* Couch Potato API key
* Pushbullet url (optional) (default - https://api.pushbullet.com/v2/pushes)
* Pushbullet token (optional)

If your unsure of how to get the client id, secret, access token, and refresh token please see issue #2 for high level steps on how to get them.

After the config file is configured be sure to create your custom categories in Couch Potato.  For this example let's create a category named "Kids" and set a different "To" folder on the renamer options screen for the newly created category.

Upon running the python script for the first time it will automatically create a new Trakt custom list named "Kids" and "Kids_archive" (if they don't already exist).  From here on out all you have to do is add movies (on Trakt) into the custom "Kids" list.  The next time you run the script it will automatically take the movies in the "Kids" Trakt list and add them into the Couch Potato wanted list with the matching Couch Potato category "Kids" set.  Upon successful addition into Couch Potato it will remove the movie from the "Kids" Trakt list and add it into the "Kids_archive" list for historical purposes.  That's it!  The script can support multiple categories so just create as many categories as you need in Couch Potato.  The subsequent Trakt lists will be automatically created for you the next time it runs.

The script can be run manually but can easiliy be scheduled to run as a cron job for example.

Features include:

* Config file for easy setting manipulation.
* Ability to manage seperate Trakt movie lists.
* Automatic creation of Trakt lists based on Couch Potato category names.
* Movies added into Couch Potato with the proper category set.
* Once movies are added to Couch Potato they are moved into an "_archive" Trakt list for historical data.
* Optional PushBullet support for notifications.
* Optional -log switch to specify a log file path. (defaults to script directory if not specified)

## Dependencies

To run trakt-to-couchpotato you will need Python 2.7+, a running instance of Couch Potato Server, and of course a Trakt account.  Pushbullet support is optional for notifications.
