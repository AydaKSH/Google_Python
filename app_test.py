import streamlit as st
import pandas as pd
import gspread
import json



username = 'AydaKSH'
password = '123456'
user = st.text_input('username')
pass_2 = st.text_input('password')

if user == username:
  if pass_2 == password:
    st.markdown('welcome')
    cred_file = st.file_uploader('Upload Credentials.json File')
    if cred_file is not None:
      content = cred_file.read()
      cred_dict = json.load(content)
      gc = gspread.service_account_from_dict(cred_dict)
      sh = gc.open("گزارش هویج").get_worksheet(16)
      d = sh.acell('A1').value
      st.write('A1 is : ', d)

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

