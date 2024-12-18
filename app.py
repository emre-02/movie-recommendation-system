import streamlit as st
import pandas as pd
import joblib
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# uygulamayı ayarla
st.set_page_config(page_title="Movie-RR", page_icon="🍿", layout="wide")    
st.markdown(f"""
            <style>
            .stApp {{background-image: url(""); 
                     background-attachment: fixed;
                     base: light;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)

# Modelleri yükleme
df = joblib.load('models/movie_db.df')
tfidf_matrix = joblib.load('models/tfidf_mat.tf')
tfidf = joblib.load('models/vectorizer.tf')
cos_mat = joblib.load('models/cos_mat.mt')



def get_recommendations(movie):
    
    # df değişkeninden indeks al
    index = df[df['title']== movie].index[0]    
    # benzer filmleri sırala  
    similar_movies = sorted(list(enumerate(cos_mat[index])), reverse=True, key=lambda x: x[1]) 
    # film adlarını döndür
    recomm = []
    for i in similar_movies[1:6]:
        recomm.append(df.iloc[i[0]].title)
    return recomm

def fetch_poster(movies):
    ids = []
    posters = []
    for i in movies:
        ids.append(df[df.title==i]['id'].values[0])
        
    for i in ids:    
        url = f"https://api.themoviedb.org/3/movie/{i}?api_key=09085051b6bc660f4d331416740e3242"
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        posters.append(full_path)
    return posters

# Streamlit 
st.image("images/app2.jpg")
st.title("Movie Recommendation Robot 🎥 🤖")
posters = 0
movies = 0

with st.sidebar:
    st.image("images/app1.png", use_container_width=True)
    
    st.header("Öneri Alın 👇")
    search_type = st.radio("", ['Film Başlığı'])  
    
    st.header("Kaynak Kod 📦")
    st.markdown("[GitHub Deposu](https://github.com/emre-02/movie-recommendation-system)")
    
    st.header("Blog 📝")
    st.markdown("[Medium Makalesi](https://medium.com/@ozturky81)")


if search_type == 'Film Başlığı': 
    st.subheader("Select Movie🎬")   
    movie_name = st.selectbox('', df.title)
    if st.button('Recommend 🚀'):
        with st.spinner('Wait for it... (Lütfen Bekleyin)'):
            movies = get_recommendations(movie_name)
            posters = fetch_poster(movies)        

   
              
# film posterlerini göster       
if posters:
    col1, col2, col3, col4, col5 = st.columns(5, gap='medium')
    with col1:
        st.text(movies[0])
        st.image(posters[0])
    with col2:
        st.text(movies[1])
        st.image(posters[1])

    with col3:
        st.text(movies[2])
        st.image(posters[2])
    with col4:
        st.text(movies[3])
        st.image(posters[3])
    with col5:
        st.text(movies[4])
        st.image(posters[4])
