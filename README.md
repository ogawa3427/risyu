API部分は別のリポジトリに切り出して新しくしたくなってきた
-> https://github.com/ogawa3427/risyu-api

https://github.com/ogawa3427/risyu-api/blob/main/docs/memos/2026-04-09-client-reference-prompt.md
これとかみてね  
/api-viewer.htmlとか  
/api-stale-then-fresh-demo.html とかもいいね  


なんか全部めんどくさくなったんで作り直しました (・ω<)

[kurisyushien.org](https://kurisyushien.org)

## CI/CD (S3 デプロイ)
GitHub Actionsで `index.html` と `static/favicon.ico` をS3へアップロードします。  
ワークフロー: `.github/workflows/deploy-s3.yml`

必要な GitHub Secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `S3_BUCKET`

だからと言って以下の内容が意味なくなるわけじゃないからな - そして引き続きNO　WARRANTIY
---


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

