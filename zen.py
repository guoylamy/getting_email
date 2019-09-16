import re
import sys
import json
import argparse
import threading
from requests import get
from requests.auth import HTTPBasicAuth


def findContributorsFromRepo(username, repo):
	response = get('https://api.github.com/repos/%s/%s/contributors?per_page=100' % (username, repo), auth=HTTPBasicAuth(uname, '')).text
	contributors = re.findall(r'https://github\.com/(.*?)"', response)
	return contributors

def findReposFromUsername(username,uname):
	print("username = ",username)
	response = get('https://api.github.com/users/%s/repos?per_page=100&sort=pushed' % username, auth=HTTPBasicAuth(uname, '')).text
	repos = re.findall(r'"full_name":"%s/(.*?)",.*?"fork":(.*?),' % username, response)
	nonForkedRepos = []
	for repo in repos:
		if repo[1] == 'false':
			nonForkedRepos.append(repo[0])
	return nonForkedRepos

def findEmailFromContributor(username, repo, contributor,uname,breach,jsonOutput):
	response = get('https://github.com/%s/%s/commits?author=%s' % (username, repo, contributor), auth=HTTPBasicAuth(uname, '')).text
	latestCommit = re.search(r'href="/%s/%s/commit/(.*?)"' % (username, repo), response)
	if latestCommit:
		latestCommit = latestCommit.group(1)
	else:
		latestCommit = 'dummy'
	commitDetails = get('https://github.com/%s/%s/commit/%s.patch' % (username, repo, latestCommit), auth=HTTPBasicAuth(uname, '')).text
	email = re.search(r'<(.*)>', commitDetails)
	if email:
		email = email.group(1)
		if breach:
			jsonOutput[contributor] = {}
			jsonOutput[contributor]['email'] = email
			if get('https://haveibeenpwned.com/api/v2/breachedaccount/' + email).status_code == 200:
				email = email + start + 'pwned' + stop
				jsonOutput[contributor]['pwned'] = True
			else:
				jsonOutput[contributor]['pwned'] = False
		else:
			jsonOutput[contributor] = email
	return email

def findEmailFromUsername(username,uname,breach,jsonOutput):
	repos = findReposFromUsername(username,uname)
	for repo in repos:
		email = findEmailFromContributor(username, repo, username,uname,breach,jsonOutput)
		if email:
			return email
			break



def all(url,username):
	inp = url
	breach = url
	output = None
	organization = False
	uname = 'guoylamy@shanghaitech.edu.cn'
	thread_count = 2

	colors = True # Output should be colored
	machine = sys.platform # Detecting the os of current system


	if inp.endswith('/'):
		inp = inp[:-1]

	targetOrganization = targetRepo = targetUser = False

	jsonOutput = {}

	if inp.count('/') < 4:
		if '/' in inp:
			username = inp.split('/')[-1]
		else:
			username = inp
		if organization:
			targetOrganization = True
		else:
			targetUser = True
	elif inp.count('/') == 4:
		targetRepo = inp.split('/')
		username = targetRepo[-2]
		repo = targetRepo[-1]
		targetRepo = True
	else:
		print ('%s Invalid input' % bad)
		quit()

	return findEmailFromUsername(username,uname,breach,jsonOutput)

#all('https://github.com/guoylamy','guoylamy')