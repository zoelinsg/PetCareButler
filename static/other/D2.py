#公立收容所資料
import requests
import pandas as pd
import re
import html
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

url = "https://data.moa.gov.tw/Service/OpenData/TransService.aspx?UnitId=2thVboChxuKs"

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

df = pd.DataFrame(data)[["ShelterName", "CityName", "Address", "Phone", "OpenTime"]].copy()

# 共用清理：去掉 \r\n
for col in ["ShelterName", "CityName", "Address", "Phone"]:
    df[col] = df[col].astype(str).str.replace(r"[\r\n]+", " ", regex=True).str.strip()

# OpenTime 專用清理：處理 <br/>
df["OpenTime"] = (
    df["OpenTime"].fillna("").astype(str)
    .map(html.unescape)  # 若有 &nbsp; 這類轉回正常字
    .str.replace(r"<br\s*/?>", "\n", regex=True)  # <br>, <br/>, <br />
    .str.replace(r"</?[^>]+>", "", regex=True)    # 其他殘留 HTML tag（保險）
    .str.replace(r"[\r\n]+", "\n", regex=True)    # 整理換行
    .str.strip()
)

df = df.rename(columns={
    "CityName": "城市名稱",
    "ShelterName": "收容所名稱",
    "Address": "地址",
    "Phone": "電話號碼",
    "OpenTime": "開放時間"
})

print(df.to_string(index=False))
