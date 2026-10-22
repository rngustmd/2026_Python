# p.217 딕셔너리
# 딕셔너리란? { }중괄호 선언하고 키:값 형태로 쉼표로 연결
# { key:value , key:value , key:value }
# key중복X / value중복O
# JS:JSON , JAVA:MAP/DTO , DB: RECORD

# 1. 선언 , { key : value , key : value }
dict_a = { 'name' : '어벤저스 엔드게임' , 
    'type' : '히어로 무비'}
# 2. 값호출 , 딕셔너리명['key']
print( dict_a['name'] ) # 어벤저스 엔드게임
print( dict_a['type'] ) # 히어로 무비
# 3. 속성값 추가 , 딕셔너리명['새로운 키'] = 새로운 값
dict_a[ 'price' ] = 5000
print( dict_a )
# 4. 속성값 수정
dict_a['type'] = '호러 무비' #이미 존재하는 키는 값 수정
print( dict_a )
# 5. 속성 삭제 , del 딕셔너리[ 'key' ]
del dict_a[ 'price' ]
print( dict_a )
# 6. 딕셔너리 내부 'key' 확인 , 찾을키 in 딕셔너리명
print( 'price' in dict_a )  # False
print( 'name' in dict_a )   # True
# 7. 속성값 호출 , 방법1: 딕셔너리명['key'] , 방법2: 딕셔너리명.get( key )
# 차이점 : 방법1은 존재하지 않으면 예외발생, 방법2는 존재하지 않으면 None 반환
print( dict_a.get( 'name') ) # 어벤저스 엔드게임
print( dict_a.get( 'price') ) # None
# 8. for 반복문 과 딕셔너리 , 딕셔너리내 key 하나씩 for에서 순회
# for key반복변수 in 딕셔너리명:
#      실행코드
for key in dict_a : 
    print( dict_a.get(key) ) #방법1
    print( dict_a[key] )     #방법2