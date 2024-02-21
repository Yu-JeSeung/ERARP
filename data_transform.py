import pandas as pd

# 데이터 로드
n_data = pd.read_csv('data/exchange_rates_2024-02-19.csv')

# 필요없는 3열부터 다 삭제
n_data = n_data.iloc[:, :2]

# 데이터가 너무 많으니 4행까지만 남기기
n_data.drop(index=n_data.index[5:], inplace=True)

# 미국 값을 저장
usd_value = n_data.iloc[0, 1]

# 헤더에 미국 USD 추가
n_data.loc[-1] = ['미국 USD', usd_value]
n_data.index = n_data.index + 1
n_data.sort_index(inplace=True)

# 열 헤더 수정
n_data.columns = ['국가명', '금액']

# 수정된 파일 덮어쓰기
# n_data.to_csv('data/exchange_rates_2024-02-15.csv', index=False)

print(n_data)

