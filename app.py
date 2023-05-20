import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(page_title="Плант Бокс - технологии возделывания лекарственных",
                   page_icon="/images/favicon.png",
                   layout="wide")

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

st.write("##")

st.write(""" В настоящее время ощущаются перебои в поставках различных экстрактов и лекарственных субстанций. По статистике по разным позициям импорт составляет от 20 до 80% всего используемого сырья. Важнейшая задача – помочь российским фермерам вырастить сырье на их земле.  

В базе данных представлена классификацированная информации из книг и открытых источников по различным семантическим признакам: ареалам произрастания дикорастущих лекарственных растений, типам почв, климатическим условиям и т.д.  

Данное решение будет способствовать устранению проблемы нехватки консолидированной информации по возделыванию лекарственных культур. """)


# подключение к базе данных (в случае отсутствия база данных создается)
connection = sqlite3.connect("data/plantarium.db")
# создание объекта подключения
cursor = connection.cursor()

cursor.execute("""SELECT region_name
                    FROM regions;""")
region_names = cursor.fetchall()
region_names = [region_name[0] for region_name in region_names]

st.subheader("Введите (выбирете) наименование региона")

select_option = st.selectbox('', region_names,
                            help="Введите (выбирете) наименование региона", index=12)

cursor.execute("""SELECT plant_ru_name, plant_lat_name, book_name, book_year, book_web
                    FROM regions
                    INNER JOIN books USING(region_id)
                    INNER JOIN redbooks USING(book_id)
                    INNER JOIN plant_ru USING(plant_ru_id)
                    INNER JOIN plant_lat USING(plant_lat_id)
                    WHERE region_name == ?;""", (select_option,))

plants_data = cursor.fetchall()
colnames = ["Название растения RU",
                "Название растения LAT", "Наименование книги (источник)",
                "Год книги", "Веб сайт книги"]
books_df = pd.DataFrame(data=plants_data, columns=colnames)

st.subheader("Список растений в красных книгах")

gd = GridOptionsBuilder.from_dataframe(books_df)
gd.configure_pagination(enabled=True,
                            paginationAutoPageSize=False,
                            paginationPageSize=15)
gd.configure_default_column(editable=True, groupable=True)
    #gd.configure_selection(selection_mode="multiple", use_checkbox=True)
gridoptions = gd.build()
grid_table = AgGrid(books_df, gridOptions=gridoptions,
                        update_mode=GridUpdateMode.SELECTION_CHANGED,
                        allow_unsafe_jscode=True,
                        theme="alpine")

st.write("##")
st.markdown("<h5 style='text-align: center; color: blac;'> ©️ Команда Extreme DS </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: blac;'> Цифровой прорыв 2023 </h5>", unsafe_allow_html=True)