#!/usr/bin/bash

PASTER=/usr/local/bin/paster
PASTE_DEPLOY=paste.deploy

PYTHONPATH=. $PASTER serve --reload $PASTE_DEPLOY
