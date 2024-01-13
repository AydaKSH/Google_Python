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
    cred_dic = {'type': 'service_account',
            'project_id': 'polar-land-409907',
            'private_key_id': '6ffcee7e78d0051ff13ccb718eb7481d6c99cc48',
            'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCZCyNMkRLhDYPs\n5n9VugJr2UD2SE8QzbQYji0MQgd34YRDinfHt1HyvoR2GcuyMeGSummFGVbMqVLG\nMqTI0yrHw907CCkRgoB6i+oB5OVpNOvkkSvj2JxGqly2D0axrevOwWgoyXxZLDf8\nJ5a4ldvueFCiDCWStcxT1919xzuaiT7bIHTWgOA0XBB8du1A08jLGyQcMb2N8xf2\noRIhalz6zdlM+ynjhcgrRuA9Pnw/q5QV2tKV18DGjVF77/77HEAl2h6BR6XKoWmz\noMmRIx3oqtWF0xvfXFskdJVGBo0AJh2YMp7pGumZIXLyT8cFH3uHPotqv/I9EAhW\nPIB0IlKTAgMBAAECggEAQiP5Hmb4FMEFicVXtJHN6BQdKhK38NglhBM1zr1eguW4\nhoP6HhrQ1KqXjn65dIpwJTxgy//Wbl6jAjry0kPIkkrIenGdZg7TPaLn/+ePabdQ\nVxiSMkbzyupnZNsXP0Sdy130iOQC1HryuwvU7HL/eIEQv+el+VCOPJHnDCulS7Rn\nlaFjAuIw1U1HewU6uchJhASGJjx+kUtEwi80wLSnzlYpiGX1alwGkYI/aqvyTtQt\nwLQRy8XEix2HsGxSubAHOPDPU5ZeMQ6Mi4BjeG6A69a8uKM7OOaJP79dZhkbWnlv\nfw2a21bDhD0w0tzUjsLaMHNhKfPCehPLcSIWcWa0QQKBgQDI600QcsgAkWYhALWA\nau/Ra21tn9oxn03wnzn40JzeC2lZct+FGqzTu/J4wH86dFc3Ef+xU0FJNXRc2rtV\nFcctZoQEzN/XVhi3XatwLrGus29d3RldZryoTOHVEDn/ne/ZMDv6b4BeS3T0S0JQ\nPq/qeSWRUyMNFjzwTDlVJCYKYQKBgQDC/+Dod9Ao2D3+O1AjQuMBabFmKXPI8dG0\nVI5PEaV6NUCLivh+iharxNF/v2Kl1d04bYu6/WkLl8RtrxkRR3UdqEKxMBnzNhkE\n91MwJKDf8XR6UCOGH5iMN7YQMo8DcxIj5h+IrD3F+178/lUU+zVbybTZ1JxJIQT0\nglH9UdZJcwKBgELD/l3i5pdZuchpxeagooTC4CA3qHgo6et13fvSxu36eM2ioKhI\njvnlUNPTk/PGyVyhfIhelClRvBNHFE1X6VIq6N/3fMK/94Kne9rRiXX2ZqGYYV9q\nTnLW6Yy10bAhuZxArQ2xk8TB6mFryOOFkUunalZ6fAFTTHjFu5+RXZrBAoGAL1qK\nGIn3/+M7csCenmGA1PgAv4lzd6nZvgwGnwbvA3VpHjn6TGhmRwI9yeMFJrZ/yVM4\n6ojdeJY7elNaKAsNUs1onLTMqHZLrxwMlJVgh+GP4qARcGG93tcsnFRazICmOBeL\nMtp5CdoYYCG3MagrdgXOqFNsPIoLNQFsvbKg8icCgYEAgRH4K8UBdFFv/qWM15Pf\nvyMC9SMoAUyTlwZCqoP+OXm2hrN2LoGpQN8K7KTuTt17/gIR52fuhGjsV5/Bj1j/\n51cdtGsb6Jyhb+whTYsacHMOXSjd5dd44Oc21AJdpty6ykkCBqagKdsj5vyz64s4\nPkRAIa0rb9GuoUkrhxZxphM=\n-----END PRIVATE KEY-----\n',
            'client_email': 'aydaksh78@polar-land-409907.iam.gserviceaccount.com',
            'client_id': '110264698144004186426',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/aydaksh78%40polar-land-409907.iam.gserviceaccount.com',
            'universe_domain': 'googleapis.com'}


    gc = gspread.service_account_from_dict(cred_dic)
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

