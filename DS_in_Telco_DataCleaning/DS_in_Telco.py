#%% md
# # Import Library
#%%
import pandas as pd
pd.options.display.max_columns = 50
#%% md
# # Load Dataset
#%%
df = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/dqlab_telco.csv')
#%%
# Tampilkan dimensi data
print(df.shape)

# Ada 7133 baris dan 22 kolom'''
#%%
# Tampilkan 5 data teratas
print(df.head(5))
#%%
# Tampilkan jumlah ID unik pelanggan
print(df.customerID.nunique())


# 1. nunique() -> digunakan untuk menghitung jumlah values yang unik
# 2. unique() -> digunakan untuk mengetahui value apa saja yang bersifat unik
# 3. Tnpa list -> akses feature tanpa list untuk menghitung jumlah feature tsb yang bersifat unik

#%% md
# # Filter ID Number Format Benar
# 
# Syarat ID Number valid:
# 1. Panjang karakter 11-12
# 2. Hanya angka
# 3. Diawali dg 45 di 2 digit pertama
#%%
# Gunakan REGEX untuk mengetahui nilai valid
df['valid_id'] = df['customerID'].astype(str).str.match(r'(45\d{9,10})')

# Buat kolom bantuan 'valid_id' untuk menandai ID mana saja yang bernilai sesuai syarat. Maknanya id akan di cek 45 adalah nilai awal dan diikuti 9/10 angka dibelakangnya. Menggunakan astype(str) -> memastika customer_ID diperlakukan sebagai string.
#%%
# Drop baris2 yang ber id tidak sesuai berdasarkan bantuan valid_id columns
df = (df[df['valid_id'] == True]).drop('valid_id', axis=1)
#%%
#Lihat hasilnya:

print('Hasil jumlah ID Customer yang valid: ', df['customerID'].count())
#%% md
# # Filter Duplikat Data
#%%
# Drop Duplicat Rows
df = df.drop_duplicates()
#%%
print(df.shape)
#%%
# Drop Duplikat data berdasarkan waktu inserting yang sama

df = df.sort_values('UpdatedAt',ascending=False).drop_duplicates('customerID')
# Hanya satu baris untuk setiap nilai 'customerID' yang akan disimpan di DataFrame, sisanya (duplikatnya) akan dihapus.
#%%
# Lihat hasil customer_ID yang telah dibersihkan datanya
print('Jumlah ID Customer after clening: ',df['customerID'].count())
#%% md
# # Mengatasi Rows Missing Value
# 
# Mendeteksi rows yang tidak terdeteksi apakah churn atau tidak. Menggunakan isnull() untuk deteksi dan dropna() untuk drop missing value
#%%
# Perlihatkan total missing value pada kolom churn
print('Total missing values kolom Churn', df['Churn'].isnull().sum())

# Ada 43 baris missing values
#%%
# Drop semua baris yang kosong pada kolom Churn
df.dropna(subset=['Churn'], inplace=True)

print('Dimensi after drop missing values: ', df.shape)
#%% md
# ## Mengatasi Missing Values dengan pengisian nilai tertentu
# 
# 1. Modeller meminta kolom Tenure yang kosong diisi dengan angka 11
# 2. Untuk variabel numerik lain yang memiliki miss value diisi dengan median dari masing-masing variabel
#%%
# Cek status missing values di semua kolom
print('Status Missing Values: ', df.isnull().values.any())

# Hasil = True -> berarti ada kolom2 yang memiliki Missing value
#%%
# Tampilkan jumlah missing values masing2 kolom:
print('\nJumlah Missing Values each columns: ')
print(df.isnull().sum().sort_values(ascending=False)) # Dari terbesar ke terkecil
#%%
df22 = df2.copy() # Takut keubah semua cuyyyyy
#%%
# Handling missing value kolom Tenure
df['tenure'] = df['tenure'].fillna(11)
#%%
# Handling num vars
for col_name in list(['MonthlyCharges', 'TotalCharges']):
    median = df[col_name].median()
    df[col_name] = df[col_name].fillna(median)
#%%
# Tampilkan jumlah missing values after handling
print('\nJumlah Missing Values After Handling: ')
print(df.isnull().sum().sort_values(ascending=False))
#%% md
# # Mengatasi Outlier
# 
# Mendeteksi outliers dengan boxplot
#%%
# Deskripsikan sebaran data sebelum divisualisasikan.
print('\nSebaran data Telco: ')
print(df[['tenure', 'MonthlyCharges', 'TotalCharges']].describe())
#%%
# Import library visualisasi
import matplotlib.pyplot as plt
import seaborn as sns
#%%
# Buat Boxplot untuk masing2 dari ketiga Variabel:
# Tenure
plt.figure()
sns.boxplot(x=df['tenure'], color='red', fliersize=8, flierprops={'markerfacecolor': 'r'})
plt.title('Boxplot Tenure')
plt.xlabel('Tenure')
plt.show()

