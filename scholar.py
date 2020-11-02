import requests
from bs4 import BeautifulSoup
import io
import sys
import urllib.request
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
def find_shaolar(key_words,schools,index_lb):
	print("start")
	df = pd.DataFrame(columns = ["name", "h-index"])
	for school_url in schools:
		flag = 0
		Flag_while = True
		while(Flag_while):
			#school url
			if(flag == 0):
				content = requests.get(school_url).text
				page = BeautifulSoup(content, 'html5lib')
			if(flag != 0):
				content = requests.get(url).text
				page = BeautifulSoup(content, 'html5lib')

			#update the url of next page 
			next_page = page.find('div', {'class': 'gsc_pgn'})
			next_page_button = str(next_page.find('button',{'aria-label':'Next'}))
			m = next_page_button[next_page_button.rfind("after_author"):]
			url = school_url + "&after_author=" + m[16:28] + "&astart=10"
			flag = 1
			print(url)

			#each scholar
			for entry in page.find_all("div", attrs={"class": "gs_ai_t"}):
				index_amount = entry.find("div",attrs={"class":"gs_ai_cby"})
				if (int(index_amount.text.split()[2]) < index_lb):
					Flag_while = False
					break
				p_url = "https://scholar.google.com.tw" + entry.a['href']
				p_content = requests.get(p_url)
				p_content.encoding = 'utf-8'
				p_page = BeautifulSoup(p_content.text, 'html5lib')

				#h-index
				for tr in p_page.find_all('div', {'class': 'gsc_rsb_s gsc_prf_pnl'}):
					p_table = tr.tbody.children
					i = 0
					for a in p_table:
						i = i + 1
						if a.find("td"):
							if (i == 2):
								j = 0
								for value in a.children:
									j = j + 1
									if(j == 2):

										#matching key words
										if (int(value.text) >= 15):
											Research = []
											Research_real = []
											research = p_page.find('div', {'class': 'gsc_prf_il','id':'gsc_prf_int'})
											for item in research.find_all("a",{'class':'gsc_prf_inta gs_ibl'}):
												Research_real.append(item.text)
												tmp = item.text.split()
												Research = Research + tmp
											Research_lw = [s.lower() for s in Research]
											for word in key_words:
												if word in Research_lw:
													new = pd.DataFrame({"name":entry.h3.a.text,"h-index":value.text,"research":str(Research_real)},index=[1])
													df = df.append(new,ignore_index=True)
													break
					break
	df.to_excel('data1.xls',sheet_name='data')

	
if __name__ == '__main__':
	#search key words
	key_words = ["urban","traffic","tranportation","transport","civil engineering"]
	#school url
	schools = list(pd.read_excel('school.xlsx', header = None)[0])
	#lower_bound of index amount
	index_lb = 1000
	#search_function
	find_shaolar(key_words,schools,index_lb)