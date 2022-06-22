import requests
import jsonpath
import os
"""
	1.url
	2.模拟浏览器请求
	3.解析网页源代码
	4.保存数据
"""

def get_Search_Music_name(name, page):
	"""
	搜索歌曲名称
	:return:
	"""
	# print("-------------------------------------------------------")
	src_url = 'https://music.liuzhijin.cn/'
	headers = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
		# 判断请求是异步还是同步
		"x-requested-with": "XMLHttpRequest",
	}
	platfroms = ["netease"
				# ,"qq"
				# ,"kugou"
				# ,"kuwo"
				# ,"ximalaya"
				]
	songList = []
	for platfrom in platfroms:
		# print(platfrom.center(50,"="))
		for i in range(page):
			param = {
				"input": name,
				"filter": "name",
				"type": platfrom,
				"page": i,
			}
			res = requests.post(url=src_url, data=param, headers=headers)
			json_text = res.json()

			title = jsonpath.jsonpath(json_text, '$..title')
			author = jsonpath.jsonpath(json_text, '$..author')
			url = jsonpath.jsonpath(json_text, '$..url')
			if title:
				songs = list(zip(title, author, url))
				songList = songList + songs
	return songList

def song_download(index, songList):
	url = songList[index][2]
	title = songList[index][0]
	author = songList[index][1]
	# 创建文件夹
	os.makedirs("download", exist_ok=True)
	song_name = author + " - " + title + '.mp3'
	print('歌曲:{0},正在下载...'.format(song_name))
	# 下载（这种读写文件的下载方式适合少量文件的下载）
	content = requests.get(url).content
	with open(file='./data/' + song_name, mode='wb') as f:
		f.write(content)
	print('下载完毕,{0},请试听'.format(song_name))
	return './data/' + song_name

