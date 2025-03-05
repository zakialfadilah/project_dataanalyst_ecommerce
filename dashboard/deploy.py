import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.write("""
    # Visualisasi Data Analysis E-Commerce
""")

st.subheader('Pertanyaan & Tujuan Analisis')
st.write("""
    1. Negara mana yang memiliki total customer e-commerce terbesar secara general?
    2. Negara mana yang memiliki potensi pertumbuhan e-commerce tertinggi dan layak untuk dijadikan prioritas ekspansi layanan?
    3. Bagaimana perkembangan penjualan pada e-commerce dalam tahun 2017 dan 2018?
    4. Bagaimana perubahan volume penjualan e-commerce antara tahun 2017 dan 2018? Apakah mengalami peningkatan atau penurunan?
""")

tab1, tab2 = st.tabs(["Geographic Analysis", "Sales Quantity Growth"])

with tab1:
    st.header("Geographic Analysis")
    data_customers = pd.read_csv("customers_dataset.csv")
    st.success("File berhasil dimuat dari direktori lokal!")
    st.write("Berikut merupakan Head dari dataset 'customers_dataset'")
    st.dataframe(data_customers.head())
    
    customer_counts = (
        data_customers.groupby("customer_state")["customer_id"]
        .count()
        .reset_index()
        .rename(columns={"customer_state": "State", "customer_id": "Total Customers"})
        .sort_values(by="Total Customers", ascending=False)
    )
    
    st.write("Berikut merupakan Total customer terbesar hingga terkecil di Negara yang sama")
    st.dataframe(customer_counts)
    
    st.write("Berikut merupakan Visualisasi dari total customer terbesar hingga terkecil di Negara yang sama")
    plt.figure(figsize=(10, 6))
    plt.bar(customer_counts["State"], customer_counts["Total Customers"], color="green")
    plt.title("Total Customers per State", fontsize=14)
    plt.xlabel("State", fontsize=12)
    plt.ylabel("Total Customers", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(plt)
    
    st.write("Setelah mendapatkan angka total customer, saya membagi menjadi 2 visualisasi data. Top 5 Highest Customers dan Top 5 Lowest Customers berdasarkan satu Negara")
    top_5_highest = customer_counts.nlargest(5, "Total Customers")
    top_5_lowest = customer_counts.nsmallest(5, "Total Customers")
    
    fig, axes = plt.subplots(1, 2, figsize=(20, 6))
    axes[0].bar(top_5_highest["State"], top_5_highest["Total Customers"], color="green")
    axes[0].set_title("Top 5 States - Highest Customers", fontsize=14)
    axes[0].set_xlabel("State", fontsize=12)
    axes[0].set_ylabel("Total Customers", fontsize=12)
    axes[0].tick_params(axis='x', rotation=45)
    
    axes[1].bar(top_5_lowest["State"], top_5_lowest["Total Customers"], color="red")
    axes[1].set_title("Top 5 States - Lowest Customers", fontsize=14)
    axes[1].set_xlabel("State", fontsize=12)
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    st.pyplot(plt)
    
    st.subheader('Implementasi - Manual Grouping')
    st.write("Setelah mendapatkan angka dan mengurutkan total customer di satu negara, saya melakukan Manual Grouping untuk mengkategorikan total customer di suatu negara termasuk High, Medium dan Low")
    
    def categorize_customers(total):
        if total > 500:
            return "High"
        elif total >= 100:
            return "Medium"
        else:
            return "Low"
    
    customer_counts["Category"] = customer_counts["Total Customers"].apply(categorize_customers)
    st.dataframe(customer_counts)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x="State", y="Total Customers", hue="Category", data=customer_counts, palette={"High": "green", "Medium": "orange", "Low": "red"})
    plt.title("Customer Categories per State", fontsize=14)
    plt.xlabel("State", fontsize=12)
    plt.ylabel("Total Customers", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.subheader("Kesimpulan")
    st.write("""Berdasarkan hasil analisis dan visualisasi data, dapat disimpulkan bahwa e-commerce yang bersangkutan dapat memprioritaskan perusahaan dengan label "High," yang menunjukkan tingginya jumlah konsumen di negara terkait. Keputusan ini dapat dijadikan acuan utama dalam strategi bisnis perusahaan. Sebaliknya, e-commerce juga dapat mempertimbangkan langkah-langkah strategis di negara dengan label "Low" sebelum mengambil keputusan lebih lanjut.""")

with tab2:
    st.header("Sales Quantity Growth")
    st.write("Berikut merupakan Head dari dataset 'orders_dataset'")
    data_order = pd.read_csv("data_order_cleaned.csv")
    st.dataframe(data_order.head())
    
    st.subheader("Tujuan")
    st.write("Tujuan dari analysis dataset ini adalah, saya ingin mengetahui berkembangan penjualan pada e-commerce pada dalam jangka 1 tahun dan juga dalam jangka bulanan")
    
    data_order['order_purchase_timestamp'] = pd.to_datetime(data_order['order_purchase_timestamp'])
    data_order['year'] = data_order['order_purchase_timestamp'].dt.year
    data_order['month'] = data_order['order_purchase_timestamp'].dt.month
    
    customer_count_per_year = data_order.groupby('year')['customer_id'].nunique()
    total_sales_per_month_year = data_order.groupby(['year', 'month'])['order_id'].count()
    
    st.write("Jumlah pelanggan unik per tahun:")
    st.dataframe(customer_count_per_year)
    st.write("\nTotal pembelian tiap bulan per tahun:")
    st.dataframe(total_sales_per_month_year)
    
    data_order = data_order[(data_order['year'] > 2016) & ~((data_order['year'] == 2018) & (data_order['month'] > 8))]
    data_order['quarter'] = ((data_order['month'] - 1) // 3) + 1
    
    total_sales_per_quarter = data_order.groupby(['year', 'quarter'])['order_id'].count().reset_index()
    
    def define_trend(sales):
        if sales.pct_change().dropna().mean() > 0:
            return "Kenaikan"
        elif sales.pct_change().dropna().mean() < 0:
            return "Penurunan"
        else:
            return "Stabil"
    
    total_sales_per_quarter['trend'] = total_sales_per_quarter.groupby('year')['order_id'].transform(define_trend)
    
    st.subheader("Tren Penjualan per Kuartal:")
    st.dataframe(total_sales_per_quarter)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data_order.groupby(['year', 'month'])['order_id'].count().reset_index(),
                 x='month', y='order_id', hue='year', marker='o')
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Pesanan")
    plt.title("Tren Penjualan Tahunan")
    plt.xticks(range(1, 13))
    plt.ylim(0)
    plt.legend(title="Tahun")
    st.pyplot(plt)

    st.subheader("Kesimpulan")
    st.write("""Berdasarkan analisis dan visualisasi data mengenai total penjualan e-commerce setiap bulan dari tahun 2017 hingga 2018, diketahui bahwa e-commerce mengalami peningkatan yang signifikan pada tahun 2017. Namun, pada tahun 2018, pertumbuhan tersebut sempat stagnan di suatu titik sebelum akhirnya mengalami penurunan. Hasil data ini dapat dijadikan bahan evaluasi bagi e-commerce untuk meninjau strategi perusahaan guna meningkatkan kembali tingkat penjualan seperti pada tahun-tahun sebelumnya.""")
