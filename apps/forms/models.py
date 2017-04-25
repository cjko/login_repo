# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import re, md5

NAME_REGEX = re.compile(r'^[a-zA-Z.-]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

# Create your models here.
class UserManager(models.Manager):

	def register(self, postData):

		errors = []

		if len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['email']) < 1 or len(postData['first_name']) < 1:
			errors.append('Missing field.')

		if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
			errors.append('First name and/or last name cannot be fewer than 2 characters.')

		if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
			errors.append('First name and/or last name can only contain letters.')

		if not EMAIL_REGEX.match(postData['email']):
			errors.append('Email is invalid.')

		if not PW_REGEX.match(postData['password']):
			errors.append('Password is invalid. Cannot be fewer than 8 characters.')

		if postData['password'] != postData['confirm_pw']:
			errors.append('Passwords do not match.')

		# search for email in database
		if User.objects.filter(email=postData['email']):
			errors.append('Email already exists.')

		return errors

	def create_user(self, postData):
		new_user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], encrypted_pw=postData['encrypted_pw'], salt=postData['salt'])
		return new_user.id

	def login(self, postData):

		errors = []

		if not User.objects.filter(email=postData['email']):
			errors.append('Username and/or password are invalid.')
		else:
			if md5.new(str(postData['password'])+str(User.objects.get(email=postData['email']).salt)).hexdigest() != User.objects.get(email=postData['email']).encrypted_pw:
				errors.append('Username and/or password are invalid.')

		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	encrypted_pw = models.CharField(max_length=255)
	salt = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

