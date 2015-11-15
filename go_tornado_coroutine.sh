#!/bin/bash

gunicorn -k tornado tornado_coroutine_app.app:app