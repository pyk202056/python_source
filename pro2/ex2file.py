print('파일 처리 : 입출력')
import os   # 운영체제(OS)와 관련된 기능 제공

try:
    print('파일 읽기 -----')
    print(os.getcwd())  # C:\works\projects\pro2

    # 읽을 파일 C:\works\projects\pro2\ftest.txt
    # f1 = open(file=os.getcwd() + r'\ftest.txt', mode='r', encoding='utf-8')
    # f1 = open(r'C:\works\projects\pro2\ftest.txt', mode='r', encoding='utf-8')
    f1 = open(r'ftest.txt', mode='r', encoding='utf-8')  # mode='r', 'w', 'a', 'b',...
    print(f1)
    print(f1.read())
    f1.close()   # 작업이 끝나면 닫기 권장

    print('\n파일 저장 -----')
    f2 = open('ftest2.txt', mode='w', encoding='utf-8')
    f2.write('내 친구들\n')
    f2.write('신기해, 이기자\n')
    f2.close()
    print('파일 저장 성공')

    print('파일 내용 추가 -----')
    f3 = open('ftest2.txt', mode='a', encoding='utf-8')
    f3.write('\n사오정')
    f3.write('\n손오공')
    f3.write('\n저팔계')
    f3.close()
    print('파일 추가 성공')

    # ftest2.txt 읽기
    print('~~~~~~~~~~')
    f4 = open(file='ftest2.txt', mode='r', encoding='utf-8')
    print(f4.read())
    f4.close()
except Exception as e:
    print("처리 오류 : ", e)
