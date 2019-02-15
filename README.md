# Canvasdata Import
Process for importing the Canvas Data Files into a MySQL Database

## What it does
Checks the Canvas Data API for a new file.  This script keeps track of imports in a database table called import_dumps
If it's new, it will fetch any new files that are specified and then import them into the database. 
We import the tables that we use for Starfish Early Alert first and then when that's done we bring in the rest that we want to download.  

## Create Database tables
Files in sql folder have scripts for making the db tables.  There may be a few missing that we don't use especially new tables.  There is a specific table called import_dumps that is needed for the canvas_data_checker script to check for a new file.  

## Setup/Config
THIS IS THE FILE YOU WILL SETUP!  There are fields for file locations and credentials.  

    config.py

## Running the Process
THIS IS THE FILE YOU WILL RUN!

    canvas_data_checker.py

