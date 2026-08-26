# 우편정보 파일 자료 읽기
# 키보드에서 입력한 동이름으로 해당 주소 정보 출력

def zipProcess():
    dongIrum = input('동 이름 입력:')
    # dongIrum = '서초1동'
    # print(dongIrum)

    with open(r'zipcode.txt', mode='r', encoding='utf-8') as f:
        # line = f.read()   # 전체 행 읽기
        line = f.readline() # 한 행 읽기

        # print(line)  # 135-806 서울    강남구  개포1동 경남아파트 1
        # 주소 문자열 자르기
        # lines = line.split('\t')  # tab 키로 구분
        # lines = line.split(chr(9))  # chr(tab에 해당하는 ascii 코드값(10진수))
        # print(lines)  # ['135-806', '서울', '강남구', '개포1동 경남아파트', '', '1\n']

        while line:
            lines = line.split(chr(9))
            if lines[3].startswith(dongIrum):
                # print(lines)
                print(f'우:{lines[0]} {lines[1]} {lines[2]} {lines[3]}')

            line = f.readline()
            

if __name__ == '__main__':
    zipProcess()