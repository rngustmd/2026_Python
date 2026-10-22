
# 구문 오류 : 실행 전 오류 , 실행 자체 불가능
# 런타임 오류 : 실행 중 오류 , 예외
# 예외 처리 : 예외를 해결하는 모든 것

# 조건문 또는 try
# 예 1] 조건문 예외
input_a = input( "정수입력: ")
# int( input_a ) # ValueError: # int( ) 정수로 변환 함수 
if input_a.isdigit() :  # 문자열.isdigit() : 문자열타입의 값이 숫자이면 true 
    int( input_a )
    
else : 
    print("정수가 아닙니다.")
# 예2] try 예외
try :
    int( input_a ) # 예외가 발생할 것 같은 코드 
except : 
    print("정수가 아닙니다.")

# 예3] pass 키워드 , 예외 어떻게 처리할지 모른경우 일단 넘어가기 
try : 
    int( input_a )
except :
    pass

# 예4] else , 예외가 발생하지 않았을 떄
try :   # 예외가 발생할 가능성이 있는 코드 
    int( input_a )
except :# 예외가 발생했을 떄 실행코드 
    print( "정수가 아닙니다.")
else : # 예외가 발생하지 않았을 떄 실행코드
    print( "정수가 맞습니다.")

# 에5] finally , 예외가 발생하든 발생하지 않든 무조건 실행 코드 
try : 
    int( input_a )
except :
    print( "정수가 아닙니다.")
else : 
    print( "정수가 맞습니다.")
finally : # 무조건 실행되는 코드
    print( "코드가 끝났습니다.")

# 예6] finally 활용
try : # open( 파일명 , 옵션 ) 파일 불러오기 함수 # w옵션 : 파일이 없으면 생성
    file = open("info.txt" , "w")
    예외.발생해라() # 일부러 예외 발생!!*****
    # try 에서 만약에 예외가 발생하면 발생한 코드 이후는 실행 안됨. -> except 이동
    # file.close() # 파일.close() : 파일닫기
except : 
    print( "예외가 발생 했습니다." )
finally : 
    file.close() # 파일.close() : 파일닫기
print( file.closed)
# finally 사용 : return 함수 종료 , break 반복문 종료 + finally 조합


numbers = [ 52 , 273 , 32 , 103 , 90 , 10 , 275 ]

print("#(1) 요소 내부에 있는 값 찾기")
print("-{} 는 {}위치에 있습니다.".format(52 , numbers.index(52)))
print()

print("#요소내부에없는값찾기")
number = 10000
try : 
    print("-{} 는 {}위치에 있습니다.".format(52 , numbers.index(52)))
except ValueError :
    print("- 리스트 내부에 없는 값입니다.")
print()

print("종료")

output = 1- + "개"
int( "안녕하세요")
(cursor.close)
[1 , 2 , 3 , 4 , 5][10]