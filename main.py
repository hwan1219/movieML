from crawler import crawl_reviews
from preprocess import preprocess_data
from mongodb import save_to_mongodb
import logging
import traceback

logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
  try:
    raw_data = crawl_reviews()
    logging.info("크롤링 완료!")

    clean_data = preprocess_data(raw_data)
    logging.info("전처리 완료!")

    save_to_mongodb(clean_data)
    logging.info("MongoDB 저장 완료!")

  except Exception as e:
    logging.error(f"[ERROR] main.py에서 오류 발생: {e}")
    logging.error(traceback.format_exc())
    
if __name__ == "__main__":
  main()