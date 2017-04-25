# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from models import User
import md5, os, binascii

# Create your views here.
def index(request):
	return render(request, 'forms/index.html')

def register(request):

	salt = binascii.b2a_hex(os.urandom(15)),

	postData = {
		'first_name': request.POST['first_name'],
		'last_name': request.POST['last_name'],
		'email': request.POST['email'],
		'password': request.POST['password'],
		'confirm_pw': request.POST['confirm_pw'],
		'encrypted_pw': md5.new(str(request.POST['password']) + str(salt)).hexdigest(),
		'salt': salt,
	}


	# if no errors
	if not User.objects.register(postData):
		# add user to database
		new_user_id = User.objects.create_user(postData)
		request.session['user_id'] = new_user_id
		messages.success(request, 'Successfully registered!')

		return redirect('/success')

	for error in User.objects.register(postData):
		messages.error(request, error)

	return redirect('/')

def login(request):

	postData = {
		'email': request.POST['email'],
		'password': request.POST['password'],
	}

	#if no errors
	if not User.objects.login(postData):
		# find id matching email
		user_id = User.objects.get(email=postData['email']).id
		request.session['user_id'] = user_id
		messages.success(request, 'Successfully logged in!')
		return redirect('/success')

	for error in User.objects.login(postData):
		messages.error(request, error)

	return redirect('/')

def success(request):

	if 'user_id' in request.session:

		first_name = User.objects.get(id=request.session['user_id']).first_name

		context = {
			'first_name': first_name,
			'message': messages
		}

		return render(request,'forms/success.html', context)

	messages.error(request, 'You are not logged in!')

	return redirect('/')

def logout(request):

	request.session.clear()
	return redirect('/')











