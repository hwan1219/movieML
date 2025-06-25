from pymongo import MongoClient
import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import streamlit as st

def model_classification():
  client = MongoClient('mongodb://localhost:27017/')
  db = client['movie']
  collection = db['reviews']

  data = pd.DataFrame(list(collection.find()))
  data = data.drop('_id', axis=1)

  def label_encoding(score):
    if score >= 7:
      return 1
    else:
      return 0
  data['label'] = data['score'].apply(label_encoding)
  data = data.dropna(subset=['label'])

  okt = Okt()
  stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
  
  def preprocess(text):
    # 형태소 분석
    tokens = okt.morphs(text, stem=True)
    # 불용어 제거
    tokens = [word for word in tokens if not word in stopwords]
    return ' '.join(tokens)
  data['cleaned_text'] = data['text'].apply(preprocess)
  
  tfidf = TfidfVectorizer(max_features=1000)
  x = tfidf.fit_transform(data['cleaned_text'])
  y = data['label'].astype(int).values
  
  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42, stratify=y)
  
  smote = SMOTE(random_state=42, k_neighbors=3)
  x_train_sm, y_train_sm = smote.fit_resample(x_train, y_train)
  
  nb_model = MultinomialNB()
  nb_model.fit(x_train_sm, y_train_sm)
  
  return nb_model, tfidf, okt, stopwords

nb_model, tfidf, okt, stopwords = model_classification()

def preprocess(text, okt, stopwords):
  tokens = okt.morphs(text, stem=True)
  tokens = [word for word in tokens if not word in stopwords]
  return ' '.join(tokens)

st.title("리뷰 감성 분류기")
user_input = st.text_area("리뷰 텍스트를 입력하세요")

if st.button("분류하기"):
  clean_text = preprocess(user_input, okt, stopwords)
  x = tfidf.transform([clean_text])
  pred = nb_model.predict(x)[0]
  result = "긍정 리뷰" if pred == 1 else "부정 리뷰"
  st.write(f"분류 결과: {result}")