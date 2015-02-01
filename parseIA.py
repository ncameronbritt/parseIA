from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin


def getURLs(start_url, soup, domain):
	# container for urls
	links =[]
	# get href from all a tags
	for link in soup.find_all('a'):
		#if str(link.get('href')).startswith(url):
		new_url = link.get('href')
		if str(new_url).startswith('mailto'):
			continue
		#construct valid url from relative path
		if str(new_url).startswith('/'):
			new_url= urljoin(start_url, new_url)
		# only include urls from domain we're interested in	
		if domain in str(new_url):
			links.append(new_url)

	# remove duplicates with set()
	links = set(links)

	return links

def getTitle(soup):
	if soup.title is not None:
		return soup.title.string
	else:
		return "Invalid title"

def get_web_page(url):
	try:
		response = urllib2.urlopen(url, timeout=5)
		try:
			return response.read()
		finally:
			response.close()
	# ignore errors 	
	except (urllib2.HTTPError, urllib2.URLError):
		pass
	

def makeSoup(data):
	if data is not None:
		soup = BeautifulSoup(data)
		return soup
	else: 
		return -1


if __name__ == "__main__":

	domain = "nasa.gov"
	start_url = "http://www.nasa.gov"
	data = get_web_page(start_url)
	soup = makeSoup(data)
	if soup != -1:
		depth1 = getURLs(start_url, makeSoup(data), domain)
	for url in depth1:
		try: 
			print(20*'**')
			#print(url)
			data = get_web_page(url)
			soup = makeSoup(data)
			if soup != -1:
				print(getTitle(soup))
				depth2 = getURLs(url, soup, domain)
		# ignore unicode error. Proobably not the best...
		except UnicodeEncodeError:
			pass
		for url in depth2:
			try:
				data = get_web_page(url)
				soup = makeSoup(data)
				if soup != -1:
					print("\t" + getTitle(soup))
					#depth2 = getURLs(url, makeSoup(data), domain) 
				#print("+"+ 4*" " + url)
			except UnicodeEncodeError:
				pass


