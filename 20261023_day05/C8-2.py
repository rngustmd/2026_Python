# 상속이란? 어떤 클래스를 기반으로 그 속성과 기능을 물려받아 새로운 클래스 만드는것
# isinstance( 인스턴스 , 클래스명 )
#예1
class Student : 
    def __init__(self):
        pass
class Human : 
    def __init__(self):
        pass
student = Student()
print( isinstance( student , Student) ) # true
print( isinstance( student , Human ) ) # false

#예2] c8-1.py 클래스 코드 가져와서 이어서 작성
class Student2 : 
    # p.484 클래스변수 ? 인스턴스없이 사용 가능한 변수
    # 클래스변수명 = 초기값 
    count = 0 
    students = [ ]
    # p.486 클래스함수
    @classmethod # 클래스함수 정의하는 데코레이터/어노테이션
    def print( cls ) : # 매개변수에 cls관례적으로 선언 
        for student in cls.students : 
            # cls.클래스변수 <--동일--> 클래스명.클래스변수
            print( str( student ) ) #

    def __init__(self , name , korean, math , engligh, science ):
        # 멤버/인스턴스 변수
        self.name = name
        self.korean = korean
        self.math = math
        self.engligh = engligh
        self.science = science
        Student2.count += 1 # 클래스변수 호출방법: 클래스명.변수명
        Student2.students.append( self )
        
    def get_sum( self ) :
        return self.korean + self.math + self.engligh + self.science
    def get_average( self ) :
        return self.get_sum() / 4 
    def to_string( self ) : 
        return "{} \t {} \t {}".format( self.name , self.get_sum() , self.get_average())
    # 특수한 이름의 메소드 # 보조기능 재정의(오버라이딩)
    def __str__(self):
        return "{} \t {} \t {}".format( self.name , self.get_sum() , self.get_average())
    # 특수한 이름의 메소드 / 비교 메소드 #  총합계 비교 함수 재정의 
    def __eq__(self, value): 
        return self.get_sum() == value.get_sum()
    def __ne__(self, value):
        return self.get_sum() != value.get_sum()
    def __gt__(self, value):
        return self.get_sum() > value.get_sum()
    def __ge__(self, value):
        return self.get_sum() >= value.get_sum()
    def __lt__(self, value):
        return self.get_sum() < value.get_sum()
    def __le__(self, value):
        return self.get_sum() <= value.get_sum()
students = [
    Student2("윤인성" , 87 , 98 , 88 , 85),Student2("윤인성" , 87 , 98 , 88 , 85),
    Student2("윤인성" , 87 , 98 , 88 , 85),Student2("윤인성" , 87 , 98 , 88 , 85),
    Student2("윤인성" , 87 , 98 , 88 , 85),Student2("윤인성" , 87 , 98 , 88 , 85),            
]
# 특수한 이름의 메소드 호출 , str( 인스턴스 )
print( str( students[0] ) )             #  __str__ 함수가 실행된다.
print( students[0] == students[1] )     # 주소값 다른데. # == 대신에 __eq__ 함수가 실행된다
# 원래 객체는 다른데. 우리가 __eq__ 메소드에서 같다 기준을 총합계 정의 했으므로   #true
print( students[0] != students[1] )     # 
# 원래 객체는 다른데. 우리가 __ne__ 메소드에서 다르다 기준을 총합계 정의 했으므로 #false 

# 클래스명.클래스변수 : 클래스변수 값 호출 
print( Student2.count ) # 6 # __init__ 6번 실행

# 클래스명.클래스함수
Student2.print() 

# p.491 프라이빗 변수 
class Circle : 
    def __init__(self ,  radius ):
        self.__radius = radius # java: private int radius 
    def get_circumference( self ):
        return 2* self.__radius  # 클래스 내부에서 프라이빗 변수 사용 가능 
    # setter and getter 
    def get_radius( self ) :
        return self.__radius # 프라이빗 변수 반환 하는 getter함수 
    def set_radius( self , radius  ) :
        self.__radius = radius # 매개변수값을 프라이빗 변수에 저장하는 setter함수

circle = Circle( 10 )
# print( circle.__radius) # 클래스 외부에서 프라이빗 변수 사용 안됨 
print( circle.get_radius() ) # 10
circle.set_radius( 20 )
print( circle.get_radius() ) # 20

# p.497 상속의 활용
class Parent : 
    def __init__(self):
        self.value = "테스트"
        print( "init 메소드 호출" )     # (1)
    def test( self ) :
        print( "test()메소드 호출" )    # (2)

# class 자식클래스명( 부모클래스명1 , 부모클래스명2 ) : 파이썬은 부모클래스가 여러개 가능!

class Child( Parent ) : # java : class 자식클래스명( 부모클래스명 )
    def __init__(self):
        super().__init__()
        print('child init 메소드 호출')  # (3)
    def test( self ) : # 오버라이딩 / 재정의
        print( 'child test 메소드 호출') # (4)
child = Child()
# print() 출력되는 횟수 # 자식이 태어나면 부모도 같이 태어난다 (1) (3)
child.test()    # 부모 test() 가 아닌 자식 test() 가 실행된다. (4)
parent = Parent()
parent.test()   # (2) test() 메소드 호출
parent2 = child
parent2.test()  # (4) child test 메소드 호출

