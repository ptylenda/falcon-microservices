#!/bin/bash

gunicorn -k tornado tornado_getresponse_app.app:app