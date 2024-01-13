import streamlit as st
import pandas as pd
import gspread



username = 'AydaKSH'
password = '123456'
user = st.text_input('username')
pass_2 = st.text_input('password')

if user == username:
  if pass_2 == password:
    st.markdown('welcome')
    file = st.file_uploader('file')
    if file is not None:
      df = pd.read_csv(file)
      st.dataframe(df)

      path = str(st.text_input('Path'))

      if path != '':
          gc = gspread.service_account(path)
          sh = gc.open("گزارش هویج").get_worksheet(16)
          a = sh.acell('A1').value
          st.title(a)

  else:
    st.markdown('password is wrong')
else:
  st.markdown('you are not allowed')
a = st.number_input('int')
b = st.number_input('int2')

c = a + b
st.write('sum is', c)
st.markdown('this app is private')
st.markdown('update is available')

