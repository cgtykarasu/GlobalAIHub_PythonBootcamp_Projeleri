import csv
import itertools
import operator
import pandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import stats
import os
import re
from collections import ChainMap
import seaborn as sns
import warnings


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.display.width = 0
plt.rcParams["figure.figsize"] = (11, 11)

df = pd.read_csv('NetflixOriginals.csv', encoding='latin-1')
# print(df)


print(
    '\n----------------------------------------------- PROJE 2 SORU 1 ---------------------------------------------------')
print(
    '----------- Veri setine göre uzun soluklu filmler hangi dilde oluşturulmuştur? Görselleştirme yapınız ------------\n')

test = df[df["Runtime"] > 100]

df2 = test.groupby(["Language"])["Language"].count()
df2_dict = df2.to_dict()
# print(df2_dict)

df2_dict = {key: val for key, val in df2_dict.items() if val > 2}

print("100 dakika üstü filmlerin yayımlandığı diller ve film sayıları:")
for k, v in df2_dict.items():
    print(k, v)

labels = []
sizes = []

for x, y in df2_dict.items():
    labels.append(x)
    sizes.append(y)

plt.figure(figsize=(11, 11))

explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)

plt.legend(labels=labels, bbox_to_anchor=(0.15, 0.95),
           ncol=3, title='100 dakika üstü filmlerin yayımlandığı diller\n', title_fontsize=18)

plt.show()

# ----------------------------------------------------------------------------------------------------------- #

df[['Month', 'Year']] = df.Premiere.str.split(',', expand=True)

df[['Month', 'Day', "none"]] = df['Month'].str.split(pat=' ', expand=True)
del df["none"]
# print(df)
df.at[308, 'Year'] = 2017
df.at[308, 'Day'] = 15
df.at[387, 'Year'] = 2016
df.at[387, 'Day'] = 15
df.at[111, 'Year'] = 2019
df.at[111, 'Day'] = 16
df.at[541, 'Year'] = 2016
df.at[541, 'Day'] = 16
df.at[538, 'Year'] = 2017
df.at[538, 'Day'] = 27

test2 = df.sort_values(['Year', 'Day'],
                       ascending=[True, True])

# print(test2)

df['Year'] = df['Year'].astype(int)
df['IMDB Score'] = df['IMDB Score'].astype(float)

print(
    '\n----------------------------------------------- PROJE 2 SORU 2 ---------------------------------------------------')
print(
    '2019 Ocak ile 2020 Haziran tarihleri arasında "Documentary" türünde çekilmiş filmlerin IMDB değerlerini bulup görselleştiriniz\n')

# test4 = df.apply(lambda row: row[df['Year'].isin([2019,2020])])
test4 = df[(df['Year'] == 2019)]

test5 = df[df["Year"] == 2020]
test5 = test5[(test5["Month"] == "January") |
              (test5["Month"] == "February") |
              (test5["Month"] == "March") |
              (test5["Month"] == "April") |
              (test5["Month"] == "May") |
              (test5["Month"] == "June")]

concatenated = pd.concat([test4, test5])
print("01-2019/06-2020 tarihleri arasında 'Documentary' türünde çekilmiş filmlerin ilk 10 tanesi :\n",
      concatenated[['Title', 'IMDB Score']].head(10), "\n")

pd.options.mode.chained_assignment = None  # default='warn'

concatenated['Month'].loc[concatenated['Month'] == "January"] = 1
concatenated['Month'].loc[concatenated['Month'] == "February"] = 2
concatenated['Month'].loc[concatenated['Month'] == "March"] = 3
concatenated['Month'].loc[concatenated['Month'] == "April"] = 4
concatenated['Month'].loc[concatenated['Month'] == "May"] = 5
concatenated['Month'].loc[concatenated['Month'] == "June"] = 6
concatenated['Month'].loc[concatenated['Month'] == "July"] = 7
concatenated['Month'].loc[concatenated['Month'] == "August"] = 8
concatenated['Month'].loc[concatenated['Month'] == "September"] = 9
concatenated['Month'].loc[concatenated['Month'] == "October"] = 10
concatenated['Month'].loc[concatenated['Month'] == "November"] = 11
concatenated['Month'].loc[concatenated['Month'] == "December"] = 12

# print(concatenated.dtypes)

concatenated = concatenated[concatenated["Genre"] == "Documentary"]
concatenated = concatenated.sort_values(['Year', 'Month', 'Day'])
# print(concatenated)
concatenated.plot.bar(x="Year", y="IMDB Score")
plt.show()

# ----------------------------------------------------------------------------------------------- #

df['Date'] = pd.to_datetime(df.Premiere)