# MonthlyCharges
plt.figure()
sns.boxplot(x=df['MonthlyCharges'], color='red', fliersize=8, flierprops={'markerfacecolor': 'r'})
plt.title('Boxplot MonthlyCharges')
plt.xlabel('MonthlyCharges')
plt.show()

# TotalCharges
plt.figure()
sns.boxplot(x=df['TotalCharges'], color='red', fliersize=8, flierprops={'markerfacecolor': 'r'})
plt.title('Boxplot TotalCharges')
plt.xlabel('TotalCharges')
plt.show()
#%% md
# ## Mengatasi Outlier dengan Quantile dan mask
#%%
# Menangani outlier
# Proses outlier dengan batch calculation (lebih efisien & rapih)
Q1 = (df[['tenure','MonthlyCharges','TotalCharges']]).quantile(0.25)
Q3 = (df[['tenure','MonthlyCharges','TotalCharges']]).quantile(0.75)
IQR = Q3 - Q1
maximum = Q3 + (1.5*IQR)
print('\nNilai Maximum dari masing-masing Variabel adalah: ')
print(maximum)

minimum = Q1 - (1.5*IQR)
print('\nNilai Minimum dari masing-masing Variabel adalah: ')
print(minimum)

more_than = (df[['tenure', 'MonthlyCharges', 'TotalCharges']] > maximum)
lower_than = (df[['tenure', 'MonthlyCharges', 'TotalCharges']] < minimum)
df = df.mask(more_than, maximum, axis=1)
df = df.mask(lower_than, minimum, axis=1)

print('\nPersebaran data setelah ditangani Outlier: ')
print(df[['tenure', 'MonthlyCharges', 'TotalCharges']].describe())
#%%
# Viasualisasikan ulang dg boxplot

# Tenure
plt.figure()
sns.boxplot(x=df['tenure'], color='red', fliersize=8, flierprops={'markerfacecolor': 'r'})
plt.title('Boxplot Tenure')
plt.xlabel('Tenure')
plt.show()

# MonthlyCharges
plt.figure()
sns.boxplot(x=df['MonthlyCharges'], color='red', fliersize=8, flierprops={'markerfacecolor': 'r'})
plt.title('Boxplot MonthlyCharges')
plt.xlabel('MonthlyCharges')
plt.show()

# TotalCharges
plt.figure()
sns.boxplot(x=df['TotalCharges'], color='red', fliersize=8, flierprops={'markerfacecolor': 'r'})
plt.title('Boxplot TotalCharges')
plt.xlabel('TotalCharges')
plt.show()
#%% md
# # Mendeteksi Nilai yang Tidak Standar
# 
# Mendeteksi apakah ada nilai-nilai dari variable kategorik yang tidak standard. Hal ini biasanya terjadi dikarenakan kesalahan input data. Perbedaan istilah menjadi salah satu faktor yang sering terjadi, untuk itu dibutuhkan standardisasi dari data yang sudah ter-input.
# 
# Gunakan fungsi value_counts() untuk melihat jumlah data unique per variable-nya.
#%%
#Loop
for col_name in list(df):
	print(f'\nUnique Values Count Before Standardized Variable {col_name}')
	print(df[col_name].value_counts())
	print()
#%% md
# ## Melakukan Standarisasi dengan looping
# 
# Kita bisa menggunakan fungsi .replace(), Namun, karena variabel yang perlu distandarisasi memiliki jenis isi variabel yang berbeda maka kita gunakan if else
#%%
kolom_std = ['gender', 'Dependents', 'Churn']

for col_name in kolom_std:
  print(f"\nStandarisasi Kolom:{col_name}")
  print('Nilai unik sebelum distandarisasi: ')
  print(df[col_name].unique())
  print('\nJumlah nilai unik sebelum distandarisasi: ')
  print(df[col_name].value_counts())
#%%
for col_name in kolom_std:
    if col_name == 'gender':
        mapping = {'Wanita' : 'Female', 'Laki-Laki' : 'Male', 'Famale' : 'Female'}
    elif col_name == 'Dependents':
        mapping = {'Iya' : 'Yes'}
    elif col_name == 'Churn':
        mapping = {'Churn' : 'Yes'}
    else:
        mapping = {}

    df[col_name] = df[col_name].replace(mapping)

for col_name in list(df[['gender', 'Dependents', 'Churn']]):
	print(f'\nUnique Values Count After Standardized Variable {col_name}')
	print(df[col_name].value_counts())
	print()