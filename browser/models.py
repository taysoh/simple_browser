 #-*- coding: utf-8 -*-
from django.db import models

class Clients(models.Model):
	host = models.CharField("Host", max_length=100 )
	login = models.CharField("Login", max_length=100 )
	password = models.CharField("Password", max_length=100 )
	startdir = models.CharField("startdir", max_length=100 , blank=True, null=True)

	def __unicode__(self):
		return str(self.login)+"@"+str(self.host)

	class Meta:
		verbose_name = u"Access"
		verbose_name_plural = u"Accesses"
		unique_together = (("host",),)