import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Baca data dari file CSV
data = pd.read_csv('D:/Bangkit/submission-ruth/data/hour.csv')

# Konversi kolom 'tanggal' menjadi tipe data datetime
data['tanggal'] = pd.to_datetime(data['dteday'])

# Sidebar untuk memilih tahun
st.sidebar.header('Pilih Tahun')
tahun = st.sidebar.selectbox('Tahun:', ['2011', '2012'])

if tahun == '2011':
    # Filter data untuk tahun 2011
    data_selected = data[data['tanggal'].dt.year == 2011]
    st.write("Korelasi untuk Tahun 2011:")
    st.set_option('deprecation.showPyplotGlobalUse', False)
else:
    # Filter data untuk tahun 2012
    data_selected = data[data['tanggal'].dt.year == 2012]
    st.write("Korelasi untuk Tahun 2012:")

# Hitung korelasi antara cuaca (weathersit) dengan tingkat keterlibatan pengguna sepeda (casual dan registered)
correlation = data_selected[['weathersit', 'casual', 'registered']].corr()

# Visualisasi korelasi menggunakan heatmap
plt.figure(figsize=(8, 6))
plt.title('Heatmap Korelasi Antara Cuaca dan Tingkat Keterlibatan Pengguna Sepeda (Tahun {})'.format(tahun))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
st.pyplot()

# Tampilkan dataframe jika dipilih
if st.checkbox('Tampilkan Dataframe Korelasi'):
    st.write(data_selected)

# Menghitung total peminjaman sepeda per hari
daily_rentals = data.groupby('dteday')[['casual', 'registered', 'cnt']].sum().reset_index()

# Menggabungkan data hari dengan data jam
merged_df = pd.merge(data, daily_rentals, on='dteday', suffixes=('_hour', '_day'))

# Membuat kolom baru untuk menandai apakah hari tersebut merupakan hari kerja atau hari libur
merged_df['is_workday'] = merged_df['workingday'].apply(lambda x: 'Workday' if x == 1 else 'Holiday')

# Menghitung total peminjaman sepeda per jam berdasarkan jenis hari
hourly_rentals_by_daytype = merged_df.groupby(['hr', 'is_workday'])[['casual_hour', 'registered_hour', 'cnt_hour']].mean().reset_index()

# Plot perbandingan penggunaan sepeda antara hari kerja dan hari libur
plt.figure(figsize=(10, 6))

for day_type in ['Workday', 'Holiday']:
    data = hourly_rentals_by_daytype[hourly_rentals_by_daytype['is_workday'] == day_type]
    plt.plot(data['hr'].values, data['cnt_hour'].values, label=day_type)

plt.xlabel('Hour')
plt.ylabel('Average Count of Rentals')
plt.title('Comparison of Bike Usage between Workdays and Holidays')
plt.legend()
plt.grid(True)

# Menampilkan plot menggunakan Streamlit
st.pyplot()

# Tampilkan dataframe jika dipilih
if st.checkbox('Tampilkan Dataframe Perbandingan'):
    st.write(hourly_rentals_by_daytype)
