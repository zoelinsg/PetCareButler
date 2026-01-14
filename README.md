# PetCareButler
Multi-pet care tracker with Gemini.

# Pet Care

環境部署
# 安裝 poetry
pip install poetry

# 初始化專案並建立環境
poetry config virtualenvs.in-project true
poetry init
poetry shell
poetry env use python

# 安裝 Django
poetry add django

# 安裝套件
poetry add pillow requests

# 創建 Django 專案
django-admin startproject core .

# 創建 App
python manage.py startapp users
python manage.py startapp datahub

# 建立超級使用者
python manage.py createsuperuser

# 生成遷移檔案
python manage.py makemigrations

# 執行資料庫遷移
python manage.py migrate

# 啟動開發伺服器
python manage.py runserver

# 靜態資料存放 static 資料夾

# Django templates html 

# 專案功能
使用者註冊
使用者登入
使用者登出
查看主人資料
修改主人資料
忘記密碼
忘記密碼郵件
密碼重置

爬取動物認領養資料
爬取動物遺失啟示資料
爬取公立收容所資料
爬取動保單位資料

關鍵字搜尋動物認領養資料
關鍵字搜尋動物遺失啟示資料
關鍵字搜尋公立收容所資料
關鍵字搜尋動保單位資料