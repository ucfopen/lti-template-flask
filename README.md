[![Join UCF Open Slack Discussions](https://ucf-open-slackin.herokuapp.com/badge.svg)](https://ucf-open-slackin.herokuapp.com/)

# LTI Template for Python and Flask

## Setup

### Docker
We are going to be creating a Docker container that uses Python 3:

#### Setup environment variables

```bash
cp .env-template .env
```

Now you can begin editing the `.env` file. At a minimum, CONSUMER_KEY, SHARED_SECRET, and SECRET_FLASK need to be input by the developer. The SECRET_FLASK is used by Flask, but the CONSUMER_KEY and SHARED_SECRET will be used in setting up the LTI. For security purposes, it's best to have randomized keys. You can generate random keys in the command line by using os.urandom(24) and inputing the resulting values into the .env file:

```
import os
os.urandom(24)
```

#### Build and run Docker Container

```bash
docker-compose build
docker-compose up
```

You should see something like this in your console:
```
[INFO] Starting gunicorn 20.1.0
[INFO] Listening at: http://0.0.0.0:9001 (1)
[INFO] Using worker: gthread
[INFO] Booting worker with pid: 11
```

Your server should now be and running.

### Open in a Browser
Your running server will be visible at [http://127.0.0.1:9001](http://127.0.0.1:9001)

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