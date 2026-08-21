# 기본 자료형 : int, float, bool, complex
# 묶음 자료형 : str, list, tuple, set, dict

# str : 문자열 저장 단위, 순서O, 수정X
s = "sequence"
print("길이(크기):", len(s))
print("포함 횟수 : ", s.count('e'))
print('검색 위치 : ', s.find('e'), s.find('e', 3), s.rfind('e'))
print('첫글자 유무 : ', s.startswith('s'), s.startswith('a'))

print()
ss = "mbc"
print(ss, id(ss))
ss = "abc"
print(ss, id(ss))

print('인덱싱 / 슬라이싱')
print(s[0], s[5], s[-1])  # s n e   <== 인덱싱
print(s[0:4], s[:4], s[-4:-1])  # sequ sequ enc  <== 슬라이싱
print(s[::2], s[0:8:3], s[0:len(s):1])

print("*" * 10)
# List : 다양한 종류의 자료 묶음형.  순서O, 수정O, 중복O
a = [1, 2, 3]  # [다양한 종류의 데이터, ...]
print(a, a[0], a[0:2])
b = [10, a, 10, 20.5, True, '문자열']
print(b, b[0], b[1], b[1][1])
print()
family = ['엄마', '아빠', '나', '여동생']
print(family, id(family))
family.append('남동생')   # 추가
print(family, id(family))
family.remove('나')   # 삭제
print(family)
family.insert(0, '할머니')  # 삽입
print(family)
family.extend(['삼촌','고모','조카'])  # 추가
print(family)
family += ['이모']   # 추가(누적)
print(family)

family.remove('아빠')   # 값에 의한 삭제
del family[2]   # 순서에 의한 삭제
print(family)

print()
kbs = ['123', '34', '234']
kbs.sort()    # 문자열 정렬
print(kbs)    # ['123', '234', '34']

mbc = [123, 34, 234]
print(mbc)
mbc.sort()   # 오름차순(ascending)  - 리스트 값 순서가 바뀜
print(mbc)   # [34, 123, 234]
mbc.sort(reverse=True)   # 내림차순(descending) 
print(mbc)   # [234, 123, 34]
print()
sbs = [123, 34, 234]
ytn = sorted(sbs)
print(ytn)
print(sbs)

print("*" * 10)
# tuple : 리스트와 유사. 읽기 전용 - 수정 X
t = (1, 2, 3, 4)  # (다양한 종류의 데이터, ...)
t = 1, 2, 3, 4    # 위와 동일
print(t, type(t)) # (1, 2, 3, 4) <class 'tuple'>

k = (1,)  # 주의
print(k, type(k))

print(t[0], t[1:3])
# t[0] = 9  # 'tuple' object does not support item assignment

# 튜플 값 수정시 리스트로 형변환 사용
imsi = list(t)  # type변환
print(type(imsi))  # <class 'list'>
imsi[0] = 9
t = tuple(imsi)
print(t, type(t))

print("--" * 10)
# set : 순서X, 중복X, 수정O
ss = {1, 2, 3, 2}
print(ss, type(ss))  # {1, 2, 3} <class 'set'>
ss2 = {3, 4}
print(ss.union(ss2))  # 합집합   {1, 2, 3, 4}
print(ss.intersection(ss2))  # 교집합  {3}
print(ss - ss2, ss | ss2, ss & ss2)  # 차, 합, 교집합  {1, 2} {1, 2, 3, 4} {3}

ss.update({6, 7})
print(ss)
ss.discard(7)  # 값 삭제
ss.discard(7)  # 값 삭제 : 해당 값 없으면 통과
ss.remove(6)   # 값 삭제
# ss.remove(6)   # 값 삭제 : 해당 값 없으면 err
print(ss)

print()
li = ['aa', 'aa', 'bb', 'cc', 'aa']
print(li)
imsi = set(li)
li = list(imsi)
print(li)  # ['aa', 'cc', 'bb']

print("--" * 10)
# dict : 사전 자료형  {'키':값} 형태
# 방법1
mydic = dict(k1=1, k2='ok', k3=1234)
print(mydic, type(mydic))  # {'k1': 1, 'k2': 'ok', 'k3': 1234} <class 'dict'>

# 방법2
dic = {'파이썬':'뱀', '자바':'커피', '번호':123}
print(dic, type(dic))
print(len(dic))
print(dic['자바'])  # 키로 값을 검색
print(dic.get('자바'))
# print(dic[0])  # 인덱싱 불가 (순서가 없기 때문)

dic['금요일'] = 'wow'   # 추가
print(dic)

del dic['번호']  # 삭제
print(dic)

print(dic.keys())
print(dic.values())
