import streamlit as st

a = st.number_input('int')
b = st.number_input('int2')

c = a + b
st.write('sum is', c)

print(c)