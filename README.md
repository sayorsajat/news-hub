# news hub
## Problem it solves
Trying to figure out what news sites are out there can take many days. When you finally figure out which sites are right for you, you will have to constantly switch from one site to another. It would seem that news aggregators are the solution... or are they? You don't know where aggregators get their news from, you can't edit the list of sources. Let's be honest, how much news are you really interested in? Even recommendation algorithms will not help, as they only give you the information that makes you use the service more, not the information that you actually need.
## My solution
Dynamically collects news from websites listed in news_sources.csv file inside /lib directory and puts it in postgres database.
Just go inside .csv file and add sources you like!

## Setting up
set up postgres database (the process may be different for different operating systems) and create .env file in root directory in this format:
```
postgres_host=localhost
postgres_port=5432
dbname=name_of_db_you_created
user_name=name_of_user_that_has_access_to_database
user_pass=password_of_the_user
```
postgres_host and postgres_port may be different for you, but usually the values ​​are like this

then install python dependencies by 
```
pip install -r requirements.txt
```

To add sources to gather from, just add to /lib/news_sources.csv as many lines as you wish in format:
```csv
url_of_your_website;yes
```
or
```csv
url_of_your_website;no
```
It depends on whether the description of the news is available to everyone

### TODO:
- [x] description gathering
- [x] gui for news viewing
- [x] urgency measurement
- [ ] multiple dashboards accessed by id
- [ ] deploy