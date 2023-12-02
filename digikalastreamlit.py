import time
import requests
import pandas as pd
import io
import streamlit as st
from PIL import Image
from jdatetime import datetime as jdatetime_datetime
from concurrent.futures import ThreadPoolExecutor
import os

brand_mapping = {
    "Samsung": 18,
    "Xiaomi": 1662,
    "Apple": 10,
    "Nokia": 20,
    "Honor": 7186,
    "Huawei": 82,
    "Motorola": 23,
    "G Plus": 11349,
}

sort_mapping = {
    "پرفروش‌ترین": 22,
    "پربازدیدترین": 4,
    "جدیدترین": 1,
    "ارزان‌ترین": 20,
    "گران‌ترین": 21,
}

phone_names = []
def scrape_product_page(page, selected_brand_id, selected_sort_id, include_unavailable):
    url = f"https://api.digikala.com/v1/categories/mobile-phone/search/?brands%5B0%5D={selected_brand_id}&sort={selected_sort_id}&seo_url=%2Fcategory-mobile-phone%2Fproduct-list%2F%3Fbrands%255B0%255D%3D{selected_brand_id}%26sort%3D7&page={page}"
    response = requests.get(url)
    data = response.json()

    rows = []
    for pr in data["data"]["products"]:
        product_id = pr["id"]
        try:
            name_fa = pr["title_fa"]
            name_fa = name_fa.replace('گوشی موبایل ', '')
        except KeyError:
            name_fa = "نام فارسی تعریف نشده است"

        try:
            name_en = pr["title_en"]
            name_en = name_en.replace('Mobile Phone','')

        except KeyError:
            name_en = "نام انگلیسی تعریف نشده است"

        try:
            brand = pr["data_layer"]["brand"]
        except (KeyError, TypeError):
            brand = "برند تعریف نشده است"

        try:
            selling_price = pr["default_variant"]["price"]["selling_price"]
            selling_price = selling_price // 10
        except(KeyError, TypeError):
            if include_unavailable:
                selling_price = "ناموجود"
            else:
                continue
        try:
            Old_price = pr["default_variant"]["price"]["rrp_price"]
            Old_price = Old_price // 10

        except (KeyError, TypeError):
            Old_price = "0"

        try:
            discount_percent = pr["default_variant"]["price"]["discount_percent"]
        except (KeyError, TypeError):
            discount_percent = "تخفیف ندارد"

        try:
            order_limit = pr["default_variant"]["price"]["order_limit"]
        except (KeyError, TypeError):
            order_limit = "0"

        try:
            product_warranty = pr["default_variant"]["warranty"]["title_fa"]
        except:
            product_warranty = "گارانتی ندارد"

        try:
            product_link = f"https://www.digikala.com/product/dkp-{product_id}/"
        except (KeyError, TypeError):
            product_link = "لینک  تعریف نشده است"
        try:
            product_seller = pr["default_variant"]["seller"]["title"]
        except:
            product_seller = "فروشنده ثبت نشده است"
        try:
            product_seller_grade = pr["default_variant"]["seller"]["grade"]["label"]
        except:
            product_seller_grade = ""
        try:
            product_seller_link = pr["default_variant"]["seller"]["url"]
        except:
            product_seller_link = ""
        try:
            min_price_in_last_month = pr["properties"]["min_price_in_last_month"]
            min_price_in_last_month = min_price_in_last_month // 10
        except (KeyError, TypeError):
            min_price_in_last_month = "0"

        row = {
            "id محصول": product_id,
            "برند": brand,
            "نام فارسی": name_fa,
            "قیمت فروش": selling_price,
            "قیمت قبلی": Old_price,
            "کمترین قیمت در ماه گذشته": min_price_in_last_month,
            "فروشنده": product_seller,
            "گرید فروشنده": product_seller_grade,
            "درصد تخفیف": discount_percent,
            "گارانتی": product_warranty,
            "محدودیت سفارش": order_limit,
            "لینک محصول": product_link,
            "لینک مربوط به فروشنده": product_seller_link,
            "نام انگلیسی": name_en,
        }
        rows.append(row)

    return rows

def scrape_data(brand_var, sort_var, checkbox_var):
    selected_brand = brand_var
    selected_brand_id = brand_mapping[selected_brand]
    selected_sort = sort_var
    selected_sort_id = sort_mapping[selected_sort]
    include_unavailable = checkbox_var
    url = f"https://api.digikala.com/v1/categories/mobile-phone/search/?brands%5B0%5D={selected_brand_id}&sort={selected_sort_id}&seo_url=%2Fcategory-mobile-phone%2Fproduct-list%2F%3Fbrands%255B0%255D%3D{selected_brand_id}%26sort%3D7&page=1"
    response = requests.get(url)
    data = response.json()
    pages = data["data"]["pager"]["total_pages"]
    pages = int(pages)
    rows = []
    counter = 0
    with ThreadPoolExecutor() as executor:
        futures = []
        for page in range(1, pages + 1):
            future = executor.submit(scrape_product_page, page, selected_brand_id, selected_sort_id, include_unavailable)
            futures.append(future)
        for future in futures:
            rows.extend(future.result())
    df = pd.DataFrame(rows)
    return df

#Set up the Streamlit app
st.set_page_config(layout="centered",page_title="DigiKala Scaper",page_icon="📱")
col1, col2 = st.columns([1, 2])
col2.title("استخراج اطلاعات آنلاین گوشی موبایل از دیجی کالا")
col2.markdown("میتوانید به صورت آنلاین برای استخراج قیمت های موبایل و مقایسه آنها در سایت دیجی کالا ، استفاده کنید")

col1.image("digikala.png", width=200)
st.markdown("---")
st.write("Developed by : HOSSEIN QASHQAEII 🧛 - ✉️ وبسایت : www.webscraper.ir ✉️)")
st.title(" ")
st.write("میتوانید به صورت آنلاین برای استخراج قیمت های موبایل و مقایسه آنها در سایت دیجی کالا ، استفاده کنید")

brand_var = st.selectbox("برند مورد نظر را انتخاب کنید:", list(brand_mapping.keys()))
sort_var = st.selectbox("مرتب سازی بر اساس:", list(sort_mapping.keys()))
checkbox_var = st.checkbox("شامل محصولات ناموجود", value=False)
if st.button("شروع استخراج"):


    start_time = time.time()
    df = scrape_data(brand_var, sort_var, checkbox_var)
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    end_time = time.time()
    st.write("تعداد محصولات استخراج شده:", len(df))
    st.write("مدت زمان طول کشیده: 👻 ", end_time - start_time, "ثانیه ⏰ ")
    st.write("آخرین بروز رسانی: ⌚ ", jdatetime_datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    st.write("داده های استخراج شده: 📝 ")
    st.dataframe(df, width=1500, height=500)
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    excel_file.seek(0)
    download_button = st.download_button("Download Excel 💾", data=excel_file, file_name=f'data{brand_var}(Developed-by-HOSSEIN-QASHQAEII).xlsx')
st.markdown("---")
