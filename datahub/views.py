from django.core.paginator import Paginator
from django.shortcuts import render

import requests

from .services import (
    fetch_animal_protect_units,
    fetch_public_shelters,
    fetch_lost_notices,
    fetch_adoptions_open,
)

def _safe_fetch(fetch_fn, *, error_title: str):
    """Fetch external data safely for public pages."""
    try:
        return fetch_fn(), None
    except requests.RequestException:
        return [], f"{error_title}：目前暫時無法取得資料，請稍後再試。"


def _paginate(request, items, per_page=20):
    paginator = Paginator(items, per_page)
    page_number = request.GET.get("page") or 1
    return paginator.get_page(page_number)

def _filter(items, q: str, fields):
    if not q:
        return items
    q_lower = q.lower()
    out = []
    for it in items:
        hay = " ".join([str(it.get(f, "")) for f in fields]).lower()
        if q_lower in hay:
            out.append(it)
    return out

def animal_protect_units_page(request):
    q = (request.GET.get("q") or "").strip()
    items, error = _safe_fetch(fetch_animal_protect_units, error_title="動保單位資料")
    items = _filter(items, q, ["動保單位名稱", "地址", "電話號碼"])
    return render(
        request,
        "datahub/animal_protect_units.html",
        {"page_obj": _paginate(request, items, 20), "q": q, "error": error},
    )

def public_shelters_page(request):
    q = (request.GET.get("q") or "").strip()
    items, error = _safe_fetch(fetch_public_shelters, error_title="公立收容所資料")
    items = _filter(items, q, ["城市名稱", "收容所名稱", "地址", "電話號碼"])
    return render(
        request,
        "datahub/public_shelters.html",
        {"page_obj": _paginate(request, items, 20), "q": q, "error": error},
    )

def lost_notices_page(request):
    q = (request.GET.get("q") or "").strip()
    items, error = _safe_fetch(fetch_lost_notices, error_title="遺失啟示資料")
    items = _filter(items, q, ["晶片號碼", "寵物名", "寵物別", "特徵", "遺失地點", "連絡電話"])
    return render(
        request,
        "datahub/lost_notices.html",
        {"page_obj": _paginate(request, items, 12), "q": q, "error": error},
    )

def adoptions_page(request):
    q = (request.GET.get("q") or "").strip()
    items, error = _safe_fetch(fetch_adoptions_open, error_title="認養公告資料")
    items = _filter(items, q, ["種類", "性別", "體型", "毛色", "收容中心名稱", "收容中心電話"])
    return render(
        request,
        "datahub/adoptions.html",
        {"page_obj": _paginate(request, items, 20), "q": q, "error": error},
    )
