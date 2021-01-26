from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from urllib.parse import urlencode, urlsplit
import pprint as p

def youtubeFilter(el):
	url = el['href']
	if 'youtube' not in url:
		parts = urlsplit(url)
		path = parts.path

		if path.endswith('/'):
			path = path.split('/')[1:-1]
		elif path.endswith(''):
			path = path.split('/')[1:]

		if len(path) > 1:
			return False
		else:
			return True
	else:
		parts = urlsplit(url)
		if re.search('channel|user', parts.path) == None:
			return False
		else:
			return True
Social_Links = []
def Social_Exf(websites):
	scan = 0
	for site in websites:
		response = requests.get(site).text
		# regex = re.compile(r'<a.*>.*</a.*>')
		# match = re.findall(regex, response)
		# socials = [i for i in match if 'facebook' in i]
		# soup = BeautifulSoup(socials[0], features='html.parser')
		# print (soup.attrs['href'])
		# print(type(socials[0]))
		soup = BeautifulSoup(response, features='html.parser')
		link = soup.find_all('a', href=re.compile('https://www.facebook|instagram|twitter|linkin|yelp|youtube|pintrest|reddit|tiktok', re.I))
		link = filter(youtubeFilter, link)
		site_obj = {}
		site_socials = {}
		socials = set([i.attrs['href'] for i in link]) 
		for social in socials:
			parts = urlsplit(social)
			site_socials[parts.netloc] = social
			site_obj[site]= site_socials
		Social_Links.append(site_obj)
		# print(socials)
		# print('-'*60)
		scan +=1
		if scan == 5:
			break
	print(pd.DataFrame(Social_Links))
	# p.pprint(Social_Links)

df = pd.read_csv(r'C:\Users\carte\OneDrive\Documents\Python Code\Apartments_in_Raleigh, NC.csv')
# Social_Exf(df['Website'].tolist())
socials_regex = re.compile(r'(.*)S|social(s)?(\s)?(-)?')
# https://www.thelapartments.com/
# Social_Exf(["https://www.walktostate.com/"])
# Social_Exf(["http://www.google.com"])
Social_Exf(["http://montecitowestapartments.com/","https://www.walktostate.com/", "http://cwsapartments.com/", "http://shellbrookapartments.com/", "http://camdenliving.com/", "http://pineknollraleigh.com/"])