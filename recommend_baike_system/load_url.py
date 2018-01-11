import sys
import urllib.request
import time
import random
import bs4

# 返回url内容
def load2(url):
	if url is None:
		return None
	# print(url)
	try:
		response = urllib.request.urlopen(url,timeout=60)
	except urllib.request.URLError as e:
		print(e)
	if response.getcode == 200:
		return None
	# print("load数据")
	return response.read()

def load(url):
	if url == None:
		return None
	try:
		response = urllib.request.urlopen(url, timeout=60)
		if response.getcode==200:
			return None
		return response.read()
	except Exception as e:
		with open('log','a', encoding='utf-8') as f:
			f.write('错误url : '+url+'>----->'+str(e)+'\n')
		return None


# 写html
def write_html(star_name, html, path):
	if html is not None:
		if star_name == "":
			p = path + str("null")
		else:
			p = path+star_name
		# print(p)
		with open(p,'w',encoding="utf-8") as f:
			f.write(html.decode("utf-8"))
		# print(star_name)

# data = load('https://baike.baidu.com/item/Lonely/13213795')
# print(data)
# write_html('test', data)


