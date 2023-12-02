# 自動予約
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time
from line import send_line_notify
from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select
from dotenv import load_dotenv
import os
import schedule
from for_moodhub import moodhub

load_dotenv()

def run():
    options = Options()
    options.headless = True  # ヘッドレスモード True=非表示, False=表示
    driver = webdriver.Chrome(options=options)

    # メールアドレスとパスワードの指定
    USERNAME = os.getenv("USERNAME")
    PASS = os.getenv("PASS")

    # ブラウザを起動
    driver.get(
        "https://sso.ritsumei.ac.jp/siteminderagent/forms/login.fcc?SMQUERYDATA=-SM-ggOZBHQthWXvF%2fdsaXkETfrsYH5KjtctGsFHSGU6fZZaFsaM7ohaNPYzLO60ZVw3n37DTrKSTZlTVh%2b2%2bVLjiTakjJR4E8mRLliTcTKLOyMshMnVjH4DGhC41piha%2b0zTtyn44IgYdNFoB%2fckwBcG57oIgd0tK%2bhahFd3fjcOC7jVZGHdvAPwAxMhd63UB%2fP5Sf3ifb0VoHah8wjW5lFHXeE4LFv5LU30Vp69FpWXD0Gz330inCGiBaLiFGJjIuh%2bX65Fr7%2fud%2fUHKCFNEOY9NJFxDsG57euGeWU2P2K5%2fLGjX1dbvdI1jPfnElE3cFPDAjlpua9iCUC293%2bhFZ%2fCSrzm0TDOPFXrFBsOsB5FceE3Aa8fUiAxGGBfKd3RCGUDLW%2buuCA26R5LERwbfYTvmK8gB2olS%2fs"
    )
    time.sleep(2)  # 2秒待機

    # ログイン情報を入力する
    search_name = driver.find_element_by_name("USER")
    search_pass = driver.find_element_by_name("PASSWORD")
    search_btn = driver.find_element_by_id("Submit")
    search_name.send_keys(USERNAME)
    search_pass.send_keys(PASS)
    search_btn.click()
    time.sleep(2)  # 2秒待機

    #指定日inputに入力
    search_date = driver.find_element_by_name("input_date")
    search_btn = driver.find_element_by_class_name("btn-primary")
    #今日+7日後の日付を取得
    #毎週木曜に実行すると仮定
    today = datetime.today()
    after_7days = today + timedelta(days=5)
    #after_7daysの日付を指定日inputに入力
    search_date.send_keys(after_7days.strftime("%Y/%m/%d")) 
    search_btn.click()
    time.sleep(2)  # 2秒待機

    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[0])
    time.sleep(2)  # 2秒待機
    #画面が変わったかを確認するために現在のsoupを取得
    old_soup = BeautifulSoup(driver.page_source, "html.parser")

    #予約ボタンをxpathで指定
    search_btn_x = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div/div/form/div[3]/div[5]/table/tbody/tr[30]/td[6]"
    )
    search_btn_x.click()
    time.sleep(2)  # 2秒待機
    #画面が変わったかを確認するために現在のsoupを取得
    new_soup = BeautifulSoup(driver.page_source, "html.parser")
    #もしsoupが変わっていたら画面が切り替わっている
    #切り替わっていたら自動予約を行う
    if old_soup != new_soup:
        #selectタグを指定
        dropdown = driver.find_element_by_name('time_st')
        dropdown1 = driver.find_element_by_name('time_ed')
        select = Select(dropdown)
        select1 = Select(dropdown1)
        # dropdown.click()
        select.select_by_value('10:40')
        # dropdown1.click()
        select1.select_by_value('12:10')

        #理由を入力
        purpose = driver.find_element_by_name("purpose")
        purpose.send_keys("プロジェクト会議")
        #次へボタンをクリック
        search_btn = driver.find_element_by_class_name("btn-primary")
        search_btn.click()
        time.sleep(2)
        #確定ボタンをクリック
        search_btn_last = driver.find_element_by_name("btn_submit")
        search_btn_last.click()
        time.sleep(5)

        #moodhubの関数を実行
        return moodhub()
    else:
        send_line_notify("そこはすでに埋まっているようです")

schedule.every().saturday.at("15:00").do(moodhub)

while True:
    schedule.run_pending()
    time.sleep(1)