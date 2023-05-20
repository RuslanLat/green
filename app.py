import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import pandas as pd
import numpy as np

st.set_page_config(page_title="Плант Бокс - технологии возделывания лекарственных", page_icon="/images/flavicon.ico")

custom_css = """<style>
                    .championship-tab-company {
                        max-height: 150px;
                        max-width: 150px;
                        align-items: center;
                        display: flex;
                        box-sizing: border-box;
                    }
                </style>
                """
st.markdown(custom_css, unsafe_allow_html=True)


st.markdown("""<div class="championship-tab-company-container">
                        <img class="championship-tab-company"
                        src="https://lodmedia.hb.bizmrg.com/avatars/company_969749.png"
                        alt="partner">
                </div>""", unsafe_allow_html=True)


st.write(""" В настоящее время ощущаются перебои в поставках различных экстрактов и лекарственных субстанций. По статистике по разным позициям импорт составляет от 20 до 80% всего используемого сырья. Важнейшая задача – помочь российским фермерам вырастить сырье на их земле.  

В базе данных представлена классификацированная информации из книг и открытых источников по различным семантическим признакам: ареалам произрастания дикорастущих лекарственных растений, типам почв, климатическим условиям и т.д.  

Данное решение будет способствовать устранению проблемы нехватки консолидированной информации по возделыванию лекарственных культур. """)

# подключение к базе данных (в случае отсутствия база данных создается)
connection = sqlite3.connect("data/plantarium.db")
# создание объекта подключения
cursor = connection.cursor()

cursor.execute("""SELECT plant_ru_name
                  FROM plant_ru;""")

plant_ru_names = cursor.fetchall()
plant_ru_names = [plant_ru_name[0] for plant_ru_name in plant_ru_names]

cursor.execute("""SELECT region_name
                  FROM regions;""")

region_names = cursor.fetchall()
region_names = [region_name[0] for region_name in region_names]

st.markdown("""
    <style>
        .stMultiSelect [data-baseweb=label] span{
            max-width: 400px;
            font-size: 0.6rem;
        }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("Выбор параметров поиска")
    region_options = st.multiselect(
                        label = 'Наименование региона',
                        options=region_names,
                        default=region_names[:3],
                        help="Выбирете (введите) наименование региона",
                        ) #label_visibility="hidden"
    plant_ru_options = st.multiselect(
                        label = 'Наименование растения',
                        options=plant_ru_names,
                        default=plant_ru_names[:3],
                        help="Выбирете (введите) наименование растения",
                        ) #label_visibility="hidden"

cursor.execute(f"""SELECT region_name, book_name, book_year, book_web
                  FROM regions
                  INNER JOIN books USING(region_id)
                  WHERE region_name IN ({','.join(['?']*len(region_options))});""", region_options)

plants_data = cursor.fetchall()
colnames = ["Наименование региона", "Наименование книги (источник)", "Год книги", "Веб сайт книги"]
books_df = pd.DataFrame(data=plants_data, columns=colnames)
books_df["Год книги"] = books_df["Год книги"].fillna("-  ").astype("str").apply(lambda x: x[:-2])

st.write("Список красных книг")

st.write(books_df[:10])

cursor.execute(f"""SELECT plant_ru_name
                  FROM plant_ru
                  WHERE plant_ru_name IN ({','.join(['?']*len(plant_ru_options))});""", plant_ru_options)
plant_ru_data = cursor.fetchall()
colnames = ["Наименование растения"]
plant_ru_df = pd.DataFrame(data=plant_ru_data, columns=colnames)

st.write(plant_ru_df)

st.write("##")
st.markdown("<h5 style='text-align: center; color: blac;'> ©️ Команда Extreme DS </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: blac;'> Цифровой прорыв 2023 </h5>", unsafe_allow_html=True)