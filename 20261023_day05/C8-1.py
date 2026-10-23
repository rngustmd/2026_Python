# 절차지향 프로그래밍 : 데이터를 순서대로 처리하고 하향식 순차 실행 흐름
# 객체지향 프로그래밍 : 객체들의 상호작용으로 프로그래밍 설계 , JAVA/PYTHON/JS
# 관점지향 프로그래밍 : 공통되는 기능(로그/검증/보안 등) 들을 분리하여 프로그래밍 설계
# 추상화 : 핵심적인 개념 또는 기능 간추려 내는 것
# [ 리스트 ] , { 딕셔너리 } 객체이다.
# 클래스 : 추상화한 데이터들을 구조화 한 것 ( 설계도 )      
# 객체 : 세상에 존재하는 모든 데이터들을 추상화 ( 실체 X )   -> 개념적 객체
# 인스턴스 : 추상화한 것을 객체로 만든 것( 실체O )          -> 물리적 객체
# 인스턴스화 : 컴퓨터 내 객체 정보 저장 , JAVA : NEW 생성자() , PY : 생성자()
# 생성자 : 클래스 기반으로 인스턴스 만드는 함수             -> 인스턴스 초기화함수

# 1. 클래스 만들기
# class 클래스명 : 
class Student : # JAVA : new Student() , PY : Student()
    pass
student = Student()
students = [
    Student(),
    Student(),
    Student(),
    Student(),
    Student(),
    Student()
]

# 2. 생성자
class Student : 
    # def __init__(self , 멤버변수1):
    #   self.멤버변수1 = 멤버변수1;
    def __init__(self , name , korean , math , english , science ):
        self.name = name
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science
    # def 메솓,명( self , 메개변수1 ) :
    def get_sum( self ) :
        return self.korean + self.math + self.english + self.science
    def get_average( self ) :
        return self.get_sum() / 4
    def to_string( self ) :
        return " {} \t {} \t {}".format( self.name , self.get_sum() , self.get_average() )

# 일반함수와 메소드 차이? 일반함수는 클래스 밖에서 독립선언 / 메소드는 클래스 안에서 선언
def get_sum2( ) : 
    pass

# 생성자 이용한 인스턴스 생성
# Student2 s = new Student( "유재석" , 10 , 20 , 30 ,40 )
students = [
    Student2("윤인성" , 87 , 98 , 88 , 85 ),
    Student2("윤인성" , 87 , 98 , 88 , 85 ),
    Student2("윤인성" , 87 , 98 , 88 , 85 ),
    Student2("윤인성" , 87 , 98 , 88 , 85 ),
    Student2("윤인성" , 87 , 98 , 88 , 85 ),
    Student2("윤인성" , 87 , 98 , 88 , 85 ),
]
# 인스턴스 내 멤버변수 호출 
print( students[0].korean ) # 87
