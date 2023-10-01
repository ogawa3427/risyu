import json
import os
import re

filename = 'setting.json'

#with open(filename, 'r', encoding='utf-8') as f:
#	data = json.load(f)

initdata = {
'filedir': '',
'newparson': True,
'iki': '',
'rui': '',
'kamoku_kyo': {
		'グローバル時代の': 'ｸﾞﾛｰﾊﾞﾙ時代の',
		'エクササイズ&スポーツ': 'E&S',
		'インテグレーテッド': 'インテグ',
		'論理学から': '',
		'異文化間コミュニケーション': '異コミュ',
		'グローバル': 'ｸﾞﾛｰﾊﾞﾙ',
		'ケーススタディ': 'ｹｰｽｽﾀﾃﾞｨ',
		'PHILLIPPSJEREMYDAVID': 'PHILLIPPS',
		'GRUENEBERGPATRICK': 'GRUENEBERG',
		'アプローチ': 'ｱﾌﾟﾛｰﾁ'
		},
'kamoku_jaku': {
		'グローバル時代の国際協力':'グロ国'
		}
	}
			
with open(filename, 'w', encoding='utf-8') as f:
	json.dump(initdata, f, indent=4)
			