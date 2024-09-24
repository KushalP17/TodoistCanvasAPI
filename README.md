### ToDo List Updater

## What it does:

This program uses pycURL & Todoist's Python RestAPI SDK to scrape Canvas for assignments (with due date & description) and autofill and update it in Todoist. 

This relies on Task Scheduler to run main.py for the updating to occur, but there are certainly other means necessary to automate this.

Setup involves running Start.py, which should autopopulate all local XML files and give a UI for user information to be entered easily enough. This will create Todoist Tasks of each entered class in the user-specified Todoist Project, in which all scraped assignments will be gathered as subtasks in each class task.

Basic Control Flow is as follows:
For each Canvas class:
    Scrape each Assignment & its Data
    Parse Descripton from HTML to something more readable
    Load Assignment into corresponding Todoist Class Task
    Log any errors encountered


## Startup UI

## Output in Todoist

## Task Scheduler Settings/Recommendations (if applicable)