df_documentary = df.loc[(df['Genre'] == 'Documentary')]
df_documentary_time_range = df_documentary.loc[(df['Date'] > "2019-01-31") & (df['Date'] < "2020-06-01")]
plt.figure(figsize=(11, 11))
plt.bar(df_documentary_time_range.Title, df_documentary_time_range["IMDB Score"],
        label="01/2019-06/2020 'Documentary' IMDB değerleri")
plt.legend()
plt.grid()
plt.xticks(rotation='vertical')
plt.show()

print(
    '----------------------------------------------- PROJE 2 SORU 3 ---------------------------------------------------')
print(
    '---------------- İngilizce çekilen filmler içerisinde hangi tür en yüksek IMDB puanına sahiptir ------------------\n')

test6 = df[df["Language"] == "English"]

print("İngilizce çekilen filmler içerisinde", test6._get_value(test6['IMDB Score'].idxmax(), 'IMDB Score'),
      "puanlı ", test6._get_value(test6['IMDB Score'].idxmax(), 'Title'), "filmidir. "
                                                                          "Filmin türü : ",
      test6._get_value(test6['IMDB Score'].idxmax(), 'Genre'), "\n")

print(
    '----------------------------------------------- PROJE 2 SORU 4 ---------------------------------------------------')
print(
    '-------------------- "Hindi" Dilinde çekilmiş olan filmlerin ortalama "runtime" suresi nedir ---------------------\n')

df['Runtime'] = df['Runtime'].astype(int)
test7 = df[df["Language"] == "Hindi"]
# print(test7)
print("TOPLAM RUNTIME : ", test7['Runtime'].sum())
print("SATIR SAYISI : ", test7.shape[0])

print("'Hindi' Dilinde çekilmiş olan filmlerin ortalama 'runtime' suresi :",
      round(test7['Runtime'].sum() / test7.shape[0], 2), "dakikadır.\n")

print(
    '----------------------------------------------- PROJE 2 SORU 5 ---------------------------------------------------')
print(
    '------- "Genre" Sütunu kaç kategoriye sahiptir ve bu kategoriler nelerdir? Görselleştirerek ifade ediniz ---------\n')

df = df.replace('-', ' ', regex=True)
var = df[df['Genre'].str.match(r'\A[\w-]+\Z')]
# var = df[df.Genre.apply(lambda x: len(x.split()) == 1)]
# print(var)

sep = '|'
punctuation_chars = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{}~'
mapping_table = str.maketrans(dict.fromkeys(punctuation_chars, ''))

df['Genre'] = sep \
    .join(df['Genre'].tolist()) \
    .translate(mapping_table) \
    .split(sep)
# print(df)

uniqueValues = var['Genre'].unique()
print("Genre sütunu kategorileri :", uniqueValues)

fig = plt.figure()

