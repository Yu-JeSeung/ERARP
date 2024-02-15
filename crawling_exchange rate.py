# 네이버 주식 크롤링 시작
import os
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# 오늘의 날짜를 가져옵니다.
today = datetime.now().strftime('%Y-%m-%d')

# 현재 위치의 data 폴더에 파일을 저장합니다.
folder_path = 'data'

# data 폴더가 존재하지 않는 경우 생성합니다.
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 저장할 파일의 경로를 만듭니다.
file_path = os.path.join(folder_path, f'exchange_rates_{today}.csv')

# 웹 페이지의 URL을 가져옵니다.
url = 'https://finance.naver.com/marketindex/exchangeList.naver'

# requests 모듈을 사용하여 URL에 GET 요청을 보냅니다.
response = requests.get(url)

# 요청이 성공했는지 확인합니다.
if response.status_code == 200:
    # BeautifulSoup을 사용하여 HTML을 파싱합니다.
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
else:
    print('페이지를 찾을 수 없습니다.')
