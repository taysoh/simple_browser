#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from browser.models import Clients
from browser.forms import ClientsForm
from stat import S_ISDIR
import paramiko 

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
def home(request):
	all_access = Clients.objects.all()
	if request.method=="POST":
		form = ClientsForm(request.POST)
		if form.is_valid:
			if request.POST['action']=='save':
				form.save()
				form = ClientsForm()
				return render_to_response( 'settings.html', {'form': form, 'add': True, 'all_access':all_access}, context_instance=RequestContext(request))
			elif request.POST['action']=='connect':
				# ssh = paramiko.SSHClient()
				# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(hostname=form['host'].value(), username=form['login'].value(), password=form['password'].value())
				ftp=ssh.open_sftp()
				path = form['startdir'].value()
				ftp.chdir(path)
				get=ftp.listdir()
				result=[]
				for single in get:
					if isdir(path+single, ftp):
						result.append(single)
				# ftp.close()
				# ssh.close()
				response = render_to_response( 'list.html', {'result':result, 'curdir': form['startdir'].value() }, context_instance=RequestContext(request))
				response.set_cookie('host', form['host'].value())
				response.set_cookie('login', form['login'].value())
				response.set_cookie('password', form['password'].value())
				return response
			else:
				form = ClientsForm()
				return render_to_response( 'settings.html', {'form': form, 'add': True, 'all_access':all_access}, context_instance=RequestContext(request))
			
		return render_to_response( 'settings.html', {'form':form}, context_instance=RequestContext(request))

	else:
		form= ClientsForm()
		response = render_to_response( 'settings.html', {'form': form, 'all_access': all_access}, context_instance=RequestContext(request))
		response.delete_cookie('host')
		response.delete_cookie('login')
		response.delete_cookie('password')
		return response

def connect(request):
	try:
		if request.method=="POST":
			access = Clients.objects.get(host = request.POST['connect'])
			# ssh = paramiko.SSHClient()
			# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=access.host, username=access.login, password=access.password)
			ftp=ssh.open_sftp()
			path = access.startdir
			ftp.chdir(path)
			get = ftp.listdir()
			result=[]
			for single in get:
				if isdir(path+single, ftp):
					result.append(single)
			ftp.close()
			ssh.close()
			response = render_to_response( 'list.html', {'result':result,'curdir': access.startdir}, context_instance=RequestContext(request))
			response.set_cookie('host', access.host)
			response.set_cookie('login', access.login)
			response.set_cookie('password', access.password)
			return response
		else:
			return redirect('/')	
	except:
		return redirect('/')

def go_to(request):
	try:
		if request.method=="GET":
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=request.COOKIES['host'], username=request.COOKIES['login'], password=request.COOKIES['password'])
			ftp=ssh.open_sftp()
			path = request.GET['to']
			ftp.chdir(path)
			get = ftp.listdir()
			result=[]
			for single in get:
				if isdir(path+single, ftp):
					result.append(single)
			ftp.close()
			ssh.close()
			split_path = path.split('/')
			prev=''
			for i in range(len(split_path)-2):
				prev = prev + str(split_path[i])+'/'
			return render_to_response( 'list.html', {'result':result,'curdir': path, 'prev': prev }, context_instance=RequestContext(request))
	except:
		return redirect('/')

def isdir(path, ftp):
  try:
    return S_ISDIR(ftp.stat(path).st_mode)
  except IOError:
    #Path does not exist, so by definition not a directory
    return False