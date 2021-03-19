from jamo import h2j, j2hcj # 자모 분리 라이브러리

'''
LevenshteinAlgorithm.py
형태소 분리 된 데이터에 대해 편집거리 알고리즘을 적용한다.
levenshtein을 두 개로 분리한 이유? = 파이썬의 for문 호출 제한 이슈 때문

def change_cost(a,b) : 교체비용에 해당하는 함수
def jamo_levenshtein(a, b) : 자모단위 levenshtein
def levenshtein(a, b): 글자단위 levenshtein

'''


def change_cost(a,b):
    if a==b: # 두 문자가 아예 같을 경우
        return 0
    return round(levenshtein(j2hcj(h2j(a)),j2hcj(h2j(b)))/3,2) # 다르다면 자모 단위까지 levenshtein을 적용한다.


def jamo_levenshtein(a, b):
    al=len(a)
    bl=len(b)
    if a==b: #문자열이 같을 때
        return 0
    if al<bl:
        return jamo_levenshtein(b,a)
    if b=='': #두 번째 문자열이 공백일 경우
        return al
    
    matrix=np.zeros((al+1,bl+1)) #모든값이 0인 행렬 반환
    
    for i in range(al+1): #초기화
        matrix[i][0]=i
    for j in range(bl+1):
        matrix[0][j]=j
    
    for i in range(1, al+1):
        aw=a[i-1]
        for j in range(1, bl+1):
            bw=b[j-1]
            matrix[i][j]=min({
                matrix[i-1][j]+1, #삭제
                matrix[i][j-1]+1, #삽입
                matrix[i-1][j-1]+(aw!=bw) #다를경우 1추가
            })
    return matrix[-1][-1] #행렬의 오른쪽 최하단값 반환


def levenshtein(a, b):
    al=len(a)
    bl=len(b)
    if a==b: #문자열이 같을 때
        return 0
    if al<bl:
        return levenshtein(b,a)
    if b=='': #두 번째 문자열이 공백일 경우
        return al
    
    matrix=np.zeros((al+1,bl+1)) #모든값이 0인 행렬 반환
    
    for i in range(al+1): #초기화
        matrix[i][0]=i
    for j in range(bl+1):
        matrix[0][j]=j
    
    for i in range(1, al+1):
        aw=a[i-1]
        for j in range(1, bl+1):
            bw=b[j-1]
            matrix[i][j]=min({
                matrix[i-1][j]+1, #삭제
                matrix[i][j-1]+1, #삽입
                matrix[i-1][j-1]+change_cost(aw,bw) #다를경우 1추가
            })
    return matrix[-1][-1] #행렬의 오른쪽 최하단값 반환

if __name__ == '__main__':
    data=pd.read_csv('C:\\Users\\SAMSUNG\\Downloads\\전체형태소_삼성전자.csv')
    data.rename(columns={'Unnamed: 0':'형태소', '0':'빈도수','Unnamed: 2':'감성점수','Unnamed: 3':'비고'},inplace=True)
    data

    data_low_frequency=data[(data.빈도수<20)&(data.빈도수>17)] # 숫자는 상황에 따라 임의 조정
    data_with_sent=data[data.빈도수>=20]

    word_dict={}
    result=[]

    for base in data_low_frequency['형태소']:
        for source in data_with_sent['형태소']:
            if levenshtein(base,source)<0.5:
                word_dict[source]=levenshtein(base,source)
        print(base)
        print(word_dict)
        
        if any(word_dict): # 만약 가까운 요소가 출력이 안된다면 base를 그대로 사용
            result.append(base)
            continue

        ans=input("출력된 단어 중 가장 가까운 단어를 골라 써주세요(없으면 x입력): ")
        if ans in word_dict:
            result.append(ans)
            print("단어가 대체되어 등록되었습니다.")
        else if ans=='x':
            print("선택하지 않으셨습니다.")
            result.append(base) # 출력된 단어 중 어느것과도 가깝지 않으면 base를 그대로 사용
        else:
            print("찾을 수 없는 단어입니다.")
            
        word_dict={} #초기화
        
    data_low_frequency['형태소']=result # 바뀐 값 복사