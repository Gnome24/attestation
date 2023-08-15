import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, ttest_rel, mannwhitneyu

# Заголовок страницы
st.title("Исследование данных с использованием Streamlit")

# Загрузка CSV-файла
uploaded_file = st.file_uploader("Загрузите CSV файл", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.dataframe(data)

    # Выбор переменных для визуализации
    column_names = data.columns.tolist()
    x_variable = st.selectbox("Выберите переменную для оси X:", column_names)
    y_variable = st.selectbox("Выберите переменную для оси Y:", column_names)

    # Визуализация
    st.subheader("Распределение переменных")
    
    if data[x_variable].dtype == "object":
        # Если переменная категориальная, строим pie chart
        st.write("По категориям:")
        pie_data = data[x_variable].value_counts()
        st.write(pie_data)
        fig, ax = plt.subplots()
        ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
        st.pyplot(fig)
    else:
        # Если переменная числовая, строим гистограмму
        st.write("Гистограмма:")
        fig, ax = plt.subplots()
        sns.histplot(data[x_variable], bins=20, ax=ax)
        st.pyplot(fig)

    if data[y_variable].dtype == "object":
        st.write("По категориям:")
        pie_data = data[y_variable].value_counts()
        st.write(pie_data)
        fig, ax = plt.subplots()
        ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
        st.pyplot(fig)
    else:
        st.write("Гистограмма:")
        fig, ax = plt.subplots()
        sns.histplot(data[y_variable], bins=20, ax=ax)
        st.pyplot(fig)

    
    st.subheader("Проверка гипотезы")
    hypothesis_test = st.selectbox(
        "Выберите проверочный алгоритм:",
        ["", "A/B тест", "t-тест", "Mann-Whitney U-тест"]
    )
    
    if hypothesis_test != "":
        test_variable = st.selectbox("Выберите первую переменную для теста:", column_names)
        second_variable = st.selectbox("Выберите вторую переменную для теста:", column_names)
        
    
        if hypothesis_test == "A/B тест":
            group1 = data[data[test_variable] == data[test_variable].unique()[0]][second_variable]
            group2 = data[data[test_variable] == data[test_variable].unique()[1]][second_variable]
            st.write("Результаты A/B теста:")
            t_statistic, p_value = ttest_ind(group1, group2)
            st.write(f"t-статистика: {t_statistic}")
            st.write(f"p-значение: {p_value}") 
        
        elif hypothesis_test == "t-тест":
            group_by_variable = st.selectbox("Выберите переменную для группировки:", column_names)
            groups = data[group_by_variable].unique()

            if len(groups) != 2:
                st.error("Для t-теста нужно выбрать 2 группы.")
            else:
                group1 = data[data[group_by_variable] == groups[0]][second_variable]
                group2 = data[data[group_by_variable] == groups[1]][second_variable]
                t_statistic, p_value = ttest_ind(group1, group2)
                st.write("Результаты t-теста:")
                st.write(f"t-статистика: {t_statistic}")
                st.write(f"p-значение: {p_value}")
        
        elif hypothesis_test == "Mann-Whitney U-тест":
            group_by_variable = st.selectbox("Выберите переменную для группировки:", column_names)
            groups = data[group_by_variable].unique()

            if len(groups) != 2:
                st.error("Для Mann-Whitney U-теста нужно выбрать 2 группы.")
            else:
                group1 = data[data[group_by_variable] == groups[0]][second_variable]
                group2 = data[data[group_by_variable] == groups[1]][second_variable]
                statistic, p_value = mannwhitneyu(group1, group2)
                st.write("Результаты Mann-Whitney U-теста:")
                st.write(f"Статистика: {statistic}")
                st.write(f"p-значение: {p_value}")
