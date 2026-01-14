from __future__ import annotations
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Any, Dict, List
import html
import requests

try:
    from django.core.cache import cache
except Exception:  
    cache = None


def _session() -> requests.Session:
    s = requests.Session()
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
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.headers.update({"User-Agent": "Mozilla/5.0 (PetCareButler/1.0)"})
    return s


def _get_json(url: str, *, cache_key: str, ttl_seconds: int = 3600) -> List[Dict[str, Any]]:
    if cache is not None:
        cached = cache.get(cache_key)
        if cached:
            return cached

    resp = _session().get(url, timeout=(15, 45))
    resp.raise_for_status()
    resp.encoding = "utf-8"
    data = resp.json()

    if cache is not None:
        cache.set(cache_key, data, ttl_seconds)

    return data


def _clean_str(v: Any) -> str:
    return str(v or "").replace("\r", " ").replace("\n", " ").strip()


# 動保單位資料
def fetch_animal_protect_units() -> List[Dict[str, str]]:
    url = "https://data.moa.gov.tw/Service/OpenData/TransService.aspx?UnitId=FczRQaLNjcvP"
    raw = _get_json(url, cache_key="moa:animal_protect_units", ttl_seconds=24 * 3600)

    out: List[Dict[str, str]] = []
    for item in raw:
        out.append({
            "動保單位名稱": _clean_str(item.get("AnimalProtectName")),
            "地址": _clean_str(item.get("Address")),
            "電話號碼": _clean_str(item.get("Phone")),
            "網址": _clean_str(item.get("Url")),
        })
    return out


# 公立收容所資料
def fetch_public_shelters() -> List[Dict[str, str]]:
    url = "https://data.moa.gov.tw/Service/OpenData/TransService.aspx?UnitId=2thVboChxuKs"
    raw = _get_json(url, cache_key="moa:public_shelters", ttl_seconds=6 * 3600)

    out: List[Dict[str, str]] = []
    for item in raw:
        open_time = html.unescape(str(item.get("OpenTime") or ""))
        open_time = (
            open_time.replace("<br />", "\n")
            .replace("<br/>", "\n")
            .replace("<br>", "\n")
        )

        out.append({
            "城市名稱": _clean_str(item.get("CityName")),
            "收容所名稱": _clean_str(item.get("ShelterName")),
            "地址": _clean_str(item.get("Address")),
            "電話號碼": _clean_str(item.get("Phone")),
            "開放時間": open_time.strip(),
        })
    return out


# 遺失啟示資料
def fetch_lost_notices() -> List[Dict[str, str]]:
    url = "https://data.moa.gov.tw/Service/OpenData/TransService.aspx?UnitId=IFJomqVzyB0i"
    raw = _get_json(url, cache_key="moa:lost_notices", ttl_seconds=30 * 60)

    keep_keys = ["晶片號碼", "寵物名", "寵物別", "性別", "特徵", "遺失時間", "遺失地點", "飼主姓名", "連絡電話", "PICTURE"]
    out: List[Dict[str, str]] = []
    for item in raw:
        row = {k: _clean_str(item.get(k)) for k in keep_keys}
        row["圖片"] = row.pop("PICTURE", "")
        out.append(row)
    return out


# 動物認領養資料（只取 OPEN）
def fetch_adoptions_open() -> List[Dict[str, str]]:
    url = "https://data.moa.gov.tw/Service/OpenData/TransService.aspx?UnitId=QcbUEzN6E6DL"
    raw = _get_json(url, cache_key="moa:adoptions_open", ttl_seconds=15 * 60)

    sex_map = {"M": "公", "F": "母", "N": "未知"}
    body_map = {"SMALL": "小型", "MEDIUM": "中型", "BIG": "大型"}
    age_map = {"CHILD": "幼年", "ADULT": "成年"}
    tf_unknown_map = {"T": "是", "F": "否", "N": "未知", "": "未知"}

    out: List[Dict[str, str]] = []
    for item in raw:
        status = _clean_str(item.get("animal_status")).upper()
        if status != "OPEN":
            continue

        out.append({
            "種類": _clean_str(item.get("animal_kind")),
            "性別": sex_map.get(_clean_str(item.get("animal_sex")).upper(), "未知"),
            "體型": body_map.get(_clean_str(item.get("animal_bodytype")).upper(), "未知"),
            "毛色": _clean_str(item.get("animal_colour")),
            "年齡": age_map.get(_clean_str(item.get("animal_age")).upper(), "未知"),
            "是否結紮": tf_unknown_map.get(_clean_str(item.get("animal_sterilization")).upper(), "未知"),
            "疫苗接種": tf_unknown_map.get(_clean_str(item.get("animal_bacterin")).upper(), "未知"),
            "收容中心名稱": _clean_str(item.get("shelter_name")),
            "收容中心電話": _clean_str(item.get("shelter_tel")),
        })
    return out
