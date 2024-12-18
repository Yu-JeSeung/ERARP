import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 데이터가 있는 폴더 경로
folder_path = 'data'

# 폴더 내의 모든 CSV 파일을 읽습니다.
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 데이터를 저장할 빈 DataFrame 생성
all_data = pd.DataFrame()

# 모든 CSV 파일을 순회하면서 데이터를 합칩니다.
for file_name in csv_files:
    # CSV 파일의 전체 경로
    file_path = os.path.join(folder_path, file_name)
    
    # CSV 파일을 데이터프레임으로 읽어옵니다.
    data = pd.read_csv(file_path)
    
    # 데이터프레임을 all_data에 추가합니다.
    all_data = pd.concat([all_data, data], ignore_index=True)

# 데이터 전처리
all_data['금액'] = all_data['금액'].str.replace(',', '').astype(float)  # 쉼표 제거 후 실수형으로 변환
data_encoded = pd.get_dummies(all_data, columns=['국가명'])

# 특성과 타겟 데이터 분리
X = data_encoded.drop(columns=['금액'])
y = data_encoded['금액']

# 학습용과 테스트용 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 초기화
model = LinearRegression()

# 모델 학습
model.fit(X_train, y_train)

# 모델 평가
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

# 입력값 설정
input_country = input("예측하고 싶은 국가명을 입력하세요 (예: 미국 USD): ")
# 미국 USD, 유럽연합 EUR, 일본 JPY (100엔), 홍콩 HKD, 대만 TWD 등

# 입력된 국가명에 해당하는 열 검색
input_data = data_encoded[data_encoded[f'국가명_{input_country}'] == 1].drop(columns=['금액'])

# 결과 예측
predicted_rate = model.predict(input_data)

# 예측 결과 출력
print(f'{input_country}의 예상 환율: {predicted_rate[0]}')
