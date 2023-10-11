import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.title('Book recommender')

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

#user_input = st.text_input('Enter the name of the book: ')
user_input = st.selectbox('Search your favourite book', list(popular_df['Book-Title'].values))

def display_images(data):
	images = list(data['Image-URL-M'].values)
	book_names = list(popular_df['Book-Title'].values)
	#displaying only 3 rows and each row has 5 columns
	display_grid = [st.columns(5) for _ in range(3)]
	k = 0
	for i in range(3):
		for j in range(5):
			with display_grid[i][j]:
				st.image(images[k])
				st.text(book_names[k])
				k += 1
if not user_input:
	display_images(popular_df)

def recommend(book_name):
	print(book_name)
	index = np.where(pt.index==book_name)[0][0]
	similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x:x[1], reverse=True)[1:5]
	data = []
	for i in similar_items:
	    item = []
	    temp_df = books[books['Book-Title'] == pt.index[i[0]]]
	    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
	    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
	    item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
	    
	    data.append(item)
	print(data)
	return data

if user_input:
	data = recommend(user_input)
	recommendation_grid = [st.columns(4) for _ in range(1)]
	k = 0
	for i in range(1):
		for j in range(4):
			with recommendation_grid[i][j]:
				st.image(data[k][2])
				st.text(data[k][0])
				k += 1

