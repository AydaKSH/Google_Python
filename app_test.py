import streamlit as st


username = 'AydaKSH'
password = '123456'
user = st.text_input('username')
pass_2 = st.text_input('password')
if user == username:
  if pass_2 == password:
    st.markdown('welcome')
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

