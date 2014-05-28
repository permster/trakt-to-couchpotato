trakt-to-couchpotato
=====

trakt-to-couchpotato is a simple Python script aimed at adding Trakt custom list contents to your Couch Potato wanted list.  The current Couch Potato automation does not give the ability to set the category or pull from multiple Trakt lists.  This script helps to alleviate that.  The script can be run manually but can easiliy be run as a cron job every hour for example.

Features include:

* Ability to manage seperate Trakt movie lists
* Automatic creation of Trakt lists based on Couch Potato category names
* Movies added into Couch Potato with the proper category set
* Once movies are added to Couch Potato they are moved into an "_archive" Trakt list for historical data.

## Dependencies

To run trakt-to-couchpotato you will need Python 2.7+, a running instance of Couch Potato Server, and of course a Trakt account.
