# Noob EventBot
The Events-driven API for Noob SNHUbot

## File Tree

```bash
$ tree --dirsfirst -I *pycache*
.
├── docs
│   └── README.md
├── instance
│   └── config.py
├── noob_eventbot
│   ├── root
│   │   ├── __init__.py
│   │   ├── healthcheck.py
│   │   └── index.py
│   └── __init__.py
├── Pipfile
├── Pipfile.lock
├── config.py
├── requirements.txt
└── run.py
```

## Development
Get started with `pipenv install`, or if you like `pip install -r requirements.txt`.

I'm using `ngrok` to proxy down to my local development environment for testing. Google it.  
This also makes me need to change the Events Request URL on the Test Bot in the Slack Bot settings.

