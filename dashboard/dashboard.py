import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
from datetime import time

# Load berkas data
day_df = pd.read_csv(
    "https://raw.githubusercontent.com/ard22001/bike-sharing-analysis-project/refs/heads/main/data/day_df.csv"
)
hour_df = pd.read_csv(
    "https://raw.githubusercontent.com/ard22001/bike-sharing-analysis-project/refs/heads/main/data/hour_df.csv"
)

# Memastikan kolom 'dteday' bertipe datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df['hr'] = pd.to_datetime(hour_df['hr'], format='%H').dt.time


# Membuat helper functions
## Total per Tahun
def create_yearly_df(df):
    year_df = df.groupby('yr').agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum'
    }).reset_index()

    base_year = 2011
    year_df['yr'] = pd.to_datetime(year_df['yr'] + base_year,
                                   format='%Y').dt.year

    return year_df


## Penggunaan Bike Sharing Bulanan
def create_monthly_df(df):
    monthly_df = df.resample(rule='ME', on='dteday').agg({
        'casual': 'mean',
        'registered': 'mean',
        "cnt": "mean"
    })
    monthly_df.index = monthly_df.index.strftime('%Y-%m')
    monthly_df = monthly_df.reset_index()
    monthly_df.rename(columns={
        'dteday': "year-month",
        "cnt": "count"
    },
                      inplace=True)
    return monthly_df


## Penggunaan Bike Sharing Harian
def create_daily_df(df):
    daily_df = df.groupby('dteday').agg({
        'casual': 'sum',
        'registered': 'sum',
        "cnt": "sum"
    }).reset_index()
    return daily_df


## Penggunaan Bike Sharing Tiap Jam
def create_hourly_df(df):
    hr_df = df.groupby(by='hr').agg({
        'casual': 'mean',
        'registered': 'mean',
        'cnt': 'mean'
    })
    return hr_df


## Berdasarkan Musim
def create_season_df(df):
    season_df = df.groupby(by='season').agg({
        'casual': 'mean',
        'registered': 'mean',
        'cnt': 'mean'
    })
    season_df = season_df.rename(index={
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    })
    return season_df


## Berdasarkan Holiday/Not
def create_holiday_df(df):
    holiday_df = df.groupby(by='holiday').agg({
        'casual': 'mean',
        'registered': 'mean',
        'cnt': 'mean'
    })
    return holiday_df


## Berdasarkan Hari ke-
def create_weekday_df(df):
    weekday_df = df.groupby(by='weekday').agg({
        'casual': 'mean',
        'registered': 'mean',
        'cnt': 'mean'
    })
    return weekday_df


## Berdasarkan Cuaca
def create_weather_df(df):
    weather_df = df.groupby('weathersit').agg({
        'registered': 'mean',
        'casual': 'mean'
    }).reset_index().rename(columns={
        'registered': 'Registered',
        'casual': 'Casual'
    })
    return weather_df


# Membuat Komponen Filter
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

time_options = [time(h, 0) for h in range(24)]

with st.sidebar:
    # Judul
    st.title(':bike: Bike Sharing Analysis Dashboard')
    # Tahun

    # Bulan
    # Tanggal
    start_date, end_date = pd.to_datetime(
        st.date_input(label='Rentang Tanggal',
                      min_value=min_date,
                      max_value=max_date,
                      value=[min_date, max_date]))
    # Jam
    start_hour, end_hour = st.select_slider("Rentang Jam",
                                            options=time_options,
                                            value=(time_options[0],
                                                   time_options[1]))

# Filter dataframe berdasarkan tanggal
main_day_df = day_df[(day_df["dteday"] >= start_date)
                     & (day_df["dteday"] <= end_date)]
# Filter dataframe berdasarkan jam
main_hr_df = hour_df[(hour_df["hr"] >= start_hour)
                     & (hour_df["hr"] <= end_hour)]

# Berbagai dataframe untuk visualisasi
yearly_df = create_yearly_df(day_df)
monthly_df = create_monthly_df(main_day_df)
daily_df = create_daily_df(main_day_df)
hourly_df = create_hourly_df(main_hr_df)
season_df = create_season_df(day_df)
holiday_df = create_holiday_df(day_df)
weekday_df = create_weekday_df(main_day_df)
weather_df = create_weather_df(day_df)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header(':bike: Bike Sharing Analysis Dashboard :bike:')

# Informasi Umum
## Total Sewa
st.subheader('Total Sewa')
col1, col2 = st.columns(2, vertical_alignment="top", border=True)

