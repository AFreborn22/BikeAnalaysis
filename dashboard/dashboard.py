import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
day_data = pd.read_csv('day.csv')
hour_data = pd.read_csv('hourNew.csv')

# Title and introduction
st.title("Bike Sharing Data Dashboard")
st.write("""
Dashboard ini menunjukkan hasil analisis faktor-faktor yang mempengaruhi penyewaan sepeda harian 
dan pola penyewaan berdasarkan kondisi cuaca.
""")

# Menampilkan informasi dataset
st.header("Informasi Dataset")
st.write(f"Jumlah data harian: {day_data.shape[0]}")
st.write(f"Jumlah data per jam: {hour_data.shape[0]}")

# Filter by season
season = st.selectbox('Pilih Musim:', ['Semua', 'Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])

if season != 'Semua':
    if season == 'Musim Semi':
        filtered_data = day_data[day_data['season'] == 1]
    elif season == 'Musim Panas':
        filtered_data = day_data[day_data['season'] == 2]
    elif season == 'Musim Gugur':
        filtered_data = day_data[day_data['season'] == 3]
    else:
        filtered_data = day_data[day_data['season'] == 4]
else:
    filtered_data = day_data

st.write(f"Menampilkan data untuk: {season}")
st.dataframe(filtered_data)

# Visualisasi: Pengaruh suhu terhadap penyewaan sepeda
st.header("Pengaruh Suhu terhadap Penyewaan Sepeda")
fig, ax = plt.subplots()
ax.scatter(filtered_data['temp'], filtered_data['cnt'], alpha=0.5)
ax.set_xlabel('Suhu (normalized)')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_title('Pengaruh Suhu terhadap Penyewaan Sepeda')
plt.xticks(rotation=45, ha='right') 
st.pyplot(fig)

# Menampilkan analisis dan visualisasi berdasarkan Hari 
st.header("Penyewaan Sepeda Berdasarkan Hari Kerja / Libur")
fig, ax = plt.subplots()
ax.bar(day_data['hari'], day_data['cnt'], color='y')  
ax.set_xlabel('hari Kerja /Libur')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_title('Pola Penyewaan Sepeda berdasarkan Hari Kerja / Libur')
st.pyplot(fig)

# Menampilkan analisis dan visualisasi berdasarkan Hari 
st.header("Penyewaan Sepeda Berdasarkan Hari ")
fig, ax = plt.subplots()
ax.bar(day_data['day'], day_data['cnt'], color='y')  
ax.set_xlabel('hari')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_title('Pola Penyewaan Sepeda berdasarkan Hari')
st.pyplot(fig)

# Menampilkan analisis dan visualisasi berdasarkan Waktu
st.header("Penyewaan Sepeda Berdasarkan Waktu")
fig, ax = plt.subplots()
ax.bar(hour_data['waktu'], hour_data['cnt'], color='y')  
ax.set_xlabel('Waktu')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_title('Pola Penyewaan Sepeda berdasarkan Waktu')
st.pyplot(fig)

# Menampilkan analisis dan visualisasi berdasarkan cuaca
st.header("Penyewaan Sepeda Berdasarkan Cuaca")
fig, ax = plt.subplots()
ax.bar(hour_data['weather'], hour_data['cnt'], color='y')  
ax.set_xlabel('Cuaca')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_title('Pola Penyewaan Sepeda berdasarkan Cuaca')
st.pyplot(fig)

# Menampilkan analisis dan visualisasi berdasarkan Musim
st.header("Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots()
ax.bar(day_data['musim'], day_data['cnt'], color='y')  
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_title('Pola Penyewaan Sepeda berdasarkan Musim')
st.pyplot(fig)  

# Kesimpulan
st.header("Kesimpulan")
st.write("""
- Faktor utama yang mempengaruhi jumlah penyewaan sepeda harian adalah suhu. Semakin tinggi suhu, semakin banyak jumlah penyewaan sepeda.
- Cuaca yang cerah atau sedikit berawan meningkatkan jumlah penyewaan, terutama pada sore hari.
- Pengguna terdaftar cenderung menyewa sepeda di pagi dan sore hari, sedangkan pengguna kasual lebih banyak menyewa sepeda di sore hari ketika suhu lebih tinggi.
""")

# Rekomendasi
st.header("Rekomendasi")
st.write("""
- Fokus promosi pada waktu sore dengan suhu yang lebih tinggi, terutama bagi pengguna tidak terdaftar.
- Pertimbangkan untuk memberikan insentif atau diskon pada hari-hari dengan kelembapan tinggi atau cuaca buruk untuk meningkatkan penyewaan pada kondisi tersebut.
""")
