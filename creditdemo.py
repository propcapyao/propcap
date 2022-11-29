import streamlit as st
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(layout = "wide")

col1, col2 = st.columns([1, 3])
with col1:
    st.image("PropCap_Logo.jpeg", width = 150)
with col2:
    st.header("")
    st.title("信用情報開示報告")

tab1, tab2 = st.tabs(["保証委託申込書", "クレジットスコア"])
with tab1:
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("申込者・賃借人")
        name = st.text_input("氏名")
        nameinfurigana = st.text_input("氏名（フリガナ）")
        gender = st.radio("性別", ["男", "女"])
        birthdate = st.date_input("生年月日", value = datetime.date.today())
        currentaddresspostalcode = st.text_input("郵便番号（現住所）")
        currentaddressprefecture = st.selectbox("都道府県（現住所）", ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県",
                                                                    "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
                                                                    "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
                                                                    "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県",
                                                                    "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"])
        currentaddressmunicipality = st.text_input("市区町村（現住所）")
        currentaddresshousenumber = st.text_input("番地（現住所）")
        currentaddressstatus = st.selectbox("現住居", ["自己所有", "家族所有", "賃貸", "社宅", "その他"])
        homephonenumber = st.text_input("自宅電話")
        cellphonenumber = st.text_input("携帯電話")
        companyname = st.text_input("勤務先名称")
        workphonenumber = st.text_input("勤務先電話")
        workaddresspostalcode = st.text_input("郵便番号（勤務先住所）")
        workaddressprefecture = st.selectbox("都道府県（勤務先住所）", ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県",
                                                                    "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
                                                                    "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
                                                                    "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県",
                                                                    "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"])
        workaddressmunicipality = st.text_input("市区町村（勤務先住所）")
        workaddresshousenumber = st.text_input("番地（勤務先住所）")
        employmentstatus = st.selectbox("雇用形態", ["公務員", "会社経営者", "役員・正社員", "派遣社員", "個人事業主", "個人事業勤務", "アルバイト・パート", "学生", "年金", "生活保護受給", "無職", "その他"])
        department = st.text_input("部署")
        annualincome = st.number_input("年収（万円）", value = 0, format = "%d")
        yearsofservice = st.number_input("勤務年数（年）", value = 0, format = "%d")
        st.write("（ 外国籍の方 ）")
        visastatus = st.text_input("在留資格")
        termofstay = st.text_input("在留期間")
        japaneseproficiency = st.selectbox("日本語検定資格", ["N-1", "N-2", "N-3", "N-4"])
        yearsinjapan = st.number_input("日本での合計在住年数（年）", value = 0, format = "%d")
        housemate = st.checkbox("同居人")
        residentsperson = st.text_input("氏名（実入居者）")
        residentspersoninfurigana = st.text_input("フリガナ（実入居者）")
        relationship = st.text_input("続柄")
        residentspersonbirthdate = st.date_input("生年月日（実入居者）", value = datetime.date.today())
        residentspersoncellphonenumber = st.text_input("携帯電話（実入居者）")

    with col4:
        st.subheader("物件内容")
        applicationdate = st.date_input("お申込日", value = datetime.date.today())
        moveindate = st.date_input("入居予定日", value = datetime.date.today())
        applicationform = st.radio("申込形態", ["新規申込者", "既存入居者"])
        purposeofproperty = st.selectbox("物件用途", ["住居用", "住居学生用", "ﾄﾗﾝｸﾙｰﾑ", "倉庫", "駐車場", "店舗 ・ 事務所", "住居兼店舗・事務所"])
        reasontomove = st.text_input("転居理由")
        purposeofuseforoffice = st.text_input("店舗・事務所の場合の利用目的")
        propertypostalcode = st.text_input("郵便番号（物件住所）")
        propertyprefecture = st.selectbox("都道府県（物件住所）", ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県",
                                                                "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
                                                                "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
                                                                "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県",
                                                                "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"])
        propertymunicipality = st.text_input("市区町村（物件住所）")
        propertyhousenumber = st.text_input("番地（物件住所）")
        buildingname = st.text_input("物件名")
        buildingnameinfurigana = st.text_input("物件名（フリガナ）")

        rent = st.number_input("家賃（賃料）", value = 0, format = "%d")
        managementfee = st.number_input("共益費・管理費", value = 0, format = "%d")
        parkinglotfee = st.number_input("駐車場", value = 0, format = "%d")
        watercharges = st.number_input("水道料・町（区）費", value = 0, format = "%d")
        miscellaneousfee = st.number_input("その他", value = 0, format = "%d")
        st.write("月額賃料")
        st.write(rent+managementfee+parkinglotfee+watercharges+miscellaneousfee)
        deposits = st.number_input("敷金・保証金", value = 0, format = "%d")
        giftmoney = st.number_input("礼金", value = 0, format = "%d")
        cancellationfee = st.number_input("敷引（解約引き）", value = 0, format = "%d")

        st.subheader("緊急連絡先")
        emergencycontact = st.text_input("氏名（緊急連絡先）")
        emergencycontactinfurigana = st.text_input("フリガナ（緊急連絡先）")
        emergencycontactrelationship = st.text_input("続柄（緊急連絡先）")
        emergencycontactgender = st.radio("性別（緊急連絡先）", ["男", "女"])
        emergencycontactbirthdate = st.date_input("生年月日（緊急連絡先）", value = datetime.date.today())
        emergencycontactpostalcode = st.text_input("郵便番号（緊急連絡先）")
        emergencycontactprefecture = st.selectbox("都道府県（緊急連絡先）", ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県",
                                                                         "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
                                                                         "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
                                                                         "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県",
                                                                         "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"])
        emergencycontactmunicipality = st.text_input("市区町村（緊急連絡先）")
        emergencycontacthousenumber = st.text_input("番地（緊急連絡先）")
        emergencycontactcellphonenumber = st.text_input("携帯電話（緊急連絡先）")

