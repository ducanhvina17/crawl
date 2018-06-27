from bs4 import BeautifulSoup
import urllib.request
import re
import csv
import requests
def  not_relative_uri(href):
	return re.compile('\/*[\w]\/').search(href) is  not  None
def crawl_post_dtri(url):
	page = requests.get('http://dantri.com.vn'+url).content
	soup = BeautifulSoup(page, 'html.parser')
	noidung=soup.find(id='ctl00_IDContent_Tin_Chi_Tiet')
	if(noidung==None):
		return
	title=noidung.find(class_='fon31 mgb15').get_text().lstrip().rstrip()
	print(title)
	content=noidung.find(id='divNewsContent')
	content_p=content.find_all('p')
	output=''
	output+=title+"\n\n"
	for p in content_p:
		output+=(p.get_text().strip('\n'))+" "
	with open('update_data\\Dtr_'+(str)(re.compile('(?<=-)\w+(?=.htm)').search(url).group(0))+'.txt','w', encoding='utf-8') as doc:
		doc.write(output)

def crawl_post_zing(url):
	page = requests.get('http://news.zing.vn'+url).content
	soup = BeautifulSoup(page, 'html.parser')
	noidung=soup.find('section',class_='main')
	if(noidung==None):
		return
	title=noidung.find(class_='the-article-title').get_text().lstrip().rstrip()
	content=noidung.find(class_='the-article-body')
	content_p=content.get_text().replace('\n',' ')
	content_p=' '.join(content_p.split())
	output=''
	output+=title+"\n\n"+content_p
	with open('update_data\\Zing_'+(str)(re.compile('(?<=-)\w+(?=.htm)').search(url).group(0))+'.txt','w', encoding='utf-8') as doc:
		doc.write(output)
def crawl_post_vnn(url):
	page = requests.get('http://vietnamnet.vn/'+url).content
	soup = BeautifulSoup(page, 'html.parser')
	title=soup.find("title").get_text().lstrip().rstrip()
	noidung=soup.find(class_='HomeBlockLeft')
	content_text=''
	if(noidung==None):
		return
	content=noidung.find(id='ArticleContent')
	if(content==None):
		content=soup.find(class_="content-wrapper")
		if(content==None):
			return
		content_p=content.find_all('p')
		for p in content_p:
			content_text+=(p.get_text().lstrip().rstrip())+" "
	else:
		content_p=content.find_all('p',recursive=False)

		for ab in content_p:
			if('class' in ab.attrs):
				if('inner-article' not in ab.attrs['class']):
					content_text+=ab.get_text().lstrip().rstrip()
			else:
				content_text+=ab.get_text().lstrip().rstrip()+" "
	output=''
	output+=title+"\n\n"+content_text.replace('\n',' ')
	with open('update_data\\Vnn_'+(str)(re.compile('(?<=-)\w+(?=.htm)').search(url).group(0))+'.txt','w', encoding='utf-8') as doc:
		doc.write(output)
def get_post_dtri():
	page=urllib.request.urlopen('http://dantri.com.vn/')
	soup = BeautifulSoup(page, 'html.parser')
	new_feeds=soup.find(class_='box27').find_all('a', href=not_relative_uri )
	for feed in new_feeds:
		title = feed.get('title')
		link = feed.get('href')
		print('Title: {} \nLink: {}'.format(title, link))
		crawl_post_dtri(link)
def get_post_zing():
	page=requests.get('http://news.zing.vn/')
	soup = BeautifulSoup(page.content, 'html.parser')
	new_feeds=soup.find('section',id="homepage").find('div',class_='content-wrap').find_all('p',class_='title')
	for feed in new_feeds:
		feed=feed.find('a')
		link = feed.get('href')
		title=feed.get_text().lstrip().rstrip()
		print('Title: {} \nLink: {}'.format(title,link))
		crawl_post_zing(link)
def get_post_vnn():
	page=requests.get('http://vietnamnet.vn/')
	soup = BeautifulSoup(page.content, 'html.parser')
	new_feeds=soup.find('div',class_='HomeTop').find_all(re.compile('^h[1-6]$'))
	for feed in new_feeds:
		feed=feed.find('a')
		link = feed.get('href')
		title=feed.get_text()
		print('Title: {}\nLink: {}'.format(title,link))
		crawl_post_vnn(link)

if __name__ == '__main__':
	get_post_dtri()
	get_post_zing()
	get_post_vnn()
