# 参考URL  
## 公式  
https://scrapy.org/
## Python製クローラー「Scrapy」の始め方メモ  
取っかかりに良い。  「クローラーのひな型の指定」について説明してくれている。  
http://sechiro.hatenablog.com/entry/2016/04/02/Python%E8%A3%BD%E3%82%AF%E3%83%AD%E3%83%BC%E3%83%A9%E3%83%BC%E3%80%8CScrapy%E3%80%8D%E3%81%AE%E5%A7%8B%E3%82%81%E6%96%B9%E3%83%A1%E3%83%A2
## Python, Scrapyの使い方（Webクローリング、スクレイピング）  
詳しい。「クローリングとスクレイピングの違い」から説明してくれている。  
https://note.nkmk.me/python-scrapy-tutorial/
## 「人とWebに優しい」Scrapyの使い方サンプル〜 #PyConJP 2017のつづき(なお野球)
「Webに優しい」設定を学ばせていただいた。  
http://shinyorke.hatenablog.com/entry/scrapy-example-yakiu
  
# Scrapyのインストール  
`$ pip install scrapy`  
  
service_identityも、一緒に入れておくのが推奨とのこと。MITM攻撃を防ぐためのパッケージ。  
`$ pip install service_identity`  
  
# まずやってみること  
Scrapy開発元であるScrapinghub社のBLOGより、記事タイトルの一覧を抜き出して（= スクレイピングして）みる。  
  
https://blog.scrapinghub.com/
  
# プロジェクト作成  
`$ scrapy startproject myproject`  
  
# setting.pyの修正  
Scrapyのデフォルト設定が、あんまりクロール先に優しくないので、いろいろ変更する。  
`$ cd myproject/`  
`$ cd myproject/`  
`$ vi settings.py`  
  
`CONCURRENT_REQUESTS = 2  # リクエスト並行数,16もいらないので2`  
`DOWNLOAD_DELAY = 1 # ページのダウンロード間隔として平均1秒空ける。`  
`CONCURRENT_REQUESTS_PER_DOMAIN = 2  # 同一ドメインに対する並行リクエスト数. CONCURRENT_REQUESTSと同じ値でOK(サンプルは単一ドメインしか相手していない)`  
`CONCURRENT_REQUESTS_PER_IP = 0  # 同一IPに対する並行リクエスト数. ドメインで絞るので無効化してOK`  
`HTTPCACHE_ENABLED = True  # キャッシュの有無,勿論True`  
`HTTPCACHE_EXPIRATION_SECS = 60 * 60 * 24  # キャッシュのExpire期間. 24時間(秒数で指定)`  
`HTTPCACHE_DIR = 'httpcache'  # キャッシュの保存先(どこでも良い)`  
クロール先に迷惑をかけないようにしましょう。  
  
# Spiderのテンプレート作成  
`$ scrapy genspider blog_scrapinghub blog.scrapinghub.com`  
blog_scrapinghub.pyが、spiderディレクトリにできる。  
  
# Spiderの実装  
https://scrapy.org/
の "Build and run your web spiders" を参考に、parse処理を記述する。  
  
まずは、parseメソッドの最初の2行、記事タイトルの一覧を抜き出すところだけを書いて、実装してみましょう。  
  
参考：  
Responseオブジェクトの公式リファレンス  
https://doc.scrapy.org/en/latest/topics/request-response.html#response-objects  
selector.extract_first()メソッドの使い方  
https://doc.scrapy.org/en/latest/topics/selectors.html?highlight=extract_first#id1  
（日本語）（しかし翻訳は途中のよう）  
https://scrapy-ja.readthedocs.io/ja/latest/topics/request-response.html#response  
https://scrapy-ja.readthedocs.io/ja/latest/intro/tutorial.html?highlight=extract_first  

# Spiderの実行  
`$ scrapy runspider blog_scrapinghub.py`  
  
# 次にやってみること  
  
次に、過去記事のページをたどって（= クローリングして）、過去記事についても、タイトルを抜き出してみる。  
  
# Spiderの実装  
再び公式。  
https://scrapy.org/  
の "Build and run your web spiders" を参考に、parse処理を記述する。  
  
ただ、古い記事へのリンクをたどる記述が最新のページに対応してないようなので、14行目はこのように書き換える必要がある。  
`        for next_page in response.css('div.blog-pagination > a'):`  
それか、こうするか。  
`        for next_page in response.css('.next-posts-link'):`  
  
# Spiderの実行  
`$ scrapy runspider blog_scrapinghub.py`  
  
↓　以下はまだ書きかけです。すいません。  
  
# Spiderのテンプレート作成  
`$ scrapy genspider news_crawl news.yahoo.co.jp`  
spiderディレクトリにできる。  
  
# Spiderの実行  
`$ cd myproject`  
`$ scrapy crawl news_crawl -o news_crawl.jl`  
`$ cat news_crawl.jl | jq .`  
  
# Pipeline作成後の使用登録  
`vi settings.py`  
`ITEM_PIPELINES = {`  
...  
`}`  
（Pipelineのクラス名を変えていなければ、デフォルトのままで良いはず？）  
