import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 데이터가 있는 폴더 경로
folder_path = 'data'

# 폴더 내의 모든 CSV 파일을 읽습니다.
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 모델 초기화
model = LinearRegression()

# 모든 CSV 파일에 대해 반복하여 모델을 학습합니다.
for file_name in csv_files:
    # CSV 파일의 전체 경로
    file_path = os.path.join(folder_path, file_name)
    
    # 데이터 로드
    data = pd.read_csv(file_path)
    
    # 데이터 전처리
    data['금액'] = data['금액'].str.replace(',', '').astype(float)
    data_encoded = pd.get_dummies(data, columns=['국가명'])
    print(data_encoded)
    # 특성과 타겟 데이터 분리
    X = data_encoded.drop(columns=['금액'])
    y = data_encoded['금액']
    
    # 학습용과 테스트용 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 모델 학습
    model.fit(X_train, y_train)
    
    # 모델 평가
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)



# # 테스트
# input_country = '미국 USD'  # 예측하고 싶은 국가명
# test_data = pd.DataFrame([[0] * len(X.columns)], columns=X.columns)

# # 국가명 인코딩
# test_data[f'국가명_{input_country}'] = 1

# # 예측
# predicted_rate = model.predict(test_data)
# print(f'{input_country} 의 예상 환율: {predicted_rate[0]}')
