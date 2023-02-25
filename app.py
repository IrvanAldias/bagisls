import streamlit as st
import pandas as pd
import random
import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

st.set_page_config(page_icon="📃", page_title="BagiSLS")

st.image(
    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/page-with-curl_1f4c3.png",
    width=100,
)

st.title("BagiSLS")
st.subheader('Data SLS:')
st.caption('Unggah data SLS yang akan dibagikan kepada pengentri. Data ini berisikan diantaranya kode sls dan jumlah keluarga. Contoh dokumen dapat diunduh di bawah.')

uploaded_file = st.file_uploader(
    "Unggah data SLS",
    key="1",
    help="Untuk mengaktifkan 'wide mode', pergi ke menu > pengaturan > aktifkan 'wide mode'",
)

if uploaded_file is not None:
    file_container = st.expander("Lihat data .csv yang unggah")
    df = pd.read_csv(uploaded_file)
    uploaded_file.seek(0)
    file_container.write(df)

else:
    st.info(
        f"""
            👆 Unggah dokumen .csv terlebih dahulu. Contoh dokumen .csv: [datasls.csv](https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv)
            """
    )
    st.stop()

sls_list = df.values.tolist()

kecamatans = pd.unique(df["kecamatan"]).tolist()

options = st.sidebar.multiselect(
    'Pilih Kecamatan',
    kecamatans, kecamatans)

sortedkec = []
for kecamatan in range(len(options)):
    #memfilter dan sorting sls dengan kecamatan yang sama
    filters = [options[kecamatan]]
    selectedkec = list(filter(lambda x: set(x).intersection(filters), sls_list))
    sortedkec.extend(sorted(selectedkec, key=lambda x: x[4], reverse=True))

st.subheader('Data Pengentri:')
st.caption('Unggah data Pengentri atau buat data dummy. Contoh dokumen dapat diunduh di bawah.')
 
uploaded_file2 = st.file_uploader(
    "Unggah data Pengentri",
    key="2",
    help="Untuk mengaktifkan 'wide mode', pergi ke menu > pengaturan > aktifkan 'wide mode'",
)

if uploaded_file2 is not None:
    file_container2 = st.expander("Lihat data .csv yang unggah")
    df2 = pd.read_csv(uploaded_file2)
    uploaded_file2.seek(0)
    file_container2.write(df2)

else:
    st.info(
        f"""
            👆 Unggah dokumen .csv terlebih dahulu. Contoh dokumen .csv: [biostats.csv](https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv)
            """
    )
    st.stop()

df2['total_kk'] = 0

pengentri_list = df2.values.tolist()

number2 = st.sidebar.number_input('Masukkan Random Seed:', step=1)

random.seed(number2)
random.shuffle(pengentri_list)

sum_kk = 0
for kec in sortedkec:
    sum_kk+=kec[4]

#memindahkan sls ke pengentri one-to-one
while sortedkec:
    for pengentri in range(len(pengentri_list)):
        if len(sortedkec) == 0:
            break
        
        if pengentri_list[pengentri][1] < (sum_kk/len(pengentri_list)):
            pengentri_list[pengentri].append(sortedkec[0])
            del sortedkec[0]

            sum = 0
            #mencari jumlah sls terkini dalam satu pengentri
            for datasls in pengentri_list[pengentri]:
                if type(datasls) == list:
                    sum+=datasls[4]
            
            #mengupdate jumlah sls terkini dalam satu pengentri
            if type(pengentri_list[pengentri][1]) == int:
                pengentri_list[pengentri][1] = sum
            
    # sorting pengentri ulang
    pengentri_list = sorted(pengentri_list, key=lambda x: x[1])
            
hasil = pd.DataFrame(pengentri_list)
hasil

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(hasil)

nama_simpan = st.text_input('Nama file', 'Hasil.csv')

st.download_button(
    label="Download data sebagai CSV",
    data=csv,
    file_name=nama_simpan,
    mime='text/csv',
)

# with pd.ExcelWriter('hasilkedua.xlsx') as writer:
#     for i in hasil:
#         hasil.iloc[i].to_excel(writer, sheet_name=str(hasil.iloc[i][0]))

# st.download_button(
#     label="Download data sebagai Excel",
#     data=xlsx,
#     file_name='hasilfinal.csv',
#     mime='text/csv',
# )

st.success('Pembagian berhasil!', icon="✅")

