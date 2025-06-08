import pandas as pd
import numpy as np
import re

def preprocess_data(raw_data):
  df = pd.DataFrame(raw_data)
  
  df.replace('', np.nan, inplace=True)
  
  def extract_score(value):
    if pd.notna(value):
      m = re.search(r'(\d+)$', str(value))
      return float(m.group(1)) if m else np.nan
    else:
      return np.nan
  df['score'] = df['score'].apply(extract_score)
  df = df.dropna(subset=['score'])

  df['text'] = (
    df['text']
    .fillna('리뷰 없음')
  )
  df['text'] = (
    df['text']
    .str.replace(r'[^\w\s가-힣]', '', regex=True)
    .str.strip()
  )

  df['date'] = pd.to_datetime(df['date'], errors='coerce')
  df['date'] = (
    df.groupby('title')['date']
    .transform(lambda x: x.fillna(max(x)))
  )
  df['date'] = (
    df['date']
    .fillna('')
    .dt.strftime('%Y-%m-%d')
  )

  df["positive"] = df["positive"].fillna("0")
  df["negative"] = df["negative"].fillna("0")

  return df.to_dict(orient='records')