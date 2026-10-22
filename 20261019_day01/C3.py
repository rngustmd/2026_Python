# 비교연산자 # == , != , > , < , >= , <=
#p.158 범위논리
x = 25
print( 10 < x < 30 )
# 논리연산자 # not , and , or
print( not True )           # False
print( True and True )      # True
print( True and False )     # False 
print( True or False )      # True
#p.163 , if조건문
# if 조건식 :
#    (tab들여쓰기)참이면
age = 10
if age >= 19 :
    print( '성인입니다.' )
# if ~ else 
# if 조건식 : 
#   (tab들여쓰기)참이면
# else :
#   (tab들여쓰기)거짓이면
number = 13
if number % 2 == 0 :
    print( '짝수입니다.')
else : 
    print( '홀수입니다.')
# if ~ elif ~ elif ~ else :
point = 85
if point >= 90 :
    print( 'A' )
elif point >= 80 :
    print( 'B' )
elif point >= 70 :
    print( 'C' )
else :
    print( '재시험')
# 주의할점 : if ~ if ~ if ~ else  [vs] if ~ elif ~ elif ~ else
# 다수조건에 다수결과 vs 다수조건에 1개결과
# 자바와 다르게 (조건식){ } 없이 :콜론 과 들여쓰기 구분

# if중첩 
x = 10