# 動保單位資料
import requests
import pandas as pd

url = "https://data.moa.gov.tw/Service/OpenData/TransService.aspx?UnitId=FczRQaLNjcvP"

resp = requests.get(url, timeout=15)
resp.raise_for_status()          # 如果 HTTP 狀態碼不是 200 直接丟錯
resp.encoding = "utf-8"          # 保險起見，避免中文亂碼

data = resp.json()               # 這裡會得到一個 list[dict]

df = pd.DataFrame(data)

# 挑選欄位
df = df[["AnimalProtectName", "Address", "Phone", "Url"]].copy()

# 清掉欄位中可能出現的換行與多餘空白
for col in ["AnimalProtectName", "Address", "Phone", "Url"]:
    df[col] = df[col].astype(str).str.replace(r"[\r\n]+", "", regex=True).str.strip()

# 改成你要顯示的中文欄名
df = df.rename(columns={
    "AnimalProtectName": "動保單位名稱",
    "Address": "地址",
    "Phone": "電話號碼",
    "Url": "網址"
})

print(df.to_string(index=False))