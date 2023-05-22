#######################################################################################################################
from os import name, replace
from re import I, M
from this import d
from turtle import end_fill
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from tkinter import *
from tkinter import filedialog


import chromedriver_autoinstaller # 크롬 버전 업그레이드 되도 자동으로 설치
import subprocess
import time
import pandas
import sys
import numpy
#######################################################################################################################
current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
print(current_time)

subprocess.Popen('C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")


chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    browser = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    browser = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
browser.implicitly_wait(10)
# 크롬 설치위치 확인 후 디버거모드로 접속 ( 봇탐지 우회 )
# 추가적으로 봇 확인하는건 보통 자바스크립트가 실행되었는지 확인 ( 사람이 할 경우에는 키보드나 마우스 사용, 자바스크립트 안씀)
#######################################################################################################################
browser.maximize_window() # 창 최대화
browser.get("http://www.logichome.org/g5/bbs/board.php?bo_table=logics_01&wr_id=101289&sfl=wr_subject&sst=wr_10&sod=desc&sop=and&page=1")

# http://www.logichome.org/g5/bbs/board.php?bo_table=logics_01&wr_id=101289&sfl=wr_subject&sst=wr_10&sod=desc&sop=and&page=1 : 산책댕댕이 ( 이거 13오류생김 확인필요 )
# http://www.logichome.org/g5/bbs/board.php?bo_table=logics_01&wr_id=109833&sfl=wr_subject&stx=%EC%82%BC&sop=and : 삼괴권 ( 현재까지 특이사항 없음 )


browser.implicitly_wait(10)
#######################################################################################################################

# 1. 행,열 개수 찾기 2차원 list 선언 ( 최초 1회 )
column_xpath = '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/section[1]/article/div[2]/div[2]/section/div[3]/table/tbody/tr[1]' #/td[2~n] 추가
row_xpath = '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/section[1]/article/div[2]/div[2]/section/div[3]/table/tbody' # /tr[2~n]/td[1] 추가
nemo_xpath = '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/section[1]/article/div[2]/div[2]/section/div[3]/table/tbody' # /tr[2~2+row_num]/td[2~2+column_num] 추가

for i in range(2,99):
    try: 
        browser.find_element_by_xpath(f'{column_xpath}/td[{i}]').is_enabled()
    except:
        column_num = i-2 # 2부터 시작했으니까 총 갯수는 i-2
        break
for i in range(2,99):
    try:
        browser.find_element_by_xpath(f'{row_xpath}/tr[{i}]/td[1]').is_enabled()
    except:
        row_num = i-2 # 2부터 시작했으니까 총 갯수는 i-2
        break

row_text_list = [[]*1 for _ in range(row_num)]
row_text_check_list = [[]*1 for _ in range(row_num)]
row_text_del_list = [[]*1 for _ in range(row_num)]
row_sum_list = list()

column_text_list = [[]*1 for _ in range(column_num)]
column_text_check_list = [[]*1 for _ in range(column_num)]
column_text_del_list = [[]*1 for _ in range(column_num)]
column_sum_list = list()
#######################################################################################################################
# 2. 열,행의 inner text를 2차원 리스트로 정리 ( 최초 1회 )
for i in range(column_num):
    column_sum = 0
    column_xpath_text_i = browser.find_element_by_xpath(f'{column_xpath}/td[{i+2}]').get_attribute('innerText')
    column_xpath_text_i = str(column_xpath_text_i).split()
    for j in range(len(column_xpath_text_i)):
        if len(column_xpath_text_i) > 0:
            column_text_list[i].append(column_xpath_text_i[j])
            column_text_check_list[i].append(column_xpath_text_i[j])
            column_text_del_list[i].append(column_xpath_text_i[j])
            column_sum += int(column_xpath_text_i[j])
        else:
            column_text_list[i].append(column_xpath_text_i[j])
            column_text_check_list[i].append(column_xpath_text_i[j])
            column_text_del_list[i].append(column_xpath_text_i[j])
            column_sum = 0
    column_sum_list.append(column_sum)
for i in range(row_num): # row는 공백없이 행별로 문자열 연결되서 나옴 ( 두자릿수 구분안됨 ) -> innerHTML로 해서 div없애놓고 <span>,</span>을 /로 바꾸고 -> / 기준으로 문자열 쪼갬
    row_sum = 0
    row_xpath_text_i = browser.find_element_by_xpath(f'{row_xpath}/tr[{i+2}]/td[1]/div').get_attribute('innerHTML')
    row_xpath_text_i = str(row_xpath_text_i).replace('<span>','/')
    row_xpath_text_i = str(row_xpath_text_i).replace('</span>','/')
    row_xpath_text_i = row_xpath_text_i.split('/')
    for j in range(len(row_xpath_text_i)):
        if row_xpath_text_i[j] == '':
            pass
        else:
            if len(row_xpath_text_i) > 0:
                row_text_list[i].append(row_xpath_text_i[j])
                row_text_check_list[i].append(row_xpath_text_i[j])
                row_text_del_list[i].append(row_xpath_text_i[j])
                row_sum += int(row_xpath_text_i[j])
            else:
                row_text_list[i].append(row_xpath_text_i[j])
                row_text_list[i].append(row_xpath_text_i[j])
                row_text_check_list[i].append(row_xpath_text_i[j])
                row_text_del_list[i].append(row_xpath_text_i[j])
                row_sum = 0
    row_sum_list.append(row_sum)
###########################################################################################################################################################

row_count = 0
for i in range(row_num):
    row_count += len(row_text_list[i])

column_count = 0
for i in range(column_num):
    column_count += len(column_text_list[i])

# 3. 행, 열 빈곳이나 최대값이 있는지 확인 ( 최초 1회 )
for i in range(row_num):  # i는 행의 갯수만큼 반복
    if len(row_text_list[i]) == 0: # 행에서 숫자가 없다면 행 전부 우클릭
        for j in range(column_num):
            ActionChains(browser).context_click(browser.find_element_by_xpath(f'{nemo_xpath}/tr[{i+2}]/td[{j+2}]')).perform()
    else:
        pass
    
    if len(row_text_list[i]) == 1 and row_text_list[i][0] == str(column_num): # 행에 있는 유일한 값이 열 갯수와 동일하다면 행 전부 좌클릭
        for j in range(column_num):
            browser.find_element_by_xpath(f'{nemo_xpath}/tr[{i+2}]/td[{j+2}]').click()
        row_text_check_list[i][0] = '0'
        del row_text_del_list[i][0] # 다 채워진 놈은 제거
    else:
        pass
for i in range(column_num):  # i는 열의 갯수만큼 반복
    if len(column_text_list[i]) == 0: # 열에서 숫자가 없다면 행 전부 우클릭
        for j in range(row_num):
            cell_status = browser.find_element_by_xpath(f'{nemo_xpath}/tr[{j+2}]/td[{i+2}]').get_attribute('class')
            if "marked" in cell_status or "checked" in cell_status: # == True 없이 사용해야 continue로 빠짐 ( 왼쪽버튼 : checked , 오른쪽버튼 : marked )
                pass
            else:
                ActionChains(browser).context_click(browser.find_element_by_xpath(f'{nemo_xpath}/tr[{j+2}]/td[{i+2}]')).perform() # perform이 하얀색인디 되넹.. ( 오른쪽버튼 AtctionChains는 조금 느림 )
    else:
        pass
    
    if len(column_text_list[i]) == 1 and column_text_list[i][0] == str(row_num): # 열에 있는 유일한 값이 열 갯수와 동일하다면 행 전부 좌클릭
        for j in range(row_num):
            cell_status = browser.find_element_by_xpath(f'{nemo_xpath}/tr[{j+2}]/td[{i+2}]').get_attribute('class')
            if "marked" in cell_status or "checked" in cell_status: # == True 없이 사용해야 continue로 빠짐 ( 왼쪽버튼 : checked , 오른쪽버튼 : marked )
                pass
            else:
                browser.find_element_by_xpath(f'{nemo_xpath}/tr[{j+2}]/td[{i+2}]').click()
        column_text_check_list[i][0] = '0'
        del column_text_del_list[i][0] # 다 채워진 놈은 제거
    else:
        pass
###########################################################################################################################################################
# 4. 열에서 빈곳이나 최대값이 있는지 확인 ( 최초 1회 )
    if len(column_text_list[i]) == 0: # 열에서 숫자가 없다면 행 전부 우클릭
        for j in range(row_num):
            cell_status = browser.find_element_by_xpath(f'{nemo_xpath}/tr[{j+2}]/td[{i+2}]').get_attribute('class')
            if "marked" in cell_status or "checked" in cell_status: # == True 없이 사용해야 continue로 빠짐 ( 왼쪽버튼 : checked , 오른쪽버튼 : marked )
                pass
            else:
                ActionChains(browser).context_click(browser.find_element_by_xpath(f'{nemo_xpath}/tr[{j+2}]/td[{i+2}]')).perform() # perform이 하얀색인디 되넹.. ( 오른쪽버튼 AtctionChains는 조금 느림 )
    else:
        pass
    
    if len(column_text_list[i]) == 1 and column_text_list[i][0] == str(row_num): # 열에 있는 유일한 값이 열 갯수와 동일하다면 행 전부 좌클릭
        for j in range(row_num):
            cell_status = browser.find_element_by_xpath(f'{nemo_xpath}/tr[{j+2}]/td[{i+2}]').get_attribute('class')
            if "marked" in cell_status or "checked" in cell_status: # == True 없이 사용해야 continue로 빠짐 ( 왼쪽버튼 : checked , 오른쪽버튼 : marked )
                pass
            else:
                browser.find_element_by_xpath(f'{nemo_xpath}/tr[{j+2}]/td[{i+2}]').click()
        del column_text_list[i][0] # 다 채워진 놈은 제거
    else:
        pass

###########################################################################################################################################################
# 4. 속도를 위해 temp_list는 빈곳, 최대값 확인 후 최초 1회만
row_status_temp_list = [[]*1 for _ in range(row_num)] # 이놈은 체크모양 담기
column_status_temp_list = [[]*1 for _ in range(column_num)] # 이놈은 체크모양 담기

for i in range(row_num): # 현재 행 업데이트    
    for j in range(column_num): # 열만큼 반복해서 한줄 만들고
        cell_status = browser.find_element_by_xpath(f'{nemo_xpath}/tr[{i+2}]/td[{j+2}]').get_attribute('class')
        if 'marked' in cell_status:
            row_status_temp_list[i].append('X')
        elif 'checked' in cell_status:
            row_status_temp_list[i].append('■')
        else: # 체크안됨
            row_status_temp_list[i].append('□')

for i in range(column_num): # 현재 열 업데이트    
    for j in range(row_num): # 열만큼 반복해서 한줄 만들고
        cell_status = browser.find_element_by_xpath(f'{nemo_xpath}/tr[{j+2}]/td[{i+2}]').get_attribute('class')
        if 'marked' in cell_status:
            column_status_temp_list[i].append('X')
        elif 'checked' in cell_status:
            column_status_temp_list[i].append('■')
        else: # 체크안됨
            column_status_temp_list[i].append('□')
###########################################################################################################################################################
# 아래처럼 def하면 row -> column 넘어갈때 column temp_list가 변경이 안됨
# row할때 column도 같이 지워야됨 ( column할때 row도 같이 지워야됨 )
def status_update(row_num,column_num,row_status_temp_list,column_status_temp_list):
    row_status_list = [[]*1 for _ in range(row_num)] # checked 99 , marked 0
    column_status_list = [[]*1 for _ in range(column_num)] # 이놈은 체크된거 1로
    for i in range(row_num):
        row_status_index = 0
        for j in range(column_num):          
            if row_status_temp_list[i][j] == '□': # 비어있으면
                row_status_index += 1
            elif row_status_temp_list[i][j] == 'X':
                if row_status_index == 0: # 초장부터 marked면 1만 넣어야됨
                    row_status_list[i].append('0')
                    row_status_index = 0
                else:
                    row_status_list[i].append(f'{row_status_index}')
                    row_status_list[i].append('0')
                    row_status_index = 0
            elif row_status_temp_list[i][j] == '■':
                if row_status_index == 0: # 초장부터 checked면 1만 넣어야됨
                    row_status_list[i].append('99')
                    row_status_index = 0
                else:
                    row_status_list[i].append(f'{row_status_index}')
                    row_status_list[i].append('99')
                    row_status_index = 0
        if row_status_index == 0: # 마지막값이 0이면 추가할 필요 없음 ( 마지막 print로 확인하면 안나온 이유가 continue되서 출력을 안함 )
            pass
        else:
            row_status_list[i].append(f'{row_status_index}')

    for i in range(column_num):
        column_status_index = 0
        for j in range(row_num):
            if column_status_temp_list[i][j] == '□': # 비어있으면
                column_status_index += 1
            elif column_status_temp_list[i][j] == 'X':
                if column_status_index == 0: # 초장부터 checked or marked면 1만 넣어야됨
                    column_status_list[i].append('0')
                    column_status_index = 0
                else: 
                    column_status_list[i].append(f'{column_status_index}')
                    column_status_list[i].append('0')
                    column_status_index = 0
            elif column_status_temp_list[i][j] == '■':
                if column_status_index == 0: # 초장부터 checked or marked면 1만 넣어야됨
                    column_status_list[i].append('99')
                    column_status_index = 0
                else: 
                    column_status_list[i].append(f'{column_status_index}')
                    column_status_list[i].append('99')
                    column_status_index = 0
        if column_status_index == 0: # 마지막값이 0이면 추가할 필요 없음 ( 마지막 print로 확인하면 안나온 이유가 continue되서 출력을 안함 )
            pass
        else:
            column_status_list[i].append(f'{column_status_index}')

    return row_status_list, column_status_list

update_result = status_update(row_num,column_num,row_status_temp_list,column_status_temp_list); row_status_list = update_result[0]; column_status_list = update_result[1]
while_count = 0
row_check_count = 0
column_check_count = 0


# while True:
#     while_count += 1
for i in range(row_num):
    row_check_count += row_text_check_list[i].count('0')
for i in range(column_num):
    column_check_count += column_text_check_list[i].count('0')

# if row_count == row_check_count and column_count == column_check_count:
#     break
# else:
#     pass

# 갯수가 애초에 몇개였는지 확인필요

for i in range(row_num): # 첫번째, 마지막 인덱스가 채워져있는지
    if len(row_text_del_list[i]) == 0:
        continue # pass하면 밑으로 가고 continue는 재낌
    else:
        if row_status_temp_list[i][0] == '■' and row_text_check_list[i][0] != '0' : # 첫번째 Index가 채워졌는가? and 첫번째 text가 이미 체크되었는가?
            text_value = row_text_check_list[i][0]
            for j in range(int(text_value)):
                if row_status_temp_list[i][j] == '■':
                    pass
                else:
                    browser.find_element_by_xpath(f'{nemo_xpath}/tr[{i+2}]/td[{j+2}]').click()
                    row_status_temp_list[i][j] = '■'
                    column_status_temp_list[j][i] = '■'
            if row_status_temp_list[i][int(text_value)] == 'X':
                pass
            else:
                ActionChains(browser).context_click(browser.find_element_by_xpath(f'{nemo_xpath}/tr[{i+2}]/td[{int(text_value)+2}]')).perform()
                row_status_temp_list[i][int(text_value)] = 'X'
                column_status_temp_list[int(text_value)][i] = 'X'
            row_text_check_list[i][0] = '0' # 수행완료되면 첫번째 index 0으로 변경
            del row_text_del_list[i][0]
        else:
            pass

        if row_status_temp_list[i][-1] == '■' and row_text_check_list[i][-1] != '0':
            text_value = row_text_check_list[i][-1]
            for j in range(int(text_value)):
                if row_status_temp_list[i][column_num-1-j] == '■':
                    pass
                else:
                    browser.find_element_by_xpath(f'{nemo_xpath}/tr[{i+2}]/td[{2+column_num-1-j}]').click()
                    row_status_temp_list[i][column_num-1-j] = '■'
                    column_status_temp_list[column_num-1-j][i] = '■'
            if row_status_temp_list[i][column_num-1-int(text_value)] == 'X':
                pass
            else:
                ActionChains(browser).context_click(browser.find_element_by_xpath(f'{nemo_xpath}/tr[{i+2}]/td[{2+column_num-1-int(text_value)}]')).perform()
                row_status_temp_list[i][column_num-1-int(text_value)] = 'X'
                column_status_temp_list[column_num-1-int(text_value)][i] = 'X'
            row_text_check_list[i][-1] = '0' # 수행완료되면 첫번째 index 0으로 변경
            del row_text_del_list[i][-1]
        else:
            pass
update_result = status_update(row_num,column_num,row_status_temp_list,column_status_temp_list); row_status_list = update_result[0]; column_status_list = update_result[1]

for i in range(column_num): # 첫번째, 마지막 인덱스가 채워져있는지
    if len(column_text_del_list[i]) == 0:
        continue # pass하면 밑으로 가고 continue는 재낌
    else:
        if column_status_temp_list[i][0] == '■' and column_text_check_list[i][0] != '0' : # 첫번째 Index가 채워졌는가? and 첫번째 text가 이미 체크되었는가?
            text_value = column_text_check_list[i][0]
            for j in range(int(text_value)):
                if column_status_temp_list[i][j] == '■':
                    pass
                else:
                    browser.find_element_by_xpath(f'{nemo_xpath}/tr[{j+2}]/td[{i+2}]').click()
                    column_status_temp_list[i][j] = '■'
                    row_status_temp_list[j][i] = '■'
            if column_status_temp_list[i][int(text_value)] == 'X':
                pass
            else:
                ActionChains(browser).context_click(browser.find_element_by_xpath(f'{nemo_xpath}/tr[{int(text_value)+2}]/td[{i+2}]')).perform()
                column_status_temp_list[i][int(text_value)] = 'X'
                row_status_temp_list[int(text_value)][i] = 'X'
            column_text_check_list[i][0] = '0' # 수행완료되면 첫번째 index 0으로 변경
            del column_text_del_list[i][0]
        else:
            pass

        if column_status_temp_list[i][-1] == '■' and column_text_check_list[i][-1] != '0':
            text_value = column_text_check_list[i][-1]
            for j in range(int(text_value)):
                if column_status_temp_list[i][row_num-1-j] == '■':
                    pass
                else:
                    browser.find_element_by_xpath(f'{nemo_xpath}/tr[{2+row_num-j-1}]/td[{i+2}]').click()
                    column_status_temp_list[i][row_num-1-j] = '■'
                    row_status_temp_list[row_num-1-j][i] = '■'
            if column_status_temp_list[i][row_num-1-int(text_value)] == 'X':
                pass
            else:
                ActionChains(browser).context_click(browser.find_element_by_xpath(f'{nemo_xpath}/tr[{2+row_num-1-int(text_value)}]/td[{i+2}]')).perform()
                column_status_temp_list[i][row_num-1-int(text_value)] = 'X'
                row_status_temp_list[row_num-1-int(text_value)][i] = 'X'
            column_text_check_list[i][-1] = '0' # 수행완료되면 첫번째 index 0으로 변경
            del column_text_del_list[i][-1]
        else:
            pass
        
update_result = status_update(row_num,column_num,row_status_temp_list,column_status_temp_list); row_status_list = update_result[0]; column_status_list = update_result[1]
for i in range(row_num): # 다 체크된 곳은 빈곳 marked 처리
    if row_sum_list[i] == row_status_temp_list[i].count('■'):
        for j in range(column_num):
            if row_status_temp_list[i][j] == '□':
                ActionChains(browser).context_click(browser.find_element_by_xpath(f'{nemo_xpath}/tr[{i+2}]/td[{j+2}]')).perform()
                row_status_temp_list[i][j] = 'X'
                column_status_temp_list[j][i] = 'X'
            else:
                pass
        for j in range(len(row_text_list[i])):
            row_text_check_list[i][j] = '0'
        row_text_del_list[i].clear()
    else:
        continue             

update_result = status_update(row_num,column_num,row_status_temp_list,column_status_temp_list); row_status_list = update_result[0]; column_status_list = update_result[1]
for i in range(column_num): # 다 체크된 곳은 빈곳 marked 처리
    if column_sum_list[i] == column_status_temp_list[i].count('■'):
        for j in range(row_num):
            if column_status_temp_list[i][j] == '□':
                ActionChains(browser).context_click(browser.find_element_by_xpath(f'{nemo_xpath}/tr[{j+2}]/td[{i+2}]')).perform()
                column_status_temp_list[i][j] = 'X'
                row_status_temp_list[j][i] = 'X'
            else:
                pass
        for j in range(len(column_text_list[i])):
            column_text_check_list[i][j] = '0'
        column_text_del_list[i].clear()
    else:
        continue   

update_result = status_update(row_num,column_num,row_status_temp_list,column_status_temp_list); row_status_list = update_result[0]; column_status_list = update_result[1]
for i in range(row_num): # 1개짜리 조지기
    text_value = row_text_del_list[i][0]
    one_index = row_text_list[i].index(text_value)
    checked_text_sum = 0
    checked_status_sum = 0
    checked_sum_index = 0
    checked_start_index = 0
    checked_end_index = column_num-1
    for j in range(one_index):
        checked_text_sum += int(row_text_list[i][j])
    if len(row_text_del_list) == 1 and row_text_list[i].count(text_value): # del list 1개만 남아있고, 중복값이 없을때만
        for j in range(column_num):
            if checked_status_sum == checked_text_sum:
                checked_sum_index = j 
            else:
                pass

            if row_status_temp_list == 'X':
                continue
            else:
                checked_status_sum += 1 


        for j in range(column_num-checked_sum_index):
            if row_status_temp_list[i][j+checked_sum_index] == 'X':
                continue
            else:
                checked_start_index = j
    else:
        continue
    # start_index 확인

    for j in range(column_num-checked_start_index):
        if row_status_temp_list[i][j+checked_start_index] == 'X':
            checked_end_index = j
            break
        else:
            pass
    # end_index 확인
    
    # if row_status_temp_list[i][j] == '■':
    #     for j in range()
    
    
    # for j in range(checked_start_index,checked_end_index): # index 시작이 99일 경우 / index 끝이 99일 경우 -> 갯수만큼 채우면됨
        
        
    #     elif row_status_temp_list[i][]
    #     pass
    


#   'X'
    
#   '■'
        
#   '□'