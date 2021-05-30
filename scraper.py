from bs4 import BeautifulSoup
import requests
import pprint

#building function that will return array data dictionary given a page number
def data_scraper(page,basic_url):
	data_store =[]
	if (page!=1):
		basic_url = basic_url + '?p=' + str(page)

	req = requests.get(basic_url)
	soup = BeautifulSoup(req.text,"html.parser")
	temp = soup.find_all("a",{'class':'storylink'})
	temp2 = soup.find_all("td",{'class':'subtext'})

	for i in temp:
		temp_dict = {
		'title': i.text,
		'link' : i['href']
		}
		data_store.append(temp_dict)
		temp_dict ={}

	x = 0;
	for i in temp2:
		temp3 = i.find("span",{'class':'score'})
		temp4 = i.find("span",{'class':'age'})

		data_store[x]['time'] = temp4.a.text
		if (temp3!=None):
			data_store[x]['points'] = temp3.text
		else:
			data_store[x]['points'] = '0 points'
		x = x + 1

	#pprint.pprint(data_store)

	return data_store

		
def get_data(page_no):
	basic_url = 'https://news.ycombinator.com/news'
	raw_data = data_scraper(page_no,basic_url)

	#removing less viewed pages
	for i in raw_data:
		temp_str = i['points']
		count = 0;

		for j in temp_str:
			if(j==' '):
				break;
			count = count + 1;

		if(count<3):
			raw_data.remove(i);
	
	return raw_data

get_data(1)