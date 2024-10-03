import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Load the dataset
day = pd.read_csv('../data/dayNew.csv')  

# Title and description
st.title("Dashboard Analisis Penyewaan Sepeda")
st.markdown("""
Dashboard ini menampilkan berbagai insight dari analisis penyewaan sepeda, termasuk faktor utama yang mempengaruhi penyewaan, dampak cuaca, pola penyewaan harian, dan hasil clustering.
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Pilih Insight", ("Pengaruh Cuaca & Waktu", "Distribusi Penyewaan", "Pola Jam Per Jam", "Cluster Analysis"))

# Display insight based on selection
if option == "Pengaruh Cuaca & Waktu":
    st.header("Pengaruh Suhu dan Kelembapan terhadap Penyewaan Sepeda")

    fig, ax = plt.subplots()
    sns.barplot(x='temp_category', y='cnt', data=day, estimator=sum, ax=ax)
    ax.set_title('Pengaruh Suhu terhadap Jumlah Penyewaan Sepeda')
    ax.set_xlabel('Kategori Suhu (temp_category)')
    ax.set_ylabel('Total Jumlah Penyewaan (cnt)')
    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.barplot(x='hum_category', y='cnt', data=day, estimator=sum, ax=ax)
    ax.set_title('Pengaruh Kelembapan terhadap Jumlah Penyewaan Sepeda')
    ax.set_xlabel('Kelembapan (Kategori Hum)')
    ax.set_ylabel('Total Jumlah Penyewaan (cnt)')
    st.pyplot(fig)

    st.markdown("""
    **Kesimpulan**: Suhu memiliki pengaruh yang signifikan terhadap penyewaan sepeda, di mana suhu hangat meningkatkan penyewaan, sedangkan kelembapan tinggi sedikit mengurangi minat penyewaan.
    """)

elif option == "Distribusi Penyewaan":
    st.header("Distribusi Penyewaan Sepeda menurut Musim dan Kondisi Cuaca")

    fig, ax = plt.subplots()
    sns.barplot(x='seasonDesc', y='cnt', data=day, estimator=sum, ax=ax)
    ax.set_title('Distribusi Penyewaan Sepeda menurut Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Total Jumlah Penyewaan')
    st.pyplot(fig)

    # Plot rentals by weather situation
    fig, ax = plt.subplots()
    sns.barplot(x='weathersit', y='cnt', data=day, estimator=sum, ax=ax)
    ax.set_title('Jumlah Penyewaan Sepeda menurut Kondisi Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

    st.markdown("""
    **Kesimpulan**: Penyewaan sepeda paling tinggi terjadi pada musim gugur dan cuaca cerah. Cuaca buruk seperti hujan atau salju secara signifikan menurunkan jumlah penyewaan.
    """)

elif option == "Pola Jam Per Jam":
    st.header("Pola Penyewaan Sepeda per Jam")

    hour = pd.read_csv('../data/hourNew.csv') 

    fig, ax = plt.subplots()
    sns.lineplot(x='waktu', y='cnt', data=hour, hue='weathersitDesc', ax=ax)
    ax.set_title('Pola Penyewaan Sepeda per Jam dengan Kondisi Cuaca')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah Penyewaan (cnt)')
    st.pyplot(fig)

    st.markdown("""
    **Kesimpulan**: Penyewaan tertinggi terjadi pada sore hari, diikuti oleh pagi hari. Cuaca cerah memberikan kontribusi besar pada peningkatan penyewaan pada jam sibuk.
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
    **Kesimpulan**: Kluster 0 menunjukkan penurunan penyewaan pada suhu dingin dan kelembapan tinggi, sedangkan Kluster 1 menunjukkan kenaikan penyewaan pada suhu hangat dan kelembapan rendah.
    """)

# Footer
st.sidebar.markdown("""
---
Created by Akmal Fauzan Restu Agung
""")