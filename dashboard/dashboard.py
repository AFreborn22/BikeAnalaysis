import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Load the dataset
day = pd.read_csv('dashboard/dayNew.csv')
hour = pd.read_csv('dashboard/hourNew.csv')
summaryWork = day.groupby('workingdayDesc').sum().reset_index()
summarySeason = day.groupby('seasonDesc').sum().reset_index()
summaryWeather = day.groupby('weathersitDesc').sum().reset_index()
summaryHour = hour.groupby('waktu').agg({
    'cnt': 'sum',
    'registered': 'sum',
    'casual': 'sum'
}).reset_index()


# Title and description
st.title("Dashboard Analisis Penyewaan Sepeda")
st.markdown("""
Dashboard ini menampilkan berbagai **insight** penting dari data penyewaan sepeda. Setiap visualisasi menjelaskan faktor-faktor yang mempengaruhi penyewaan sepeda, termasuk:
- **Pengaruh cuaca dan waktu** terhadap jumlah penyewaan.
- **Distribusi penyewaan** berdasarkan kelembapan, suhu, musim, dan kondisi cuaca.
- **Jumlah penyewaan** pada hari kerja dan hari libur.
- **Pola penyewaan sepeda** berdasarkan waktu dalam sehari.
- **Analisis cluster** yang memvisualisasikan pola penyewaan dalam kelompok yang berbeda.
Pilih salah satu **insight** di panel samping untuk melihat visualisasinya secara detail.
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Pilih Insight", 
    (
        "Pengaruh Cuaca & Waktu", 
        "Distribusi Penyewaan Berdasarkan Kelembapan", 
        "Distribusi Penyewaan Berdasarkan Suhu", 
        "Jumlah Penyewaan Hari Kerja vs Libur", 
        "Distribusi Berdasarkan Musim", 
        "Distribusi Berdasarkan Kondisi Cuaca", 
        "Cluster Analysis",
        "Pola Penyewaan Sepeda Berdasarkan Waktu"
    )
)

# Display insight based on selection
if option == "Pengaruh Cuaca & Waktu":
    st.header("Pengaruh Suhu terhadap Jumlah Penyewaan Sepeda")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(data=day, x='temp', y='cnt', label='Jumlah Penyewaan', ax=ax)
    sns.lineplot(data=day, x='temp', y='cnt', estimator='mean', color='red', label='Rata-rata Penyewaan', ax=ax)
    ax.set_title('Pengaruh Suhu terhadap Jumlah Penyewaan Sepeda')
    ax.set_xlabel('Suhu (Normalisasi)')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.legend()
    st.pyplot(fig)

    st.markdown("""
    **Penjelasan**: Visualisasi ini menunjukkan bagaimana suhu mempengaruhi jumlah penyewaan sepeda. Semakin hangat suhu, semakin tinggi jumlah penyewaan sepeda, namun ada batasan dimana suhu terlalu panas dapat menurunkan penyewaan.
    """)

elif option == "Distribusi Penyewaan Berdasarkan Kelembapan":
    st.header("Distribusi Penyewaan Sepeda Berdasarkan Kelembapan")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=day, x='hum_category', y='cnt', palette='viridis', ax=ax)
    ax.set_title('Distribusi Penyewaan Sepeda Berdasarkan Kelembapan')
    ax.set_xlabel('Kelembapan')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

    st.markdown("""
    **Penjelasan**: Distribusi ini menunjukkan bahwa tingkat kelembapan yang lebih tinggi sedikit menurunkan jumlah penyewaan sepeda, sedangkan pada kelembapan rendah hingga sedang penyewaan lebih tinggi.
    """)

elif option == "Distribusi Penyewaan Berdasarkan Suhu":
    st.header("Distribusi Penyewaan Sepeda Berdasarkan Suhu")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=day, x='temp_category', y='cnt', palette='viridis', ax=ax)
    ax.set_title('Distribusi Penyewaan Sepeda Berdasarkan Suhu')
    ax.set_xlabel('Suhu')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

    st.markdown("""
    **Penjelasan**: Penyewaan sepeda lebih tinggi saat suhu sedang dan menurun pada suhu ekstrem (sangat dingin atau sangat panas).
    """)

elif option == "Jumlah Penyewaan Hari Kerja vs Libur":
    st.header("Jumlah Penyewaan pada Hari Kerja dan Hari Libur")
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(summaryWork['cnt'], labels=summaryWork['workingdayDesc'], autopct='%1.1f%%', startangle=90, explode=[0.1, 0.0])
    ax.set_title('Jumlah Penyewaan pada Hari Kerja dan Hari Libur')
    ax.axis('equal')
    st.pyplot(fig)

    st.markdown("""
    **Penjelasan**: Grafik pie ini menunjukkan perbandingan penyewaan sepeda pada hari kerja dan hari libur. Terlihat bahwa jumlah penyewaan sepeda cenderung lebih tinggi pada hari libur dibandingkan hari kerja.
    """)

elif option == "Distribusi Berdasarkan Musim":
    st.header("Distribusi Penyewaan Sepeda Berdasarkan Musim")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=summarySeason, x='seasonDesc', y='cnt', palette='viridis', ax=ax)
    ax.set_title('Distribusi Penyewaan Sepeda Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

    st.header("Jumlah Penyewaan pada berbagai Musim")
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(summarySeason['cnt'], labels=summarySeason['seasonDesc'], autopct='%1.1f%%', startangle=90, explode=[0.0, 0.0, 0.0, 0.1])
    ax.set_title('Jumlah Penyewaan pada berbagai Musim')
    ax.axis('equal')
    st.pyplot(fig)

    st.markdown("""
    **Penjelasan**: Visualisasi ini menunjukkan penyewaan sepeda lebih tinggi pada musim tertentu, terutama di musim yang lebih hangat.
    """)

elif option == "Distribusi Berdasarkan Kondisi Cuaca":
    st.header("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=summaryWeather, x='weathersitDesc', y='cnt', palette='viridis', ax=ax)
    ax.set_title('Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

    st.header("Jumlah Penyewaan pada berbagai Kondisi Cuaca")
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(summaryWeather['cnt'], labels=summaryWeather['weathersitDesc'], autopct='%1.1f%%', startangle=90, explode=[0.0, 0.1, 0.0])
    ax.set_title('Jumlah Penyewaan pada berbagai Kondisi Cuaca')
    ax.axis('equal')
    st.pyplot(fig)

    st.markdown("""
    **Penjelasan**: Grafik ini menunjukkan penyewaan sepeda pada berbagai kondisi cuaca, di mana cuaca cerah mendorong lebih banyak penyewaan dibandingkan cuaca buruk seperti hujan atau kabut.
    """)

elif option == "Cluster Analysis":
    st.header("Analisis Cluster Penyewaan Sepeda")
    
    # Applying KMeans clustering
    features = day[['temp', 'hum', 'windspeed', 'weathersit', 'season', 'workingday', 'cnt']]
    kmeans = KMeans(n_clusters=2, random_state=42)
    clusters = kmeans.fit_predict(features)
    day['cluster'] = clusters

    # Reducing dimensions for visualization
    pca = PCA(n_components=3)
    pca_features = pca.fit_transform(features)

    # Creating a DataFrame for PCA results
    pca_df = pd.DataFrame(pca_features, columns=['PC1', 'PC2', 'PC3'])
    pca_df['cluster'] = clusters

    # 3D scatter plot using matplotlib
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pca_df[pca_df['cluster'] == 0]['PC1'], pca_df[pca_df['cluster'] == 0]['PC2'], pca_df[pca_df['cluster'] == 0]['PC3'], c='b', label='Cluster 0', alpha=0.6)
    ax.scatter(pca_df[pca_df['cluster'] == 1]['PC1'], pca_df[pca_df['cluster'] == 1]['PC2'], pca_df[pca_df['cluster'] == 1]['PC3'], c='r', label='Cluster 1', alpha=0.6)
    ax.set_title('Visualisasi 3D Cluster Penyewaan Sepeda')
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    ax.legend()
    st.pyplot(fig)

    st.markdown("""
    **Penjelasan**: Analisis cluster ini mengelompokkan data penyewaan sepeda berdasarkan faktor seperti suhu, kelembapan, dan kondisi cuaca. Cluster 0 menunjukkan penurunan penyewaan pada suhu dingin, sedangkan Cluster 1 menunjukkan peningkatan penyewaan pada suhu hangat.
    """)

elif option == "Pola Penyewaan Sepeda Berdasarkan Waktu":  
    st.header("Pola Penyewaan Sepeda berdasarkan Waktu")
    
    # Barplot untuk penyewaan berdasarkan waktu
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=summaryHour, x='waktu', y='cnt', palette='viridis', ax=ax)
    ax.set_title('Pola Penyewaan Sepeda berdasarkan Jam')
    ax.set_xlabel('Waktu dalam Sehari')
    ax.set_ylabel('Jumlah Penyewaan')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Pie chart untuk persentase penyewaan berdasarkan waktu
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(summaryHour['cnt'], labels=summaryHour['waktu'], autopct='%1.1f%%', startangle=90, explode=[0.0, 0.0, 0.0, 0.0, 0.1])
    ax.set_title('Jumlah Penyewaan pada berbagai Waktu')
    ax.axis('equal')
    st.pyplot(fig)

    st.markdown("""
    **Penjelasan**: Penyewaan sepeda lebih tinggi pada pagi hari dan sore hari, saat aktivitas masyarakat sedang tinggi.
    """)

# Footer
st.sidebar.markdown("""
---
Created by Akmal Fauzan Restu Agung
""")