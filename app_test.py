import streamlit as st
import pandas as pd
import gspread
import json
from datetime import datetime
import jdatetime
from datetime import date
import plotly.figure_factory as ff
#from datetime import timedelta
#from datetime import time

# ======================================================
#                    Visualization
# ======================================================
def bullet_chart(df, project_df, project):
    idxx = list(project_df[project_df.Project == project].index)[0]
    try:
        duration = int(project_df.InstagramPeriod[idxx]) 
    except:
        duration = 1
    
    default_project_period = 30 * duration
    
    today = date.today()
    
    idx = list(df[df.Project == project].index)[0]
    first_post_date = df.FirstPostDate[idx]
    year_0 = int(first_post_date.split(sep = '-')[0])
    month_0 = int(first_post_date.split(sep = '-')[1])
    day_0 = int(first_post_date.split(sep = '-')[2])
    first_date = jdatetime.date(year_0, month_0, day_0).togregorian()
    
    diff_day = int((today - first_date).days)

    if diff_day > default_project_period:
        st.write(diff_day, 'days have passed since the start of the project')
        st.markdown('You Have Passed The Deadline! But If You Want to Recaculate Please Enter a New Period')
        project_period = st.number_input('Please Enter The New Period', min_value=30)
        ratio = diff_day / project_period
        
    else:
        ratio = diff_day / default_project_period

    
    total_posts = (int(df.TotalPosts[idx]) + int(df.RemainingPosts[idx])) * duration
    expected_posts = int(ratio * total_posts)
                         
    total_stories = (int(df.Stories[idx]) + int(df.RemainingStories[idx])) * duration 
    expected_stories = int(ratio * total_stories) 
    
    total_activity = (float(df.ActivityTime[idx]) + float(df.RemainingActivityTime[idx])) * duration            
    expected_activity = round(ratio * total_activity, 2)
    
    post_range_lst = [expected_posts * 0.8, expected_posts * 1.2, total_posts]
    story_range_lst = [expected_stories * 0.8, 1.2 * expected_stories, total_stories]
    activity_range_lst = [expected_activity * 0.8, expected_activity * 1.2, total_activity]
    
    post_point = [expected_posts]
    story_point = [expected_stories]
    activity_point = [expected_activity]
    
    post_performance = [0, int(df.TotalPosts[idx])]
    story_performance = [0, int(df.Stories[idx]) ]
    activivty_performance = [0, float(df.ActivityTime[idx])]
    
    data = (
        {"label": "Post", "range": post_range_lst, "performance": post_performance, "point": post_point},
        {"label": "Story", "range": story_range_lst, "performance": story_performance, "point": story_point},
        {"label": "ActivityTime", "range": activity_range_lst, "performance": activivty_performance, "point": activity_point}
        )
    
    fig = ff.create_bullet(
        data, titles='label', markers='point',
        measures='performance', ranges='range', orientation='h',
    )
    if ratio <= 1:
        st.plotly_chart(fig, use_container_width=True)
                          
    return
     
# ======================================================
#                    Functions
# ======================================================

# ========================
#       Time Cleaning
# ========================

def str_to_time(time_str):
    if 'AM' in time_str:
        time_str = time_str.replace('AM', '').strip()
        time_lst = time_str.split(sep = ':')
        hour = int(time_lst[0])
        if hour in [1, 2, 3, 4, 5, 6, 7]:
            hour += 12
        minute = int(time_lst[1])
        if len(time_lst) == 3:
            second = int(time_lst[2])
        else:
            second = 0            
            
    elif 'PM' in time_str:
       time_str = time_str.replace('PM', '').strip()
       time_lst = time_str.split(sep = ':')
       hour = int(time_lst[0])
       if hour in [1, 2, 3, 4, 5, 6, 7, 8]:
           hour += 12
       minute = int(time_lst[1])
       if len(time_lst) == 3:
           second = int(time_lst[2])  
       else:
           second = 0
           
    else:
        time_str = time_str.strip()
        try:
            hour = int(time_str.split(sep = ':')[0])
        except:
            hour = 1
        try:
            minute = int(time_str.split(sep = ':')[1])
        except:
            minute = 0
        second = 0
        if hour in [1, 2, 3, 4, 5, 6, 7]:
            hour += 12
    
    #time_time = time(hour, minute, second)
    time_str = str(hour) + ':' + str(minute) + ':' + str(second)
    t = datetime.strptime(time_str, "%H:%M:%S")

    return time_str, t
        

