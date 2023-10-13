
~~アカンサスポータル確認事項第6条の8に抵触する可能性が否定できない状況です~~  
事務さんからOK出ましたが
鯖の負荷には注意

KUSSOの先にあるデータを一般公開してるのってまずくね？みたいなことも思ってないわけではない

https://burnt-learning-ae0.notion.site/risyu-68085c98995a4446b9fbdb91e10142b0?pvs=4

自己責任においてクローン等するようにしてください

NO　WARRANTIY

# risyu
$HOMEに抽選科目登録状況のHTMLを投げ込んでrisyu(シェルスクリプト)を実行すると日時付きのCSVにします  
先方が仕様変更したら多分おかしくなります

dir.csvにフルパスを書いとくとそこからHTMLを探します  
私はDownloadにしてる

(Python GUI)
python3.11.5  
~~PySimpleGUI~~  
tknter  

(WEB)
python3.8
Flask
WSGI
Apache2


#ライセンス License
MITライセンスでよろしくお願いいたします
MIT License


NO　WARRANTIY



## ファイル構成 Files  
risyu  
　おまけ。CSV化の部分のBashスクリプト。メンテはしてない。  
risyu.py  
　本体。これを実行すると全部GUI上でできる。気が向いたらCLIオプションつけるかも。  
setting.json  
　初回起動時に作られる。個人設定が入る。下のと保存しとくと環境のBUになるはず。   
role.json  
　履修対象判定のための情報が入ってる。  
(タイムスタンプ)risyu.csv  
　完成品のＣＳＶです。煮るなり焼くなりって感じ。
app.py
	webサーバーの内蔵ちゃん
templates/
	内蔵ちゃんが読み出すHTML
	index.html
	aff.html
	set.html
	man.html
csvs/
	内蔵ちゃんが投げてくるデータ置き場、最新のタイムスタンプのやつがデフォで使われる