### Tahun 2011
with col1:
    total_rents_11 = yearly_df[yearly_df['yr'] == 2011]['cnt'].sum()
    st.metric(r'$\textsf{\large Tahun 2011 }$', value=f"{total_rents_11:,}")

    # Casual & Registered
    left, right = st.columns(2)

    with left:
        reg_11 = yearly_df[yearly_df['yr'] == 2011]['registered'].sum()
        st.metric(r'$\textsf{\small Registered }$', value=f"{reg_11:,}")
    with right:
        cas_11 = yearly_df[yearly_df['yr'] == 2011]['casual'].sum()
        st.metric(r'$\textsf{\small Casual }$', value=f"{cas_11:,}")

### Tahun 2012
with col2:
    total_rents_12 = yearly_df[yearly_df['yr'] == 2012]['cnt'].sum()
    st.metric(r'$\textsf{\large Tahun 2012 }$', value=f"{total_rents_12:,}")

    # Casual & Registered
    left, right = st.columns(2)

    with left:
        reg_12 = yearly_df[yearly_df['yr'] == 2012]['registered'].sum()
        st.metric(r'$\textsf{\small Registered }$', value=f"{reg_12:,}")

    with right:
        cas_12 = yearly_df[yearly_df['yr'] == 2012]['casual'].sum()
        st.metric(r'$\textsf{\small Casual }$', value=f"{cas_12:,}")

st.divider()

## Rata-Rata Sewa Harian
st.subheader('Rata-Rata Sewa Harian')
# Casual & Registered
col1, col2 = st.columns([1, 3])

with col1:
    reg = round(daily_df['registered'].mean())
    st.metric(r'$\textsf{\small Registered }$', value=f"{reg:,}")

    cas = round(daily_df['casual'].mean())
    st.metric(r'$\textsf{\small Casual }$', value=f"{cas:,}")

# Tabs
tab1, tab2, tab3 = st.tabs(["Tren Sewaan", "Pola Pengguna", 'Jam-Jam Sibuk'])

with tab1:
    # Tren Bulanan
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=monthly_df,
                 x='year-month',
                 y='registered',
                 label='Pengguna Registered',
                 color='#69aae9')
    sns.lineplot(data=monthly_df,
                 x='year-month',
                 y='casual',
                 label='Pengguna Casual',
                 color='#3fa931')

    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='x', rotation=45)
    ax.legend(frameon=0)

    st.pyplot(fig)

with tab1:
    # Tren Harian
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(daily_df['dteday'],
            daily_df['registered'],
            label='Pengguna Registered',
            color='#3187a9')
    ax.plot(daily_df['dteday'],
            daily_df['casual'],
            label='Pengguna Casual',
            color='#3fa931')

    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.legend(frameon=0)

    st.pyplot(fig)

with tab2:
    st.subheader('Berdasarkan Hari dan Jam Tertentu')
    hr_reg_df = hourly_df.reset_index().drop(columns=['cnt', 'casual'])
    hr_reg_df['hr'] = hr_reg_df['hr'].apply(lambda x: x.hour)
    hr_cas_df = hourly_df.reset_index().drop(columns=['cnt', 'registered'])
    hr_cas_df['hr'] = hr_cas_df['hr'].apply(lambda x: x.hour)

    hari = {
        0: "Minggu",
        1: "Senin",
        2: "Selasa",
        3: "Rabu",
        4: "Kamis",
        5: "Jumat",
        6: "Sabtu"
    }
    wd_reg_df = weekday_df.reset_index().drop(columns=['cnt', 'casual'])
    wd_reg_df = wd_reg_df.replace({"weekday": hari})
    wd_cas_df = weekday_df.reset_index().drop(columns=['cnt', 'registered'])

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

    sns.lineplot(x=wd_reg_df['weekday'],
                 y=wd_reg_df['registered'],
                 label='Pengguna Registered',
                 color='#3187a9',
                 linewidth=2,
                 ax=ax[0])

    sns.lineplot(x=wd_cas_df['weekday'],
                 y=wd_cas_df['casual'],
                 label='Pengguna Casual',
                 color='#3fa931',
                 linewidth=2,
                 ax=ax[0])

    ax[0].set_title('Berdasarkan Hari', size=15, y=1.03)
    ax[0].set_xlabel('Hari', fontsize=12)
    ax[0].set_ylabel(None)
    ax[0].set_xticks(range(0, 7))
    ax[0].legend().remove()
    ax[0].grid(True, alpha=0.4)

    sns.lineplot(x=hr_reg_df['hr'],
                 y=hr_reg_df['registered'],
                 label='Pengguna Registered',
                 color='#3187a9',
                 linewidth=2,
                 ax=ax[1])

    sns.lineplot(x=hr_cas_df['hr'],
                 y=hr_cas_df['casual'],
                 label='Pengguna Casual',
                 color='#3fa931',
                 linewidth=2,
                 ax=ax[1])

    ax[1].set_title('Berdasarkan Jam', size=15, y=1.03)
    ax[1].set_xlabel('Jam ke-', fontsize=12)
    ax[1].set_ylabel(None)
    ax[1].set_xticks(range(0, 24))
    ax[1].legend().remove()
    ax[1].grid(True, alpha=0.4)

    handles, labels = ax[1].get_legend_handles_labels()
    fig.legend(handles,
               labels,
               loc='upper center',
               bbox_to_anchor=(0.5, 1.10),
               ncol=1,
               fontsize=13,
               frameon=0)

    st.pyplot(fig)
