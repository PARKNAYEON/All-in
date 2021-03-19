import glob
import csv

'''
MergeFile.py
여러개로 나누어진 종목토론방 데이터를 하나로 묶음

'''

def merge_file(input_path, merge_output):
    file_list=glob.glob(os.path.join(input_path,'*'))
    with open(merge_output,'w',encoding='utf-8-sig') as f:
        for i, file in enumerate(file_list):
            if i==0: # 처음 파일에만 헤더 포함!
                with open(file,'r',encoding='utf-8-sig') as f2:
                    while True:
                        line=f2.readline()
                        
                        if not line:
                            break
                        f.write(line)
                file_name=file.split('\\')[-1]
                print(file_name+ ' complete')
            else:
                with open(file,'r',encoding='utf-8-sig') as f2:
                    n=0
                    while True:
                        line=f2.readline()
                        if not line:
                            break
                        if n!=0:
                            f.write(line)
                        n+=1
                file_name=file.split('\\')[-1]
                print(file_name+ ' complete')
    print("모든 파일 완료")


if __name__ == '__main__':
    input_path=input("경로를 입력해주세요. :") # 기업별 하위 디렉토리 경로 ./기업코드_data 형식
    input_path.replace("\\","\/") # 복사 붙여넣기 해도 \를 /로 바꿔준다.
    input_path=input_path+'\/' # 맨 마지막에도 채워 넣어 준다.
    output_name=input("최종 파일 이름을 입력해주세요. :")
    output_path=input("최종 파일 경로를 입력해주세요. :")
    output_path.replace("\\","\/")
    merge_output=output_path+'\\'+output_name+'.csv'
    merge_file(input_path,merge_output)