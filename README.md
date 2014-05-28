trakt-to-couchpotato
=====

trakt-to-couchpotato is a simple Python script aimed at adding Trakt custom list contents to your Couch Potato wanted list.  The current Couch Potato automation does not give the ability to set the category or pull from multiple Trakt lists.  This script helps to alleviate that.

## Usage:
Be sure to edit the variables at the top of the script for Couch Potato api, Trakt api, username (trakt), password (trakt).  After that create a custom category in Couch Potato.  I named mine "Kids" and set a different To folder on the renamer options screen.  Upon running the python script for the first time it will create a new Trakt custom list named "Kids" and "Kids_archive".  From here on out all you have to do is add movies (on Trakt) into the custom "Kids" list.  The next time you run the script it will autoatmically take the movies in the "Kids" Trakt list and add them into the Couch Potato wanted list with the appropriate category set.  Upon successful addition into Couch Potato it will remove the movie from the "Kids" Trakt list and add it into the "Kids_archive" for historical data.  That's it!  The script can support multiple categories so just create as many categories as you need in Couch Potato.  The subsequent Trakt lists will be automatically created for you the next time it runs.

The script can be run manually but can easiliy be run as a cron job every 4 hours for example.

Features include:

* Ability to manage seperate Trakt movie lists
* Automatic creation of Trakt lists based on Couch Potato category names
* Movies added into Couch Potato with the proper category set
* Once movies are added to Couch Potato they are moved into an "_archive" Trakt list for historical data.

## Dependencies

To run trakt-to-couchpotato you will need Python 2.7+, a running instance of Couch Potato Server, and of course a Trakt account.
