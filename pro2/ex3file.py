# with 구문 형식
# with 표현식 as 변수:
#     실행문

# 파일 입출력에서는 보통 이렇게 사용
# with open("파일명", "모드", encoding="utf-8") as 파일객체:
#     파일 처리 코드 ...
# 블록 종료시 파일 자동 close됨

try:
    # 파일 저장
    with open('ftest3.txt', mode='w', encoding='utf-8') as fobj1:
        fobj1.write('파이썬에서 문서 저장\n')
        fobj1.write('with 구문은\n')
        fobj1.write('파일 작업 종료시 자동 close됨')

    print('저장 완료')

    print()
    # 파일 읽기
    with open('ftest3.txt', mode='r', encoding='utf-8') as fobj2:
        print(fobj2.read())

except Exception as e:
    print('err : ', e)


print('\n\n피클링(Pickling) : 일반 객체 및 복합 객체 파일 입출력')
import pickle

try:
    dictData = {'tom':'111-1111', '길동':'222-2222'}
    listData = ['마우스', '모니터']
    tupleData = (dictData, listData)

    with open('hello.dat', mode='wb') as fobj3:
        pickle.dump(tupleData, fobj3)   # 저장 - pickle.dump(대상, 파일객체)
        pickle.dump(listData, fobj3)

    print('특정 객체를 파일로 저장')

    print('\n피클 객체 읽기')
    with open('hello.dat', mode='rb') as fobj4:
        a, b = pickle.load(fobj4)  # pickle.load(파일객체)
        print('a : ', a)  # {'tom': '111-1111', '길동': '222-2222'}
        print('b : ', b)  # ['마우스', '모니터']

        c = pickle.load(fobj4)
        print('c : ', c)  # ['마우스', '모니터']

except Exception as e2:
    print('피클링 연습 중 오류 : , e2')




