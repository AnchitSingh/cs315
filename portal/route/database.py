from flask import Flask,abort, session, render_template, url_for, flash, redirect, request,send_file
from portal import app, db, bcrypt,mail
from portal.forms import *
from portal.models import *
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import os 
import json
import secrets
from os import path
from os.path import join, dirname, realpath
from sqlalchemy.sql.functions import func
from sqlalchemy.sql import text
from sqlalchemy import update
import pandas as pd

from datetime import datetime ,date ,timedelta

from flask import Response

import json
import os


from sqlalchemy import and_,or_
import requests
global cur_usr

from datetime import date
from datetime import datetime
from dateutil import parser
import urllib.request, json
from sqlalchemy import func
import codecs

import numpy as np
from portal.function import *
import MySQLdb
import time

