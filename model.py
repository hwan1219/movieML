from pymongo import MongoClient
import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# https://adoptium.net/temurin/releases/?os=any&arch=any&version=11

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
  lr_model = LogisticRegression(max_iter=1000, class_weight='balanced')
  rf_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
  
  nb_model.fit(x_train_sm, y_train_sm)
  lr_model.fit(x_train_sm, y_train_sm)
  rf_model.fit(x_train_sm, y_train_sm)
  
  nb_pred = nb_model.predict(x_test)
  lr_pred = lr_model.predict(x_test)
  rf_pred = rf_model.predict(x_test)
  
  print(f"NaiveBayes Accuracy: {accuracy_score(y_test, nb_pred)}")
  print(f"NaiveBayes report:\n{confusion_matrix(y_test, nb_pred)}")
  
  print(f"LogisticRegression Accuracy: {accuracy_score(y_test, lr_pred)}")
  print(f"LogisticRegression report:\n{confusion_matrix(y_test, lr_pred)}")
  
  print(f"RandomForest Accuracy: {accuracy_score(y_test, rf_pred)}")
  print(f"RandomForest report:\n{confusion_matrix(y_test, rf_pred)}")

model_classification()