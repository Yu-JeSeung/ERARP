import os
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pandas as pd

def crawl_and_modify_exchange_rates():
    # 오늘 날짜 로드
    today = datetime.now().strftime('%Y-%m-%d %H')

    # data 폴더에 파일저장
    folder_path = 'data'

    # 저장할 파일 경로 생성
    file_path = os.path.join(folder_path, f'exchange_rates_{today}.csv')

    # 환율 URL
    url = 'https://finance.naver.com/marketindex/exchangeList.naver'

    # requests 모듈을 사용하여 URL에 GET 요청을 보냅니다.
    response = requests.get(url)

    # 요청이 성공했는지 확인
    if response.status_code == 200:
        # BeautifulSoup을 사용하여 HTML을 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 환율 정보가 담긴 테이블을 찾습니다.
        exchange_table = soup.find('table', class_='tbl_exchange')

        # 파일에 데이터를 저장하기 위해 CSV 파일을 엽니다.
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            # CSV 파일을 작성하기 위해 writer 객체를 생성합니다.
            writer = csv.writer(csvfile)
            
            # 테이블 내의 각 행을 찾습니다.
            rows = exchange_table.find_all('tr')

            # 각 행의 데이터를 가져와 CSV 파일에 씁니다.
            for row in rows:
                # 행의 각 셀을 가져옵니다.
                cells = row.find_all('td')
                
                # 셀의 데이터를 CSV 파일에 씁니다.
                row_data = [cell.text.strip() for cell in cells]
                writer.writerow(row_data)
                
        print(f'CSV 파일 {file_path}로 저장되었습니다.')

        # 데이터 로드
        n_data = pd.read_csv(file_path)

        # 필요없는 3열부터 다 삭제
        n_data = n_data.iloc[:, :2]

        # 데이터가 너무 많으니 4행까지만 남기기
        # n_data.drop(index=n_data.index[5:], inplace=True)

        # 미국 값을 저장
        usd_value = n_data.iloc[0, 1]

        # 헤더에 미국 USD 추가
        n_data.loc[-1] = ['미국 USD', usd_value]
        n_data.index = n_data.index + 1
        n_data.sort_index(inplace=True)

        # 열 헤더 수정
        n_data.columns = ['국가명', '금액']

        # 수정된 파일 덮어쓰기
        n_data.to_csv(file_path, index=False)

        # 결과 출력
        print(n_data)
    else:
        print('페이지를 찾을 수 없습니다.')

# 함수 호출
crawl_and_modify_exchange_rates()
