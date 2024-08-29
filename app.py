
import compress_pickle as cpickle
import pickle
import streamlit as st
import numpy as np
import pandas as pd

st.header('Book Recommender System Using Unsupervised Machine Learning')
model = pickle.load(open('Pickle/model.pkl','rb'))
book_names = pickle.load(open('Pickle/book_names.pkl','rb'))
final_rating = pickle.load(open('Pickle/final_rating.pkl','rb'))
book_pivot = pickle.load(open('Pickle/book_pivot.pkl','rb'))


# Load the model
with open('Picklec/model.pkl', 'rb') as file:
    model1 = pickle.load(file)

# Load book names
with open('Picklec/book_names.pkl', 'rb') as file:
    book_namess = pickle.load(file)

# Load final books
final_books = cpickle.load('Picklec/final_rating_compressed.lzma', compression='lzma')

with open('Picklec/book_pivot.pkl', 'rb') as file:
    book_pivot_table = pickle.load(file)

def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url

def fetch_poster_(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot_table.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_books['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_books.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url

def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                books_list.append(j)
    return books_list , poster_url       

def recommend_book_(book_name):
    books_list = []
    book_id = np.where(book_pivot_table.index == book_name)[0][0]
    distance, suggestion = model1.kneighbors(book_pivot_table.iloc[book_id,:].values.reshape(1,-1), n_neighbors=100 )

    poster_url = fetch_poster_(suggestion)
    
    for i in range(len(suggestion)):
            books = book_pivot_table.index[suggestion[i]]
            for j in books:
                books_list.append(j)
    return books_list , poster_url  
#book_name=book_namess[0]
combined_index = pd.Index(book_names.tolist() + book_namess.tolist())


selected_books = st.selectbox(
    "Type or select a book from the dropdown",
    combined_index
)

if st.button('Show Recommendation'):
    try:
        recommended_books,poster_url = recommend_book(selected_books)
    except Exception as e:
        print("genre")
        recommended_books,poster_url = recommend_book_(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])
    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])

    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])
    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])
    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])