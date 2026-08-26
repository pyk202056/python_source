# 예외처리 : 파일, 네크워크, DB작업, 실행오류 등의 에러에 대처
# try ~ except는 프로그램 실행 중 발생할 수 있는 오류(Exception)를 
# 처리해서 프로그램이 갑자기 종료되지 않도록 하는 문법.

# try에는 오류가 발생할 가능성이 있는 코드를 작성하고, 
# except에는 해당 오류가 발생했을 때 어떻게 처리할지를 작성한다.

# try:
#   실행할 코드
#   ...
# except 예외종류:
#   오류 처리 코드
# finally:
#   오류유무와 상관없이 처리할 구문 (반드시 실행할 코드)

def divideFunc(a, b):
    return a / b

print('이런 저런 작업을 하다가 ...')
# c = divideFunc(5, 2)
# c = divideFunc(5, 0)
# print(c)

try:
    # 실행문 처리 블럭 (오류 가능 영역)
    c = divideFunc(5, 2)
    # c = divideFunc(5, 0)
    print(c)
    print('계속')
    aa = [1, 2]
    print(aa[0])
    # print(aa[3])

    # 파일 읽기
    open('c:/work/ok.txt')

except ZeroDivisionError:
    # 에러 발생시 처리 영역
    print('두번째 값은 0을 주면 안돼요')
except IndexError as err:
    print('참조 범위 오류 : ', err)
except Exception as e:  # 발생한 일반적인 예외를 한 번에 받아서 처리할 때 사용
    # 여러 예외를 포괄적으로 처리
    print('에러 : ', e)
finally:
    print('에러 유무에 상관없이 반드시 수행됨')

print('프로그램 종료')


