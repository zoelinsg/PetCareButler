# Pet Care

- 以 Django Template 為主的寵物照護管理專案，包含寵物資料、日常紀錄、開支紀錄、相片管理，以及資料爬取與搜尋等功能。
---

## 專案呈現
- **[說明簡報](https://docs.google.com/presentation/d/1hmswIjc709DnCZP5JWac4fqHxKPdR7MuYtJBKAgw95Y/edit?usp=drive_link)**
- **[Demo影片](https://www.youtube.com/watch?v=R1xDsy_aJu8)**
---

## 專案環境與工具

- Python：建議 3.12+
- 套件管理：Poetry
- Web Framework：Django
- 其他套件：pillow、requests

---

## 環境部署

- 安裝 Poetry
```bash
pip install poetry
```

- 初始化專案並建立虛擬環境
```bash
poetry init
poetry install
poetry shell
```

- 安裝 Django 與常用套件
```bash
poetry add django
poetry add pillow requests
```

- 建立 Django 專案
```bash
django-admin startproject core .
```

- 建立 Apps
```bash
python manage.py startapp users
python manage.py startapp datahub
python manage.py startapp photos
python manage.py startapp pets
python manage.py startapp records
python manage.py startapp expenses
python manage.py startapp planner
python manage.py startapp dashboard
```

- 建立超級使用者
```bash
python manage.py createsuperuser
```

- 建立遷移檔案
```bash
python manage.py makemigrations
```

- 執行資料庫遷移
```bash
python manage.py migrate
```

- 啟動開發伺服器
```bash
python manage.py runserver
```

---

## 專案功能
- 使用者註冊
- 使用者登入
- 使用者登出
- 查看主人資料
- 修改主人資料
- 忘記密碼
- 忘記密碼郵件
- 密碼重置

- 爬取動物認領養資料
- 爬取動物遺失啟示資料
- 爬取公立收容所資料
- 爬取動保單位資料

- 關鍵字搜尋動物認領養資料
- 關鍵字搜尋動物遺失啟示資料
- 關鍵字搜尋公立收容所資料
- 關鍵字搜尋動保單位資料

- 相片列表查看
- 相片詳情查看
- 相片新增
- 相片刪除
- 相片修改

- 寵物資料新增
- 寵物資料刪除
- 寵物資料修改
- 寵物資料查看
- 寵物列表查看

- 日常生活記錄新增
- 日常生活記錄刪除
- 日常生活記錄修改
- 日常生活紀錄列表查看
- 日常生活紀錄詳情查看

- 日常開支記錄新增
- 日常開支記錄刪除
- 日常開支記錄修改
- 日常開支紀錄列表查看
- 日常開支紀錄詳情查看

- 行事曆月曆檢視
- 行事曆日檢視
- 行程新增
- 行程詳情
- 行程編輯
- 行程刪除
- 提醒列表
- 提醒全部標記已讀

- 儀表板顯示今日提醒
- 儀表板顯示今日行程
- 儀表板顯示本月開支