[![Join UCF Open Slack Discussions](https://ucf-open-slackin.herokuapp.com/badge.svg)](https://ucf-open-slackin.herokuapp.com/)

# LTI Template for Python and Flask

## Setup

### Virtual Environment
Create a virtual environment that uses Python 2:

```
virtualenv venv -p /usr/bin/python2.7
source venv/bin/activate
```

Install the dependencies from the requirements file. 

```
pip install -r requirements.txt
```

### Create your local settings file
Create settings.py from settings.py.template

```
cp settings.py.template settings.py
```

Note: settings.py is alreay referenced in the .gitignore and multiple python files, if you want a different settings file name be sure to update the references.

#### Add your values to the settings file.
At a minimum, CONSUMER_KEY, SHARED_SECRET, and secret_key need to be input by the developer. The secret_key is used by Flask, but the CONSUMER_KEY and SHARED_SECRET will be used in setting up the LTI. For security purposes, it's best to have randomized keys. You can generate random keys in the command line by using os.urandom(24) and inputing the resulting values into the settings.py file:

```
import os
os.urandom(24)
```

### Run a Development Server
Here's how you run the flask app from the terminal:
```
export FLASK_APP=views.py
flask run
```

### Open in a Browser
Your running server will be visible at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Install LTI in Canvas
- Have the XML, consumer key, and secret ready.
    - You can use the [XML Config Builder](https://www.edu-apps.org/build_xml.html) to build XML.
- Navigate to the course that you would like the LTI to be added to. Click Settings in the course navigation bar. Then, select the Apps tab. Near the tabs on the right side, click 'View App Configurations'. It should lead to a page that lists what LTIs are inside the course. Click the button near the tabs that reads '+ App'.
- A modal should come up that allows you to customize how the app gets added. Change the configuration in the Configuration Type dropdown menu to 'By URL' or 'Paste XML' depending on how you have your LTI configured. If your LTI is publicly accessible, 'By URL' is recommended. From there, fill out the Name and Consumer Keys, and the Config URL or XML Configuration. Click Submit.
- Your LTI will appear depending on specifications in the XML. Currently, they get specified in the **options** tag within the **extensions** tag. Extensions can include these options:
    - Editor Button (visible from within any wiki page editor in Canvas)
    - Homework Submission (when a student is submitting content for an assignment)
    - Course Navigation (link on the lefthand nav)
    - Account Navigation (account-level navigation)
    - User Navigation (user profile)

**Note**: If you're using Canvas, your version might be finicky about SSL certificates. Keep HTTP/HTTPS in mind when creating your XML and while developing your project. Some browsers will disable non-SSL LTI content until you enable it through clicking a shield in the browser bar or something similar.