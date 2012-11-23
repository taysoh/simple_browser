#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from browser.models import Clients

class ClientsForm(ModelForm):
	class Meta:
		model = Clients
