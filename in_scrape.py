# coding: UTF-8
import requests
from bs4 import BeautifulSoup

## アクセスするURL
#url = "http://in-note.com/"
#
## URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
#html = requests.get(url)
#
## htmlをBeautifulSoupで扱う
#soup = BeautifulSoup(html.text, "html.parser")
#
## タイトルを文字列を出力
#print(soup.title.string)
#
#s = requests.Session()
#r = s.post('http://in-note.com/', data = {
#           'query': 'foo',
#           'exclude': 'bar',
#           'target': ['1', '2'],
#           })
#soup = BeautifulSoup(r.text, 'html.parser')
#itemTags = soup.select('.item-caption a')
#for itemTag in itemTags:
#    r = s.get(itemTag['href'])
#    soup = BeautifulSoup(r.text, 'html.parser')
#    itemDetailTag = soup.select_one('.item-detail')
#    print('{}: {}'.format(itemTag.text.strip(), itemDetailTag.text.strip()))


import time
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
# Chromeのパス（Stableチャネルで--headlessが使えるようになったら不要なはず）
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
# ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
options.add_argument('--headless')
# ChromeのWebDriverオブジェクトを作成する。
driver = webdriver.Chrome(chrome_options=options)

# Googleのトップ画面を開く。
driver.get('http://in-note.com/')

# タイトルに'Google'が含まれていることを確認する。
assert '韻' in driver.title

##コマンドラインから取得
#arg = unicode(sys.argv, 'cp932')

# 検索語を入力して送信する。
input_element = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/input')
input_element.send_keys('おはよう')
input_element.send_keys(Keys.RETURN)

time.sleep(2)  # Chromeの場合はAjaxで遷移するので、とりあえず適当に2秒待つ。

# タイトルに'Python'が含まれていることを確認する。
#assert 'Python' in driver.title

# スクリーンショットを撮る。
driver.save_screenshot('search_results.png')

#隠れている検索結果を表示する。
#assertEquals(
#             0,
#             driver.find_elements_by_xpath('/html/body/div[8]/ul/button'))

hidden_button = driver.find_elements_by_class_name('show-more')
if hidden_button != []:
    driver.find_element_by_class_name('show-more').send_keys(Keys.RETURN)

# 検索結果を表示する。/html/body/div[8]/ul/li[2]/a/div[1]/div[2]/span[1]
#body > div.main > div.ajax > ul > li:nth-child(1) > a > div.normal-area > div.word.element > span.word-main
#body > div.main > ul > li:nth-child(4) > a > div.normal-area > div.word.element > span.word-main
#for a in driver.find_elements_by_xpath('/html/body/div[8]/ul'):
#    print(a.text)
#    print(a.get_attribute('href'))
      
#for a in range(len(driver.find_elements_by_xpath('/html/body/div[8]/ul'))):
#    for b in driver.find_elements_by_xpath('/html/body/div[8]/ul/li[a]/a/div[1]/div[2]/span[1]'):
#        print(b.text)

for a in driver.find_elements_by_class_name("word-main"):
    print(a.text)


driver.quit()  # ブラウザーを終了する。