plt.text(0.05, 0.01, uniqueValues[0], size=18, rotation=20.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.05, 0.2, uniqueValues[1], size=18, rotation=10.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.05, 0.4, uniqueValues[2], size=18, rotation=30.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.05, 0.6, uniqueValues[3], size=18, rotation=40.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.05, 0.8, uniqueValues[4], size=18, rotation=15.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.05, 1, uniqueValues[5], size=18, rotation=5.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.35, 0.02, uniqueValues[6], size=18, rotation=0.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.35, 0.2, uniqueValues[7], size=18, rotation=12.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.35, 0.4, uniqueValues[8], size=18, rotation=22.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.35, 0.6, uniqueValues[9], size=18, rotation=34.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.35, 0.8, uniqueValues[10], size=18, rotation=45.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.35, 1, uniqueValues[11], size=18, rotation=55.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.6, 0.1, uniqueValues[12], size=18, rotation=10.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.6, 0.4, uniqueValues[13], size=18, rotation=27.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.6, 0.6, uniqueValues[14], size=18, rotation=17.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.8, 0.85, uniqueValues[15], size=18, rotation=15.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.6, 1, uniqueValues[16], size=18, rotation=21.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.9, 0.6, uniqueValues[17], size=18, rotation=4.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.9, 0.4, uniqueValues[18], size=18, rotation=33.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.9, 0.2, uniqueValues[19], size=18, rotation=59.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.show()

print(
    '\n----------------------------------------------- PROJE 2 SORU 6 ---------------------------------------------------')
print(
    '----------------------- Veri setinde bulunan filmlerde en çok kullanılan 3 dili bulunuz --------------------------\n')

dftest = df.groupby(["Language"])["Language"].count()
dftest_dict = dftest.to_dict()
sorted_d = sorted(dftest_dict.items(), key=operator.itemgetter(1), reverse=True)
print("Veri setinde bulunan filmlerde en çok kullanılan 3 dil")
print(sorted_d[0][0], "dili ilk sırada yer almakta olup", sorted_d[0][1], "filmde kullanılmıştır.\n",
      sorted_d[1][0], "dili ikinci sırada yer almakta olup", sorted_d[1][1], "filmde kullanılmıştır.\n",
      sorted_d[2][0], "dili üçüncü sırada yer almakta olup", sorted_d[2][1], "filmde kullanılmıştır.")

print(
    '\n----------------------------------------------- PROJE 2 SORU 7 ---------------------------------------------------')
print(
    '---------------------------- IMDB puanı en yüksek olan ilk 10 film hangileridir ----------------------------------\n')

dfimdb = df.sort_values('IMDB Score', ascending=False)
print("IMDB puanı en yüksek olan ilk 10 film :\n",
      dfimdb[['Title', 'IMDB Score']].head(10))

print(
    '\n----------------------------------------------- PROJE 2 SORU 8 ---------------------------------------------------')
print(
    '------------ IMDB puanı ile "Runtime" arasında nasıl bir korelasyon vardır? İnceleyip görselleştiriniz -----------\n')

dfcorr = df[['Runtime', 'IMDB Score']]

sns.set(style="ticks", color_codes=True)
g = sns.pairplot(dfcorr)
plt.show()

print(
    '\n----------------------------------------------- PROJE 2 SORU 9 ---------------------------------------------------')
print(
    '------------------- IMDB Puanı en yüksek olan ilk 10 "Genre" hangileridir? Görselleştiriniz ----------------------\n')

dfimdbgenre = df.sort_values('IMDB Score', ascending=False)
print("IMDB puanı en yüksek olan ilk 10 film :")
for i in dfimdbgenre[:10]:
    print(i)

uniqueGenre = dfimdbgenre['Genre'].unique()
print("IMDB Puanı en yüksek olan ilk 10 'Genre")
for i in uniqueGenre[:10]:
    print(i)

fig = plt.figure()

plt.legend(labels=labels, bbox_to_anchor=(0.85, 1.15),
           ncol=1, title='IMDB Puanı en yüksek olan ilk 10 Genre\n', title_fontsize=12)

plt.text(0.2, 0.01, uniqueGenre[0], size=18, rotation=20.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.2, 0.2, uniqueGenre[1], size=18, rotation=10.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.2, 0.4, uniqueGenre[2], size=18, rotation=30.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.4, 0.6, uniqueGenre[3], size=18, rotation=5.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.4, 0.8, uniqueGenre[4], size=18, rotation=15.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.1, 0.9, uniqueGenre[5], size=18, rotation=5.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.9, 0.1, uniqueGenre[6], size=18, rotation=0.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.7, 0.2, uniqueGenre[7], size=18, rotation=12.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.7, 0.4, uniqueGenre[8], size=18, rotation=22.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.text(0.8, 0.8, uniqueGenre[9], size=18, rotation=17.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

plt.show()

print(
    '\n----------------------------------------------- PROJE 2 SORU 10 ---------------------------------------------------')
print(
    '------------------ "Runtime" değeri en yüksek olan ilk 10 film hangileridir? Görselleştiriniz. --------------------\n')

dfruntime = df.sort_values('Runtime', ascending=False)
print("Runtime değeri en yüksek olan ilk 10 film :\n",
      dfruntime[['Title', 'Runtime']].head(10))

plt.bar(dfruntime.Title.head(10), dfruntime["Runtime"].head(10), label="'Runtime' değeri en yüksek olan ilk 10 film")
plt.legend()
plt.grid()
plt.xticks(rotation='vertical')
plt.show()

print(
    '\n----------------------------------------------- PROJE 2 SORU 11 ---------------------------------------------------')
print(
    '------------------------- Hangi yılda en fazla film yayımlanmıştır? Görselleştiriniz ------------------------------\n')

dfyear = df.groupby(["Year"])["Year"].count()
# print(dfyear)
dfyear_dict = dfyear.to_dict()
# print(dfyear_dict)
sorted_y = sorted(dfyear_dict.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_y)
# print(type(sorted_y))

text = [sorted_y[0][1], sorted_y[1][1], sorted_y[2][1], sorted_y[3][1], sorted_y[4][1], sorted_y[5][1], sorted_y[6][1],
        sorted_y[7][1]]

plt.xlabel("Yıllar")
plt.ylabel("Film sayıları")
xs = [x for x, y in sorted_y]
ys = [y for x, y in sorted_y]
plt.title('Yıllara göre yayımlanan film sayıları')
colors = np.random.rand(8)
plt.scatter(xs, ys, s=1000, c=colors, alpha=0.5)

for i in range(len(xs)):
    plt.annotate(text[i], (xs[i], ys[i] + 0.2))

plt.show()

print(
    '\n----------------------------------------------- PROJE 2 SORU 12 ---------------------------------------------------')
print(
    '----------- Hangi dilde yayımlanan filmler en düşük ortalama IMBD puanına sahiptir? Görselleştiriniz --------------\n')

# print("#" * 70)

dfimdblang = df.sort_values('IMDB Score', ascending=True)
dfimdblang['avg_imdb'] = dfimdblang.groupby(['Language'])['IMDB Score'] \
    .transform('mean')
dfimdblang = dfimdblang.drop_duplicates(subset=["Language"], keep=False)
dfimdblang = dfimdblang.drop(
    labels=['Title', 'Genre', 'Premiere', 'Runtime', 'IMDB Score', 'Month', 'Year', 'Day', 'Date'], axis=1)
dfimdblanglist = dfimdblang.values.tolist()

# print("IMDB puanı en düşük olan filmler ve yayımlandığı diller :\n",
#       dfimdblang[['Language', 'IMDB Score']])

uniquelang = dfimdblang['Language'].unique()
print("En düşük IMDB puanına sahip ilk 10 filmin yayımlandığı diller")
for i in uniquelang[:10]:
    print(i)

textl = [dfimdblanglist[0][1], dfimdblanglist[1][1], dfimdblanglist[2][1], dfimdblanglist[3][1], dfimdblanglist[4][1],
         dfimdblanglist[5][1], dfimdblanglist[6][1], dfimdblanglist[7][1], dfimdblanglist[8][1], dfimdblanglist[9][1],
         dfimdblanglist[10][1], dfimdblanglist[11][1], dfimdblanglist[12][1], dfimdblanglist[13][1],
         dfimdblanglist[14][1], dfimdblanglist[15][1], dfimdblanglist[16][1], dfimdblanglist[17][1]]

plt.xlabel("Diller")
plt.ylabel("IMDB Puanı")
xsl = [x for x, y in dfimdblanglist]
ysl = [y for x, y in dfimdblanglist]
plt.title('IMDB puanı en düşük filmlerin yayımlandığı diller ve IMDB puanları')
colors = np.random.rand(18)
plt.scatter(xsl, ysl, s=50, c=colors, alpha=0.9)
plt.xticks(rotation='vertical')

for i in range(len(xsl)):
    plt.annotate(textl[i], (xsl[i], ysl[i]))

plt.show()

print(
    '\n----------------------------------------------- PROJE 2 SORU 13 ---------------------------------------------------')
print(
    '------------------------------ Hangi yılın toplam "runtime" süresi en fazladır ------------------------------------\n')

df_longest_movie = df[df.Runtime == df.Runtime.max()]
print(df_longest_movie.iloc[0])

df["Date"] = pd.to_datetime(df.Premiere)
df['Year'] = df['Date'].dt.year
year = df.Year.value_counts()
print(year)
df_total_run_per_year = df.groupby("Year").agg({"Runtime": "sum"}).sort_values(by="Runtime", ascending=False)
plt.bar(df_total_run_per_year.index, df_total_run_per_year.Runtime, label="Year")
plt.legend()
plt.grid()
plt.xticks(rotation='vertical')
plt.show()

print(
    '\n----------------------------------------------- PROJE 2 SORU 14 ---------------------------------------------------')
print(
    '----------------------------- Her bir dilin en fazla kullanıldığı "Genre" nedir -----------------------------------\n')

# df_language_genres = df.groupby(["Language"])["Genre"].value_counts()

# df_language_genres = df.groupby(["Language"])["Genre"].count()
df_language_genres = (df.groupby(['Language', 'Genre']).size()
                      .sort_values(ascending=False)
                      .reset_index(name='count')
                      .drop_duplicates(subset='Language'))

print("Her dilin en fazla kullanıldığı 'Genre' listesi")
print(df_language_genres)

print(
    '\n----------------------------------------------- PROJE 2 SORU 15 ---------------------------------------------------')
print(
    '------------------------------ Veri setinde outlier veri var mıdır? Açıklayınız -----------------------------------\n')

dflast = pd.read_csv('NetflixOriginals.csv', encoding='latin-1')

warnings.filterwarnings('ignore')
plt.figure(figsize=(16,5))
plt.subplot(1,2,1)
sns.distplot(dflast['IMDB Score'])
plt.subplot(1,2,2)
sns.distplot(df['Runtime'])
plt.show()

print("Outlier tespiti için kullanmış olduğum Z-score treatment yönteminde 'Runtime' sütununda aykırı değer "
      "olduğunu görmekteyim. Ancak yapılan veri analizinde bahse konu sütunun yapılacak analize etki edecek bir husus "
      "olmadığını değerlendirmekteyim.")
