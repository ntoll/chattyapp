# ChattyApp 💬

A world changing chat app to be acquired for billions 💰 at some point in the
future. This is Nicholas and Paul's totally legit (and not entirely serious)
retirement plan expressed in as few lines of code as possible. 💵👴🎉😉

More seriously, this is an example of using [PyScript](https://pyscript.net/)
as a frontend to a [Flask](https://flask.palletsprojects.com/en/stable/)-ish
application (we use the async
[Quart](https://quart.palletsprojects.com/en/latest/) framework, based on the
Flask API). We also use the wonderful [RoboHash](https://robohash.org/)
service for our goofy robot avatars. 🤖

This world changing technology was first announced by our visionary founders at
[FlaskCon](https://flaskcon.com/2025/) (a conference inside a conference) at
[PyConUS 2025](https://us.pycon.org/2025/).

Next step: add AI bandwagon. ✨

## Developer setup 🖥️🐍

* Clone the repository.
* Create and activate a virtual environment.
* `pip install -r requirements.txt` (currently only `quart` is needed).
* `make run` to serve locally.
* Point your browser[s] to: [localhost:8000](http://localhost:8000/)
* Chat! 💬

All source code is in the `chatty` directory.

There is (currently) no test suite. But if there were, we'd be using the
[uPyTest](https://github.com/pyscript/upytest) and
[uMock](https://github.com/pyscript/umock) frameworks for testing Python code
in the browser with PyScript. 🛠️

PRs welcome. 🤗

## PythonAnywhere Deployment

When demonstrating this app, we host it with the lovely folks at
[PythonAnywhere](https://pythonanywhere.com). Here are the steps we use to
deploy the application. We assume you already have an account with a
`<USERNAME>` associated with it. By the end of these steps you'll have a
version of this site running at `<USERNAME>.pythonanywhere.com`.

* If you have not done so already, you must create a PythonAnywhere API token.
  This is easy to do via
  [these instructions](https://help.pythonanywhere.com/pages/GettingYourAPIToken).
* Make sure you don't already have a website running at
  `<USERNAME>.pythonanywhere.com`. If you do, delete it.
* Open a fresh Bash console from your PythonAnywhere dashboard.
* From your home directory, clone the ChattyApp from GitHub:
  `git clone https://github.com/ntoll/chattyapp.git`
* In the new Bash console, install the command line tools:
  `pip install --upgrade pythonanywhere` (if you see errors, ignore them).
* Create a new virtual environment: `mkvirtualenv chatty --python=python3.10`
* Change into the `chattyapp` directory that was created when you cloned the
  app from GitHub: `cd chattyapp`
* Install the app's dependencies: `pip install -r requirements.txt`
* Install `uvicorn` (used to serve the app): `pip install "uvicorn[standard]"`
* Ensure you have a site _command_, used to start the server. You should use
  the following command but with `<USERNAME>` replaced with your actual
  username:
  `/home/<USERNAME>/.virtualenvs/chatty/bin/uvicorn --app-dir /home/<USERNAME>/chatty --uds ${DOMAIN_SOCKET} chatty.app:app`
* Create your website, and ensure `<USERNAME>` is replaced with your actual
  username. Also ensure `<COMMAND>` is replace with the command worked out in
  the previous step: `pa website create --domain <USERNAME>.pythonanywhere.com --command '<COMMAND>'`
* If everything was a success you should see a message like this:

```
< All done! Your site is now live at <USERNAME>.pythonanywhere.com. >
   \
    ~<:>>>>>>>>>
```

* To see details of your website: `pa website get --domain <USERNAME>.pythonanywhere.com`
* To restart/reload your website: `pa website reload --domain <USERNAME>.pythonanywhere.com`
* To delete your website: `pa website delete --domain <USERNAME>.pythonanywhere.com`
* If you encounter any problems, please check out the log files from the
  "Files" page in your PythonAnywhere console.

That's it. 🚀