with tab2:
    st.subheader('Berdasarkan Cuaca')
    weather_melt = weather_df.melt(id_vars='weathersit',
                                   var_name='user_type',
                                   value_name='count')

    weather_labels = {
        1: "Cerah / Sedikit Berawan",
        2: "Berawan / Berkabut",
        3: "Hujan / Salju Ringan",
        4: "Hujan Lebat / Salju Tebal"
    }
    weather_melt['weathersit'] = weather_melt['weathersit'].map(weather_labels)

    fig, ax = plt.subplots(figsize=(10, 4.5))

    sns.barplot(data=weather_melt,
                x='weathersit',
                y='count',
                hue='user_type',
                palette=['#3187a9', '#3fa931'],
                edgecolor='white',
                linewidth=1)

    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.legend(frameon=0)

    st.pyplot(fig)

with tab2:
    st.subheader('Berdasarkan Musim')
    col1, col2 = st.columns(2)
    season = ["Spring", "Summer", "Fall", "Winter"]
    reg = season_df['registered']
    cas = season_df['casual']

    colors1 = ["#4CAF50", "#FFB400", "#FF5733", "#4682B4"]
    colors2 = ["#6DBE45", "#F5C63C", "#E85D04", "#537895"]
    explode = [0, 0, 0.05, 0]

    with col1:
        st.write(r'$\textsf{\large Registered }$')

        fig, ax = plt.subplots(figsize=(2.2, 2.2))
        ax.pie(reg,
               labels=season,
               autopct='%1.1f%%',
               colors=colors1,
               explode=explode,
               textprops={'fontsize': 7})
        st.pyplot(fig)

    with col2:
        st.write(r'$\textsf{\large Casual }$')
        fig, ax = plt.subplots(figsize=(2.2, 2.2))

        ax.pie(cas,
               labels=season,
               autopct='%1.1f%%',
               colors=colors2,
               explode=explode,
               textprops={'fontsize': 7})

        st.pyplot(fig)

with tab2:
    st.subheader('Berdasarkan Holiday/Bukan')
    col1, col2 = st.columns(2)

    labels = ["Bukan Holiday", "Holiday"]
    reg = holiday_df['registered']
    cas = holiday_df['casual']

    colors1 = ['#3187a9', '#7fc1db']
    colors2 = ['#8ecb86', '#3fa931']

    with col1:
        st.write(r'$\textsf{\large Registered }$')

        fig, ax = plt.subplots(figsize=(2.2, 2.2))
        ax.pie(reg,
               labels=labels,
               autopct='%1.1f%%',
               colors=colors1,
               textprops={'fontsize': 7})
        st.pyplot(fig)

    with col2:
        st.write(r'$\textsf{\large Casual }$')
        fig, ax = plt.subplots(figsize=(2.2, 2.2))

        ax.pie(cas,
               labels=labels,
               autopct='%1.1f%%',
               colors=colors2,
               startangle=180,
               textprops={'fontsize': 7})

        st.pyplot(fig)

with tab3:
    hr_data = hourly_df[['cnt']]
    labels = ['Sepi', 'Normal', 'Sibuk']
    hr_data['cnt_category'] = pd.qcut(hr_data['cnt'],
                                      q=[0, 0.33, 0.66, 1],
                                      labels=labels)

    hr_data.sort_values(by='cnt', ascending=False).head()

    fig, ax = plt.subplots(figsize=(15, 5))
    colors = ["#17b11d", "#f1b123", "#f13e23"]

    sns.barplot(x="hr",
                y="cnt",
                data=hr_data,
                palette=colors,
                hue='cnt_category',
                width=0.8)

    ax.set_xlabel("Jam ke-")
    ax.set_xticks(range(0, 24))
    ax.set_xticklabels(range(0, 24))
    ax.legend(loc="upper right", bbox_to_anchor=(1.11, 1), frameon=False)
    ax.set_ylabel("")  # Hilangkan label sumbu Y agar lebih bersih

    st.pyplot(fig)
