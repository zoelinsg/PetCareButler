# 遺失啟示資料
import requests
import pandas as pd
import re
import html
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

url = "https://data.moa.gov.tw/Service/OpenData/TransService.aspx?UnitId=IFJomqVzyB0i"

session = requests.Session()

retry = Retry(
    total=5,                 # 最多重試 5 次
    connect=5,
    read=5,
    backoff_factor=1.0,      # 1,2,4,8... 秒退避
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
    raise_on_status=False,
)

adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)
session.mount("http://", adapter)

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; DataFetcher/1.0)"
}

# timeout 建議拆成 (connect_timeout, read_timeout)
resp = session.get(url, headers=headers, timeout=(30, 60))
resp.raise_for_status()

data = resp.json()

df = pd.DataFrame(data)[["晶片號碼", "寵物名", "寵物別", "性別", "特徵", "遺失時間", "遺失地點", "飼主姓名", "連絡電話", "PICTURE"]].copy()

# 共用清理：去掉 \r\n
for col in ["晶片號碼", "寵物名", "寵物別", "性別", "特徵", "遺失時間", "遺失地點", "飼主姓名", "連絡電話", "PICTURE"]:
    df[col] = df[col].astype(str).str.replace(r"[\r\n]+", " ", regex=True).str.strip()

df = df.rename(columns={
    "晶片號碼": "晶片號碼",
    "寵物名": "寵物名",
    "寵物別": "寵物別",
    "性別": "性別",
    "特徵": "特徵",
    "遺失時間": "遺失時間",
    "遺失地點": "遺失地點",
    "飼主姓名": "飼主姓名",
    "連絡電話": "連絡電話",
    "PICTURE": "圖片"
})

print(df.to_string(index=False))