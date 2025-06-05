import pandas as pd

def preprocess_data(raw_data):
  df = pd.DataFrame(raw_data)
  
  try:
    df['score'] = (
      df['score']
      .str.extract(r'(\d+)$')[0]
      .astype(float)
    )
    df['score'] = (
      df.groupby('title')['score']
      .transform(lambda x: x.fillna(round(x.mean()))))

    df['text'] = (
      df['text']
      .fillna('리뷰 없음')
    )
    df['text'] = (
      df['text']
      .str.replace(r'[^\w\s가-힣]', '', regex=True)
      .str.strip()
    )

    df['date'] = (
      df.groupby('title')['date']
      .transform(lambda x: x.fillna(max(x)))
    )
    df['date'] = (
      df['date']
      .fillna('')
      .str.split().str[0]
      .str.rstrip('.')
    )

    df["positive"] = df["positive"].fillna("0")
    df["negative"] = df["negative"].fillna("0")

    return df.to_dict(orient='records')
  
  except Exception as e:
    print(f"전처리 중 오류 발생: {e}")
    return []