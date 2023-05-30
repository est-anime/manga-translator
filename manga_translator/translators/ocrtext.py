

import hashlib
import urllib.parse
import random
import sqlite3

from .common import CommonTranslator, InvalidServerResponse, MissingAPIKeyException


class OCRTextTranslator(CommonTranslator):
	_LANGUAGE_CODE_MAP = {
		'CHS': 'zh',
		'CHT': 'cht',
		'JPN': 'ja',
		'ENG': 'en',
		'KOR': 'kor',
		'VIN': 'vie',
		'CSY': 'cs',
		'NLD': 'nl',
		'FRA': 'fra',
		'DEU': 'de',
		'HUN': 'hu',
		'ITA': 'it',
		'PLK': 'pl',
		'PTB': 'pt',
		'ROM': 'rom',
		'RUS': 'ru',
		'ESP': 'spa',
	}

	def __init__(self) -> None:
		super().__init__()

	async def _translate(self, from_lang, to_lang, queries):
		# Create a connection and open the database
		conn = sqlite3.connect('manga_page.db')

		# Create a cursor object
		cursor = conn.cursor()
		# Read the page field value of the first piece of data in the page_count table
		cursor.execute('SELECT page FROM page_count LIMIT 1')
		result = cursor.fetchone()
		page = result[0]
		
		atext = ""
		atext = "@Page "+str(page)+"，"+str(len(queries))+" sentences in total.\r\n" # Test to add special symbols
		# atext = "第"+str(page)+"页，共"+str(len(queries))+"句。\r\n\r\n" # Test to add special symbols

		result_list = [] # by number

		for i, text in enumerate(queries):
			# Replace the wrong words in the text
			for key, value in dict_kv.items():
				text = text.replace(key, value)
			atext += f"{i + 1}.{text}\r\n"
			# result_list.append(str(i+1)) # tagging order
		atext = atext + "@Page "+str(page)+" End"

		# 过滤[]
		atext = atext.replace("[", "")
		atext = atext.replace("]", "")

		print("当前文本概览：")
		print(atext)
		print("导入数据库")
		


		
		# Update page field value
		new_page = page + 1
		cursor.execute('UPDATE page_count SET page=? WHERE rowid=1', (new_page,))


		# create form
		#cursor.execute('''CREATE TABLE manga_page(id INTEGER PRIMARY KEY AUTOINCREMENT, words TEXT, trans TEXT)''')

		# insert data
		#data = 'Hello, World!'
		cursor.execute("INSERT INTO manga_page (words) VALUES (?)", (atext,))

		# commit changes
		conn.commit()

		# close connection
		conn.close()
		return result_list