def time_cleaning(df, sort_col, time_col_lst):

    df.sort_values(by = sort_col, axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last', ignore_index=True)
    StartTime = time_col_lst[0]
    CompletionTime = time_col_lst[1]
    
    #Duration = time_col_lst[2]

    duration_lst = list()
    duration_int_lst = list()
    start_time_str_lst = list()
    end_time_str_lst = list()
    for i in range(df.shape[0]):
        if df[StartTime][i] == '0':
            df[StartTime][i] = df[CompletionTime][i-1]
        if df[CompletionTime][i] == '0':
            if i != df.shape[0] - 1:
                df[CompletionTime][i] = df[StartTime][i+1]
            
  
        start = df[StartTime][i]
        complete = df[CompletionTime][i]
        start_time_str, t1 = str_to_time(start)
        end_time_str, t2 = str_to_time(complete)
        
        start_time_str_lst.append(start_time_str)
        end_time_str_lst.append(end_time_str)
        
        duration = t2 - t1
        duration_str = str(duration)
        
        try:
            duration_int = int(duration_str.split(sep = ':')[0])*3600 + int(duration_str.split(sep = ':')[1])*60 + int(duration_str.split(sep = ':')[2])
        except:
            duration_int = 1200
            
        duration_int_lst.append(duration_int) 
        duration_lst.append(duration_str)
        
    df['NewStartTime']= start_time_str_lst
    df['NewCompletionTime'] = end_time_str_lst 
    df['NewDuration'] = duration_lst
    df['Duration_int'] = duration_int_lst
    
    return df

# ========================
#       Fill Day
# ========================
def fill_day(df, day_col, month_col, year_col):
    for i in range(df.shape[0]):
        if df[day_col][i] == '0':
            df[day_col][i] = df[day_col][i-1]
        if df[month_col][i] == '0':
            df[month_col][i] = df[month_col][i-1]
        if df[year_col][i] == '0':
            df[year_col][i] = df[year_col][i-1]
    return df

# ========================
# Date - Gregorian//Jalali
# ========================
persian_month_dict = {'فروردین':1,
                      'اردیبهشت':2,
                      'خرداد':3,
                      'تیر':4,
                      'مرداد':5,
                      'شهریور':6,
                      'مهر':7,
                      'آبان':8,
                      'آذر':9,
                      'دی':10,
                      'بهمن':11,
                      'اسفند':12
                      }
weekday_dict = {0: 'Sat', 1: 'Sun', 2: 'Mon', 3: 'Tue', 4: 'Wed', 5: 'Thu', 6: 'Fri'}

def persian_date(df, year_col, month_col, day_col):
    persian_date_lst = list()
    p_date_lst = list()
    weekday_lst = list()
    for i in range(df.shape[0]):
        day = int(df[day_col][i])
        month = persian_month_dict[df[month_col][i]]
        year = int(df[year_col][i])
        persian_date = jdatetime.date(year, month, day)
        weekday_code = persian_date.weekday()
        weekday = weekday_dict[weekday_code]
        persian_date_lst.append(str(persian_date))
        p_date_lst.append(persian_date)
        weekday_lst.append(weekday)
    df['Date'] = persian_date_lst
    df['WeekDay'] = weekday_lst
    df['PersianDate'] = p_date_lst     # use this column for your self

    return df

# ========================
#          Get Data
# ========================

def get_data(sheet, col_lst, base_col):
    records_lst = sheet.get_all_values()
    df = pd.DataFrame(records_lst, columns = col_lst)
    df.drop([0], axis = 0, inplace = True)
    df = df[df[base_col] != '']
    df.reset_index(drop = True, inplace = True)    
    return df

#connect to the service account
#gc = gspread.service_account(filename="C:/Users/ASUS/Desktop/WebjarCodes/GoogleSheetsPython/credentials.json")

# ========================
#         DataFrames
# ========================
def SEO_data():
    
    SEO_sheet = gc.open("گزارش هویج").get_worksheet(16)    
    cols_name = ['ID', 'Year', 'Month', 'Day', 'Person', 'Project', 'Task', 'SubTask',
             'Count', 'EstimateTime', 'StartTime', 'CompletionTime', 'Duration', 'Info']

    SEO_df = get_data(SEO_sheet, cols_name, 'Person')
    SEO_df.replace('', '0', inplace = True)
    
    SEO_df.dropna(axis = 0, subset = ['Person'], inplace = True)
    SEO_df.reset_index(drop = True, inplace = True)
    SEO_df_1 = fill_day(SEO_df, 'Day', 'Month', 'Year')
    SEO_df_2 = time_cleaning(SEO_df_1, ["Person", 'Day'], ['StartTime', 'CompletionTime', 'Duration'])
    SEO_df_3 = persian_date(SEO_df_2, 'Year', 'Month', 'Day')
    return SEO_df_3


def wordpress_data():
    
    wordpress_sheet = gc.open("word press").get_worksheet(0)    
    cols_name = ['Year', 'Month', 'Day', 'Person', 'Project', 'Task',
                 'StartTime', 'CompletionTime', 'Duration', 'Info']

    wordpress_df = get_data(wordpress_sheet, cols_name, 'Person')
    wordpress_df.replace('', '0', inplace = True)
    
    wordpress_df.dropna(axis = 0, subset = ['Person'], inplace = True)
    wordpress_df.reset_index(drop = True, inplace = True)
    wordpress_df_1 = fill_day(wordpress_df, 'Day', 'Month', 'Year')
    wordpress_df_2 = time_cleaning(wordpress_df_1, ["Person", 'Day'], ['StartTime', 'CompletionTime', 'Duration'])
    wordpress_df_3 = persian_date(wordpress_df_2, 'Year', 'Month', 'Day')
    return wordpress_df_3

def DOP_data():
    
    dop_sheet = gc.open("گزارش هویج").get_worksheet(18)  
    cols_name = ['ID', 'Year', 'Month', 'Day', 'Person', 'Project', 'Task', 'count', 'rush',
                 'StartTime', 'CompletionTime', 'Duration', 'Info']

    dop_df = get_data(dop_sheet, cols_name, 'Person')
    dop_df.replace('', '0', inplace = True)
    
    dop_df.dropna(axis = 0, subset = ['Person'], inplace = True)
    dop_df.reset_index(drop = True, inplace = True)
    dop_df_1 = fill_day(dop_df, 'Day', 'Month', 'Year')
    dop_df_2 = time_cleaning(dop_df_1, ["Person", 'Day'], ['StartTime', 'CompletionTime', 'Duration'])
    dop_df_3 = persian_date(dop_df_2, 'Year', 'Month', 'Day')
    return dop_df_3

def instagram_data():
    
    instagram_sheet = gc.open("گزارش هویج").get_worksheet(19)  
    cols_name = ['Year', 'Month', 'Day', 'Person', 'Project', 'Task', 'count',
                 'StartTime', 'CompletionTime', 'Duration', 'Info']

    instagram_df = get_data(instagram_sheet, cols_name, 'Person')
    instagram_df.replace('', '0', inplace = True)
    
    instagram_df.dropna(axis = 0, subset = ['Person'], inplace = True)
    instagram_df.reset_index(drop = True, inplace = True)
    instagram_df_1 = fill_day(instagram_df, 'Day', 'Month', 'Year')
    instagram_df.StartTime.replace('0', '9:00:00 AM')
    instagram_df.CompletionTime.replace('0', '8:00:00 PM')
    instagram_df_2 = time_cleaning(instagram_df_1, ["Person", 'Day'], ['StartTime', 'CompletionTime', 'Duration'])
    instagram_df_3 = persian_date(instagram_df_2, 'Year', 'Month', 'Day')
    return instagram_df_3

def shooting_data():
    
    shooting_sheet = gc.open("Havij Projects").get_worksheet(2)  
    cols_name = ['Date', 'Project', 'Operation', 'StartTime', 'CompletionTime', 'Duration', 'Team',
                 'Cameraman', 'Mobile', 'Camera', 'OSMO', 'Ronin', 'Light', 'OtherEquipment']

    shooting_df = get_data(shooting_sheet, cols_name, 'Project')
    shooting_df.replace('', '0', inplace = True)
    
    shooting_df.dropna(axis = 0, subset = ['Project'], inplace = True)
    shooting_df.reset_index(drop = True, inplace = True)

    return shooting_df

def projects_detail_data():
    projects_detail_sheet = gc.open('Havij Projects').get_worksheet(1)
    cols_name = ['Project', 'Plan', 'FirstPostDate', 'Reels', 'OtherPosts', 'TotalPosts', 'RemainingPosts', 
                 'Stories', 'RemainingStories', 'ActivityTime', 'RemainingActivityTime', 'CameramanTime',
                 'AdminTime', 'TotalShooting', 'Covers', 'Highlights', 'RemainingHighlights']
    projects_detail_df = get_data(projects_detail_sheet, cols_name, 'Project')
    for i in range(projects_detail_df.shape[0]):
        projects_detail_df.FirstPostDate[i] = projects_detail_df.FirstPostDate[i].replace('/', '-')
    projects_detail_df.replace('', '-', inplace = True)
    
    return projects_detail_df

def projects_data():
    projects_sheet = gc.open('Havij Projects').get_worksheet(0)
    cols_name = ['Project', 'Owner', 'PhoneNumber', 'ContractDate', 'Plan', 'InstagramPageID',
                 'Admin', 'InstagramPeriod', 'InstagramCost', 'SeoPeriod', 'SeoMonthlyCost',
                 'SeoTotalCost', 'SeoWords', 'TotalCost', 'Details']
    projects_df = get_data(projects_sheet, cols_name, 'Project')
    projects_df.drop(list(projects_df[projects_df['Project'] == 'فروشگاه ایرانیان'].index), axis = 0, inplace = True)
    projects_df.reset_index(drop = True, inplace = True)
    projects_df.drop('Details', axis = 1, inplace = True)
    for i in range(projects_df.shape[0]):
        projects_df.ContractDate[i] = '1402' + '-' + projects_df.ContractDate[i].replace('/', '-')
    
    return projects_df
        
# ======================================================
#                   Phase 1 - Request 1
# ======================================================
    
def date_project_filter(df, project, period_lst, cols_lst):
    if len(period_lst) == 1:
        df_date_filter = df[df['Date'] == period_lst[0]]
    else:
        start_date = period_lst[0]
        end_date = period_lst[1]
        df_date_filter1 = df[df['Date'] <= end_date]
        df_date_filter = df_date_filter1[df_date_filter1['Date'] >= start_date]
    df_project_filter = df_date_filter[df_date_filter['Project'] == project]
    
    df_filtered = df_project_filter[cols_lst]
    return df_filtered
    
def request_1(project, period_lst):
# ----------------------------- SEO Section

    st.header('SEO')
    SEO_df = SEO_data()
    SEO_df_filtered = date_project_filter(SEO_df, project, period_lst, cols_lst=['Person', 'Task', 'SubTask', 'Date', 'NewDuration'])
    SEO_df_filtered.sort_values(by='Date', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last', ignore_index=True, key=None)
    if SEO_df_filtered.empty:
        st.markdown('There is no information to show!')
    else:
        st.dataframe(SEO_df_filtered, hide_index = True, width = 700)
# ----------------------------- WordPress Section

    st.header('WordPress')
    wordpress_df = wordpress_data()
    wordpress_df_filtered = date_project_filter(wordpress_df, project, period_lst, cols_lst=['Person', 'Task', 'Date', 'NewDuration', 'Info'])
    wordpress_df_filtered.sort_values(by='Date', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last', ignore_index=True, key=None)   
    if wordpress_df_filtered.empty:
        st.markdown('There is no information to show!')
    else:
        st.dataframe(wordpress_df_filtered, hide_index = True, width = 700)
# ----------------------------- DOP Section

    st.header('DOP')
    dop_df = DOP_data()
    dop_df_filtered = date_project_filter(dop_df, project, period_lst, cols_lst=['Person', 'Task', 'Date', 'StartTime', 'CompletionTime', 'NewDuration', 'Info'])
    dop_df_filtered.sort_values(by='Date', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last', ignore_index=True, key=None)
    if dop_df_filtered.empty:
        st.markdown('There is no information to show!')
    else:
        st.dataframe(dop_df_filtered, hide_index = True, width = 700) 
# ----------------------------- Instagram Section

    st.header('Instagram')
    instagram_df = instagram_data()
    instagram_df_filtered = date_project_filter(instagram_df, project, period_lst, cols_lst=['Person', 'Task', 'Date', 'StartTime', 'CompletionTime', 'NewDuration', 'Info'])
    instagram_df_filtered.sort_values(by='Date', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last', ignore_index=True, key=None)
    if instagram_df_filtered.empty:
        st.markdown('There is no information to show!')
    else:
        st.dataframe(instagram_df_filtered, hide_index = True, width = 700)
# ----------------------------- Shooting Section

    st.header('Shooting')
    shooting_df = shooting_data()
    shooting_df_filtered = date_project_filter(shooting_df, project, period_lst, cols_lst=['Date', 'Project', 'StartTime', 'CompletionTime', 'Duration', 'Team', 'Mobile', 'Camera', 'OSMO', 'Ronin', 'Light'])
    shooting_df_filtered.sort_values(by='Date', axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last', ignore_index=True, key=None)
    if shooting_df_filtered.empty:
        st.markdown('There is no information to show!')
    else:
        st.dataframe(shooting_df_filtered, hide_index = True, width = 700) 
        
    return

# ======================================================
#                   Phase 1 - Request 2
# ======================================================

def request_2(project):
    
    projects_detail_df = projects_detail_data()
    projects_detail_df_filtered = projects_detail_df[projects_detail_df.Project == project]
    projects_detail_df_filtered.reset_index(drop = True, inplace = True) 
        
    projects_df = projects_data()
    projects_df_filtered = projects_df[projects_df.Project == project]
    projects_df_filtered.reset_index(drop = True, inplace = True) 
    
    cols_3 = st.columns(2)
    with cols_3[0]:
        st.write('Contract Date: ', projects_df_filtered.ContractDate[0])
        st.write('First Post Date: ', projects_detail_df_filtered.FirstPostDate[0])
    with cols_3[1]:
        st.write('Contract Duration: ', str(projects_df_filtered.InstagramPeriod[0]) + ' Month')
        st.write('Plan: ', projects_df_filtered.Plan[0])

    full_data_option = st.radio(label = 'Wanna See Full Information?', options = ['No', 'Yes'])
    if full_data_option == 'Yes':
        st.markdown('Contract Data:')
        st.dataframe(projects_df_filtered, hide_index = True, width = 700) 
        st.markdown('Project Status Data:')
        st.dataframe(projects_detail_df_filtered, hide_index = True, width = 700) 
    
    return
    

# ======================================================
#                    Streamlit
# ======================================================
projects_lst = ['چرمینه' ,'کلینیک ماه ملورین', 'کلینیک ماری', 'کلینیک رازی', 'کلینیک رادین', 'اسمارت کیدز', 'هویج' ,'وبجار' 
               ,'اورنگ 🐥' ,'بونسای','شاه نهمت اللهی', 'عطاحیدری' ,'کلینیک آذین', 'کلینیک ارغوان', 'شایما' ,'دکتر مهرابی', 'کلینیک پریا'
                , 'ماهان اسپرسو','اوصیا','هنرمند','کلینیک اوتانا' , 'حس خوب زندگی', 'اعتمادبار' ,'دکوچی دیزاین', 'تابلوسازی' ,'کلینیک لادن', 'پرتوبازار', 'سیتی فون', 'مسافرت کجا'
                , 'معلولان ذهنی', 'دکیمون' ,'نقره چی', 'قالی و قالیچه', 'حسابداری' ]
projects_lst_2 = ['چرمینه' ,'کلینیک ماه ملورین', 'کلینیک ماری', 'کلینیک رازی', 'کلینیک رادین', 'اسمارت کیدز', 'هویج' ,'وبجار' 
               ,'اورنگ 🐥' ,'بونسای','شاه نهمت اللهی', 'عطاحیدری' ,'کلینیک آذین', 'کلینیک ارغوان', 'شایما' ,'دکتر مهرابی', 'کلینیک پریا'
                , 'ماهان اسپرسو','کلینیک اوتانا' , 'حس خوب زندگی']


user_dict = {'AydaKSH': '241178', 'SepehrT': 'Webjar123'}
cols_1 = st.columns(2)
username = cols_1[0].text_input('username')
password = cols_1[1].text_input('password')

if username in user_dict.keys():
#if True:
    if user_dict[username] == password:
    #if True:
        st.markdown('welcome')
        cred_file = st.file_uploader('Upload Credentials.json File')
        if cred_file is not None:
        #if True:
            cred_dict = json.load(cred_file)
            gc = gspread.service_account_from_dict(cred_dict)
            date_option = st.radio(label = 'please select one option', options = ['Period', 'Just 1 Day'])
            if date_option == 'Period':
                cols_2 = st.columns(2)
                start_date = cols_2[0].text_input('Please Enter the Start Date, format yyyy-mm-dd')
                end_date = cols_2[1].text_input('Please Enter the End Date, format yyyy-mm-dd')
                period_lst = [start_date, end_date]
            else:
                single_date = st.text_input('Please Enter the Date, format yyyy-mm-dd')
                period_lst = [single_date]
            project_option = st.selectbox('Select Your Desired Project', projects_lst)
            
            request_1(project = project_option, period_lst = period_lst)
            # ----------------------- Request 2
            st.divider()
            st.title('ProjectsDetail')
            project_option_2 = st.selectbox('Please Select a Project', projects_lst_2)
            request_2(project_option_2)
            
            st.divider()
            projects_detail_df = projects_detail_data()
            projects_df = projects_data()
            bullet_chart(projects_detail_df, projects_df,project_option_2)
            
            
    else:
        st.markdown('password is wrong')
else:
    st.markdown('you are not allowed')


