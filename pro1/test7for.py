# 반복문 for
# for target in object:
#   statement...

# for i in [1,2,3,4,5]:
# for i in (1,2,3,4,5):
# for i in {1,2,3,4,5,5,5,5,5,5}:
aa = {1,2,3,4,5,5,5,5,5,5}
for i in aa:
    # pass
    print(i, end = ' ')

print('분산/표준편차 ---')
# numbers = [1,3,5,7,9]   # 합은 25, 평균은 5.0
# numbers = [3,4,5,6,7]   # 합은 25, 평균은 5.0
numbers = [-3,4,5,7,12]   # 합은 25, 평균은 5.0
tot = 0
for a in numbers:
    tot += a

print(f"합은 {tot}, 평균은 {tot / len(numbers)}")

avg = tot / len(numbers)

# 편차 제곱의 합
hap = 0
for i in numbers:
    hap += (i - avg) ** 2
print(f"편차 제곱의 합 : {hap}")

vari = hap / len(numbers)
print(f'분산은 {vari}')
print(f'표준편차는 {vari ** 0.5}')

print()
colors = ['빨강', '초록', '파랑']
for v in colors:
    print(v, end = ' ')

print()
print('iter() : 반복 가능한 객체를 하나씩 꺼낼 수 있는 상태로 만들어 주는 함수')
iterator = iter(colors)
for v in iterator:
    print(v, end = ' ')

print()
for idx, d in enumerate(colors, start=0):  # 인덱스와 값을 반환
    print(idx, ' ', d)

print('\n사전형 ---')
datas = {'python':'만능언어','java':'웹용언어','mariadb':'RDBMS'}
print(datas.items())  # [('python', '만능언어'), ... ]
for i in datas.items():
    print(i[0], ' ~~ ', i[1])   # python  ~~  만능언어 ...

for k, v in datas.items():
    print(k, ' ~~ ', v)

for k in datas.keys():
    print(k, end = ' ')   # python java mariadb 

print()
for v in datas.values():
    print(v, end = ' ')   # 만능언어 웹용언어 RDBMS

print('\n다중 for ------')
for n in [2, 3]:
    print(f'{n}단 ~~~ ')
    for su in [1,2,3,4,5,6,7,8,9]:
        print(f'{n} * {su} = {n * su}')

print('\nfor : continue, break ------')
nums = [1,2,3,4,5]
for i in nums:
    if i == 2: continue
    # if i == 4: break
    print(i, end=' ')
else:
    print('정상 종료')

print('\n\n정규표현식 + for 연습 ---')
message = """
도널드 트럼프 미국 대통령이 이재명 대통령과 최근 통화에서 이란전쟁에 대한 한국의 지원을 요청했지만 거절당했다고 공개했다. 전날 한국의 대이란 지원 거부를 한미연합훈련 축소 이유 중 하나로 제시한 데 이어 실제 정상 간 통화 내용까지 공개하며 불만을 드러낸 것이다.
17일(현지시간) 트럼프 대통령은 백악관에서 취재진과 만나 최근 이 대통령과 통화한 사실을 공개하며 "내가 좋아하는 한국 대통령에게 전화를 걸어 '우리를 좀 도와줄 수 있나. 이란 문제와 관련해 도움이 필요한 것은 아니지만 원한다면 손을 좀 보태달라'고 말했다"고 밝혔다.
도널드 트럼프 미국 대통령이 이재명 대통령과 최근 통화에서 
도널드 트럼프 도널드 트럼프 도널드 트럼프 abc & * $ # @
"""
import re
message2 = re.sub(r'[^가-힣\s]', '', message)  # 패턴과 일치하는 문자열을 다른 문자열로 치환
print(message2)
message3 = message2.split(' ')  # 공백 기준 문자열 분리
print(message3, ' ', len(message3))
# 단어별 빈도수 출력 : dict 사용
cou = {}
for i in message3:
    if i in cou:
        cou[i] += 1  # 같은 단어가 있으면 누적
    else:
        cou[i] = 1  # 최초 단어일 경우 '단어':1

print(cou)  # {'\n도널드': 2, '트럼프': 6,  ...

print('정규 표현식 좀 더 ...')
for imsi in ['111-1234','일이삼-일이삼사','222-1234','333&1234']:
    if re.match(r'^\d{3}-\d{4}$', imsi):
        print(imsi, '전화번호 맞네')
    else:
        print(imsi, '전화번호 아니야')

print('\ncomprehension : 반복문 + 조건문 + 값 생성을 한 줄로 표현')
a = [1,2,3,4,5,6,7,8,9,10]

li = []
for i in a:
    if i % 2 == 0:
        li.append(i)
print(li)   # [2, 4, 6, 8, 10]

print(list(i for i in a if i % 2 == 0))  # [2, 4, 6, 8, 10]

print()
datas = [1, 2, 'a', True, 3.0]
li2 = [i for i in datas if type(i) == int]
print(li2)

print()
id_name = {1:'tom', 2:'james'}
name_id = {val:key for key, val in id_name.items()}
print(name_id)  # {'tom': 1, 'james': 2}

print()
aa = [(1,2),(3,4),(5,6)]

for a, b in aa:
    print(a + b)

print(*[a + b for a, b in aa], sep='\n') 

print('\n수열 생성 : range(start, stop, step)')
print(list(range(1, 6)))  # [1, 2, 3, 4, 5]
print(list(range(1, 6, 1))) 
print(list(range(1, 6, 2)))
print(tuple(range(1, 6, 2)))
print(set(range(1, 6, 2)))
print(set(range(0, 6, 1)))  # {0, 1, 2, 3, 4, 5}
print(set(range(6)))  # {0, 1, 2, 3, 4, 5}
print(list(range(-10, -100, -20)))
print()
for i in range(6):
    print(i, end = ", ")

print()
for _ in range(6):
    print('반복')

print('1 ~ 10까지 정수 합')
tot = 0
for i in range(1, 11):
    tot += i

print('tot : ', tot, ' ', sum(range(1, 11))) # sum()내장함수

for i in range(1, 10):
    print(f'2 * {i} = {2 * i}')

print('2 ~ 9 구구단 출력 (단은 행단위 출력)')
for i in range(2, 10):
    for j in range(1, 10):
        print(f'{i}*{j} = {i * j}', end=' ')
    print()

print('주사위를 두 번 던져 나온 숫자들의 합이 4의 배수가 되는 경우만 출력')
for i in range(6):
    n1 = i + 1
    for j in range(6):
        n2 = j + 1
        n = n1 + n2
        if n % 4 == 0:
            print(n1, n2)
print()
for i in range(1, 7, 1):
    for j in range(1, 7):
        hap = i + j
        if hap % 4 == 0:
            print(i, j)





