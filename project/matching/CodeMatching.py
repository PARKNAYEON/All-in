'''

CodeMatching.py
(기업코드6자리).KS 형태로 저장되어 있는 데이터들을 기업 코드에 맞는 기업 명으로 매칭하는 작업

def code_dict(dictionary) : 코드-기업명 딕셔너리 생성
def code_matching(df,code) : 매칭하는 함수

'''

def code_dict(dictionary):
    data=open('기업코드.txt','r',encoding='UTF8')
    line=data.readlines()
    data.close()
    code_key=[]
    code_value=[]
    for i in line:
        temp=i[:-1] # 줄바꿈 제거
        code_key.append(temp.split(" ")[1]+'.KS') # 공백기준 코드만 뽑기
        code_value.append(temp.split(" ")[0]) # 공백기준 기업명 뽑기
    code=dict(zip(code_key,code_value)) # zip은 인덱스 기준으로 리스트를 순서대로 가져오는 함수, dict는 딕셔너리 변환
    return code

def code_matching(df,code):
    code_key_list=list(code.keys())
    code_name_list=list(code.values())
    match_code=[]
    for i, data in enumerate(df['Code']):
        for j, obj in enumerate(code_key_list):
            if data==obj:
                match_code.append(code_name_list[j])
    df['기업명']=match_code

