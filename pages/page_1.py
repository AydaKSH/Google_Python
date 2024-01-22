import streamlit as st
import pandas as pd

df = pd.DataFrame({'id':['ayda', 'ayda', 'mari', 'mari'], 'value':[2, 3, 45, 9]})
dic = dict()

st.dataframe(df)

for i in range(df.shape[0]):
    k = df['id'][i]
    v = df['value'][i]
    if k in dic.keys():
        dic[k] += v
    else:
        dic[k] = v
        
