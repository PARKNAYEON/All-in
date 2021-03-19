import rhinoMorph # 형태소 분석기
import re
rn = rhinoMorph.startRhino()

'''
WordAnalysis.py
모인 데이터를 바탕으로 형태소를 분석함

def Morph(df) : 형태소 Morph 사용해서 분석하는 함수
def comment(df) : 제목에서 댓글 수 뽑아내는 함수. 댓글은 [n]의 형태

'''

def Morph(df):
    print(df.isna().sum()) # 결측치 확인
    comment(df)
    
    morphed_data=''

    for i in df['adj_title']:
        morphed_data_object=rhinoMorph.onlyMorph_list(rn,i,pos=['NNG', 'VCP', 'VCN', 'MAG', 'VA', 'VV', 'XR','MM','NV','NF'],eomi=True)
        joined_data_object=' '.join(morphed_data_object)
    
    if joined_data_object:
        morphed_data+=joined_data_object+'\n'
        
    merge_text_list=re.split('\n| ',morphed_data)
    word=pd.Series(merge_text_list)
    result=word.value_counts()
    
    result.to_csv('result.csv',mode='w',encoding='utf-8-sig',header=True,index=True)


def comment(df):
    df['comment']=0
    df['adj_title']=''
    
    k=0
    for j in df['title']:
        if j:
            if j[-1]==']': 
                df['comment'][k]=float(j[-2])
                df['adj_title'][k]=j[:-3]
            else:
                df['adj_title'][k]=j
        k+=1
        
    df['date']=pd.to_datetime(df['date'],format='%Y.%m.%d %H:%M') # 문자열로 받은 날짜 데이터 포맷 변경
    df.drop(labels=['Unnamed: 0','title'],axis=1,inplace=True) # 원래 타이틀은 댓글 수를 포함하고 있으므로 분리 이후에 삭제
    
    return df

if __name__ == '__main__':
    data=pd.read_csv('./merge_output.csv', encoding='utf-8-sig') # 파일 이름은 merge_file 함수를 거치고 난 결과물을 대입
    Morph(data)