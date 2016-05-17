# UnMemorize

A todo list responsive web app.

## Installation

Follow the next steps :

1. python manage.py syncdb
	- Answer no to "Would you like to create one now?"

2. Run the application using your favorite way (I'm using WSGI)
	Here's an example of virtualhost :

<VirtualHost *:80>

    ServerName unmemorize.mydomain.com
    ServerAlias unmemorize.mydomain.com
 
    WSGIScriptAlias / /<mypath>/unmemorize/unmemorize/wsgi.py
    Alias /static/ /<mypath>/unmemorize/todolist/static/

    <Location /static>
        Options -Indexes
    </Location>

</VirtualHost>

3. Open settings.py and fill the ALLOWED_HOSTS variable

4. Go to homepage : unmemorize.mydomain.com

5. Enter a new password, UnMemorize will create the user with the corresponding password

6. Enjoy!

## To do

Static dir must not be versioned.

