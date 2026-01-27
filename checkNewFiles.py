import os, time #os와 time 모듈을 가져옵니다.
DIR_PATH= '/Users/kimgwanhun/Desktop/Pictures/밤부/26-1/가두모집/인생네컷/photos' #DIR_PATH 변수에 디렉토리 경로 'static'을 저장합니다.
# pre_file = set(os.listdir(DIR_PATH)) #os.listdir(DIR_PATH)를 사용하여 'static' 디렉토리의 파일 리스트를 가져오고, 이를 set으로 변환하여 pre_file 변수에 저장합니다. set형은 중복허용이 되지 않는다는 특징이 있습니다.
# print(pre_file) # pre_file을 출력하여 초기 파일 리스트를 확인합니다.

def checkNewFiles(pre_file):
    cureent_file = set(os.listdir(DIR_PATH)) # os.listdir(DIR_PATH)를 사용하여 현재 시점의 파일 리스트를 가져오고, 이를 set으로 변환하여 cureent_file 변수에 저장합니다.
    result_diff = cureent_file - pre_file #cureent_file - pre_file은 현재 시점에서 새로 추가된 파일들의 집합을 result_diff에 저장합니다. 이 연산은 cureent_file에서 pre_file에 없는 파일들을 찾는 것을 의미합니다. 
   
    for file_name in result_diff:
        print(f"새로운 파일 탐지 : {file_name} ")  #result_diff에 있는 각 파일에 대해 반복하여, 새로운 파일을 탐지하면 그 파일 이름을 출력합니다.
    pre_file = cureent_file  #pre_file을 cureent_file로 갱신하여 다음 반복 시 현재 파일 리스트를 기준으로 비교할 수 있게 합니다.
    print("확인!!")
    return pre_file