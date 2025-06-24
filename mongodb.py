from pymongo import MongoClient
import logging

def save_to_mongodb(data):
  client = MongoClient("mongodb://localhost:27017/")
  db = client["movie"]
  collection = db["reviews"]

  collection.delete_many({})
  logging.info("기존 데이터 삭제 완료!")

  if data:
    collection.insert_many(data)
    logging.info(f"데이터 {len(data)}건 저장 완료!")
  else:
    logging.warning("저장할 데이터가 없습니다.")