with tab2:
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Affordability:")
        affordability_flag1 = st.checkbox("Tenant's bank account is confirmed")
        affordability_flag2 = st.checkbox("Tenant's annual income is confirmed")
        affordability_flag3 = st.checkbox("The tenant is able to afford their rent based on the income verified")
        affordability_flag4 = st.slider("The tenant is able to pay the rent in advance", 0, 24, 0, 1)

        st.subheader("Identity:")
        identity_flag1 = st.checkbox("Identity verified")
        identity_flag2 = st.checkbox("Sanction check verified")

    with col6:
        st.subheader("Address History:")
        address_flag1 = st.checkbox("Tenant’s address history verified")
        address_flag2 = st.checkbox("Obtain proof of current address and identification")

        st.subheader("Credit Reference:")
        credit_reference_flag1 = st.checkbox("Declared adverse credit?")
        credit_reference_flag2  = st.number_input("Total value of CCJs", value = 0, format = "%d")
        credit_reference_flag3  = st.number_input("Total CCJs value outstanding", value = 0, format = "%d")
        credit_reference_flag4 = st.checkbox("Notice of Correction recorded?")
        credit_reference_flag5 = st.checkbox("Adverse records registered to an alias or previous name of tenant")
        credit_reference_flag6 = st.checkbox("Adverse records registered to the tenant at an undisclosed address")

    st.markdown("***")

    creditscore = int(min(1000 * (float(affordability_flag1) + float(affordability_flag2) + float(affordability_flag3) + float(affordability_flag4 / 24) + float(identity_flag1) + float(identity_flag2)  + float(address_flag1) + float(address_flag2) + (1 - float(credit_reference_flag1)) +  (1 - min(float(credit_reference_flag3) / 1000000, 1.0)) + (1 - min(float(credit_reference_flag3) / max(float(credit_reference_flag2), 1.0), 1.0)) + (1 - float(credit_reference_flag4)) + (1 - float(credit_reference_flag5)) + (1 - float(credit_reference_flag6))) / 14, 999))
    #creditscore = (1 - min(float(credit_reference_flag3) / 1000000, 1.0)) + (1 - min(float(credit_reference_flag3) / max(float(credit_reference_flag2), 1.0), 1.0))

    col7, col8 = st.columns([3, 1])
    with col7:
        st.markdown(f'<h1 style="text-align: right;">{"Credit Score:"}</h1>', unsafe_allow_html = True)
    with col8:
        st.markdown(f'<h1 style="text-align: left; color:#E9340D;">{creditscore}</h1>', unsafe_allow_html = True)
