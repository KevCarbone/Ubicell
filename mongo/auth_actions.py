#!/usr/bin/env python

from tornado import database
import MySQLdb
from constants import *

import hashlib
import random

from bson import json_util
import pymongo
import models

import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def get_user_id(db,username):
	_id = db.user.find_one({'UserName' : username},{})
	return _id



def do_login(db,username,password):
	m = hashlib.md5()
	m.update(password)
	hashed = m.hexdigest()
	login = db.user.find_one({'UserName' : username, 'Password' : hashed})
	if login is not None:
		del login['Password']
		login['_id'] = str(login['_id'])

	print 'Login',login
	return login


def validate_email(email):
	if len(email) <= 0:
		return False;
	if not EMAIL_REGEX.match(email):
		return False
	
	per = email.rfind('.') 
	if per >= 0:
		suf = email[per+1:]
		if suf != 'edu':
			return False
	return True



def check_exists(db,field,item):
	item = db.user.find_one({field : item},{})
	return item != None

def do_register(db,user):
	print user
	password = user["Password"][0]
	m = hashlib.md5()
	m.update(password)
	password = m.hexdigest()
	username = user['UserName'][0]
	firstname = user['FirstName'][0]
	lastname = user['LastName'][0]
	email = user['Email'][0]
	user  = {'UserName' : username, 'Password' : password,'FirstName' : firstname, 'LastName' : lastname, 'Email' : email }
	return db.user.update({'UserName' : username},user,upsert=True)



def is_registered(db,cookie):
	req = db.get("select 1 from RegisterRequests where UserID = (select User.UserID from User inner join Cookie on User.UserID = Cookie.UserID and Cookie.CookieVal = %s)",cookie)
	if req is None:
		return True
	return False

def is_register_requested(db,cookie):
	req = db.get("select User.UserID from User inner join Cookie on User.UserID = Cookie.UserID and Cookie.CookieVal = %s",cookie)
	if req is None:
		return False
	userid = req["UserID"]
	req = db.get("select 1 from RegisterRequests where UserID = %s",userid)
	if req is None:
		return False
	return True


def main():
	print "Testing Database Connection"
	#db = database.Connection("localhost", "ProjectTakeOver",user="root",password="")
	#print db is not None
	#print "Testing Login"
	#cookie = do_login(db,"kmcarbone","kmcarbone")
	#print cookie
	db = pymongo.MongoClient().uplace

	# user_reg = {'UserName' : "kmcarbone",'Password' : "kmcarbone",'UID' : 1,'FirstName' : "Kevind",'LastName' : "Carbone", 'Email' : "kmcarbone16@gmail.com"}
	# user_reg2 = {'UserName' : "jillian",'Password' : "jillian",'UID' : 1,'FirstName' : "jillian",'LastName' : "Carbone", 'Email' : "jpcarbone@gmail.com"}


	# #print "Testing Registration"
	# userid = do_register(db,user_reg)

	# print userid
	print validate_email('kmc8206@blah.rit.edu')
	print check_exists(db,'Email','kmc8206@rit.edu')
	#print do_login(db,'njcbone2','blah')
	#print "Testing is_register_requested"
	#resp = is_register_requested(db,cookie)
	#print resp
	#db.close()


if __name__ == "__main__":
	main()