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
		title = soup.title.string
		#remove leading whitespace and newlines
		title = title.strip().replace('\n', ' ')
		return title
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

def get_tree(max_depth, current_depth, url, start_url, domain): 
	try:
		data = get_web_page(url)
		soup = makeSoup(data)
		# print the title
		if soup != -1:
			print(current_depth *"|\t" + getTitle(soup))
			print(current_depth *"|\t" + "* " + url)
			current_depth += 1
			# if less than max depth, get next batch of URLs
			if current_depth < max_depth:
				url_list = getURLs(start_url, soup, domain)
				#current_depth += 1
				for url in url_list:
					get_tree(max_depth, current_depth, url, start_url, domain)
	except UnicodeEncodeError:
		pass

if __name__ == "__main__":
	domain = "nasa.gov"
	start_url = "http://www.nasa.gov"
	depth = 3
	get_tree(depth, 0, start_url, start_url, domain)

