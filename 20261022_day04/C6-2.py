# 예외객체 란? 발생한 예외 정보 갖는 객체 
# 예외클래스 : Exception(예외 최상위클래스)
# except 예외클래명 as 변수명 : 
# as 키워드 : 클래스의 객체변수 생성 
# 그외 모든 예외 처리 : 여러개 except 에서 Exception은 항상 마지막에 위치 
#  주의할점 : Exception 앞에 위치하면 아래 except 예외가 작동 안함.-> 상속개념 
# raise : 강제로 예외발생 , 주로 CRUD 실패500 의미

# p.383
list_number = [ 52 , 273 , 32 , 72 , 100 ]
try :
    number_input = int( input('정수입력: ') ) # 타입 예외
    print( list_number[ number_input ] )     # 인덱스 예외
except ValueError as e :    # 타입변환 예외
    print( e )
except IndexError as e :    # 인덱스 예외
    print( e )
except Exception as e :     # 그 외 (최상위) 예외 항상 마지막
    print( e )

#
a = 10              # 전역스택
def 함수( ) :   
    # 단순 호출이면 global 생략 가능, 
    # 전역변수 수정하면 global 필수
    global a        # global 전역변수명
    a = a + 1
    print( a )      # global 없어도 전역스택 가능
    b = 20          # 함수스택
함수( )