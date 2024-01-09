from flask import Flask , jsonify
import requests
from flask_cors import CORS
from bs4 import BeautifulSoup
from datetime import datetime
from flask import request

def do():
    url = "https://sso.ritsumei.ac.jp/siteminderagent/forms/login.fcc?SMQUERYDATA=-SM-jrg%2bnK3h0J1Yzrd%2bfDE0ypw39nJbw7daP3wjlUTdxppSIdDwq%2b9Ul2sdLmXPg7KaPVjwMf0G8Q6l25zlG6FDc5WGyJ2yFW%2bC3r2Y51rib9vHIxOtNgvv25TImGA6H4w691lFV9rrzgA%2fezQBHF65WQ%2fx6abJn0DqJFj41n4qLJ78CvXE4FO2rqXDwb2t6nedAhjCzszMcyK6ICRNifUk%2fgTWCSed6GQOO27lwz2TNpX4drZWcpaJIlQhYRk%2f9MAnjj72clgHQ0hTwTKVTL%2b%2bMK5QlBtvrkZTUmIEePX8EDf5dGotCKRgTjaEdEsTjDcD5P%2f7h%2fK5u0GDjGbsMKKY%2buN7kcL85MxcE5pSuHjicuYs9PQBzj8IwIw2EXRyw%2bnPvLegkO%2btKNop4NgIfRaFIV3gyz9QGy4v"

    payload = {
        "csrfmiddlewaretoken":"dc4423eff7f8435727001943bdcb88b8",
        "lang":"0",
        "loginMode":"login",
        "EPPN":"is0660hp",
        "rurl":"%2Fopac%2Frsv%2F",
        "lang":"0",
        "ssosw":"1",
        "u_mode":"0"
    }
    try:
        # POSTリクエストを送信
        res = requests.post(url, data=payload)
        # BeautifulSoupを使用してHTMLを解析
        soup = BeautifulSoup(res.text, "html.parser")
        print(soup)
    except Exception as e:
        print(e)
        print("エラーが発生しました。")

if __name__ == "__main__":
    do()