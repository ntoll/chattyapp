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

That's it. 🚀
