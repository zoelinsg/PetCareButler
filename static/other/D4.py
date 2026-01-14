# 動物認領養資料
import requests
import pandas as pd
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

url = "https://data.moa.gov.tw/Service/OpenData/TransService.aspx?UnitId=QcbUEzN6E6DL"

session = requests.Session()
retry = Retry(
    total=5,
    connect=5,
    read=5,
    backoff_factor=1.0,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
    raise_on_status=False,
)
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)
session.mount("http://", adapter)

headers = {"User-Agent": "Mozilla/5.0 (compatible; DataFetcher/1.0)"}

resp = session.get(url, headers=headers, timeout=(30, 60))
resp.raise_for_status()
resp.encoding = "utf-8"
data = resp.json()

df = pd.DataFrame(data)

# 1) 只要 OPEN
df = df[df["animal_status"].astype(str).str.upper().eq("OPEN")].copy()

# 2) 你要的欄位（順便把 animal_status 留著以免之後要查）
cols = [
    "animal_kind", "animal_sex", "animal_bodytype", "animal_colour",
    "animal_age", "animal_sterilization", "animal_bacterin",
    "shelter_name", "shelter_tel", "animal_status"
]
df = df[cols].copy()

# 3) 基本清理（去掉換行、前後空白）
for col in cols:
    df[col] = df[col].fillna("").astype(str).str.replace(r"[\r\n]+", " ", regex=True).str.strip()

# 4) 代碼轉中文（建議：新增顯示欄位，而不是覆蓋原欄位）
sex_map = {"M": "公", "F": "母", "N": "未知"}
body_map = {"SMALL": "小型", "MEDIUM": "中型", "BIG": "大型"}
age_map = {"CHILD": "幼年", "ADULT": "成年"}
tf_unknown_map = {"T": "是", "F": "否", "N": "未知", "": "未知"}

# 結紮 / 疫苗（你的資料常見 T/F/N）
df["是否結紮"] = df["animal_sterilization"].str.upper().map(tf_unknown_map).fillna("未知")
df["疫苗接種"] = df["animal_bacterin"].str.upper().map(tf_unknown_map).fillna("未知")

# 年齡、體型、性別
df["年齡"] = df["animal_age"].str.upper().map(age_map).fillna("未知")
df["體型"] = df["animal_bodytype"].str.upper().map(body_map).fillna("未知")
df["性別"] = df["animal_sex"].str.upper().map(sex_map).fillna("未知")

# 5) 最終輸出：挑顯示用欄位
out = df[[
    "animal_kind", "性別", "體型", "animal_colour", "年齡",
    "是否結紮", "疫苗接種", "shelter_name", "shelter_tel"
]].rename(columns={
    "animal_kind": "種類",           
    "animal_colour": "毛色",
    "shelter_name": "收容中心名稱",
    "shelter_tel": "收容中心電話",
})

print(out.to_string(index=False))
