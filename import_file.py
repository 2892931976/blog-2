# coding: utf-8

import re
import os
import sys
import time
import json
import redis
import requests
import logging
import urllib
import logging.handlers
import warnings
import pymysql
import uuid
import socket
import datetime
import qrcode
 
from platform import system
from functools import wraps
from pbkdf2 import PBKDF2

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from tornado.web import url, StaticFileHandler , RequestHandler, Finish
import tornado.log
import tornado.websocket 
from tornado.util import  PY3
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from pycket.session import SessionMixin

from sqlalchemy import create_engine, event, desc, or_
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, contains_eager, deferred
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import DisconnectionError
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean, DATE, BigInteger

try:
    import configparser
except: 
    import ConfigParser as configparser
  
try:  
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance  
except ImportError:  
    import Image, ImageDraw, ImageFont, ImageEnhance 
 
try:
   import cPickle as pickle
except:
   import pickle
   
try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO
    
    