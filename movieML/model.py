from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from konlpy.tag import Okt
import re
import pickle

# okt = OKt()
# https://wikidocs.net/44249