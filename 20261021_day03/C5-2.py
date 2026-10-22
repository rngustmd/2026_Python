# p.293 재귀함수 , 재귀란 자기 자신을 호출하는것 
# 1] 팩토리얼 반복문
def factorial1(n) : 
    output = 1
    for i in range( 1 , n+1 ):
        output *= i 
    return output
factorial1( 2 )   # 2! ->  1 ~ 2 -> 1 * 2 
factorial1( 3 )   # 3! ->  1 ~ 3 -> 1 * 2 * 3 
# 만약에 n 이 3이면 range( 1 , 4 ) 반복하므로
# i는 1일때 output = output * 1
# i는 2일때 output = output * 2
# i는 3일때 output = output * 3
# 1 * 2 * 3 => 3!





# 2] 팩토리얼 재귀 
def factorial2( n ) : 
    # 무한 재귀 방지
    if n == 0 : 
        return 1 
    else : # 재귀함수  
        return n * factorial2( n-1 )
factorial2( 2 )
factorial2( 3 )
# 만약에 n 이 3이면 n == 0 false 
    # return n * factorial2( 2 )                                   return 3 * 2 * 1 * 1
        # n 이 2이면 n == 0 false   
            # return n * factorial2( 1 )                        return 2 * 1 * 1
                 # n 이 1이면 n == 0 false
                    # return n * factorial2( 0 )            return 1 * 1
                        # n 이 0 이면 n == 0 true       return 1
# 함수 호출 1개당 리턴1번 => 함수 3번 호출 / 리턴 3번 

# 구구단 반복문
for 단 in range( 2 , 10 , 1 ) : # 단 : 2 부터 9 까지 1씩증가
    for 곱 in range( 1 , 10 , 1 ) : # 곱 : 1부터 9까지 1씩증가
        print( 단*곱 )
# 2단~3단 까지 / 1~4곱 까지 의 반복문 순서도 작성 













# 구구단 재귀
def 구구단( 단=2 , 곱= 1 ) : 
    if 단 > 9 : # 재귀 끝
        return
    if 곱 > 9 : # 단마다 곱하기 9까지 했으면 단 올리기 
        구구단( 단+1 , 1 )
        return
    print( 단 * 곱 )
    구구단( 단 , 곱 + 1 ) # 곱 올리기 
구구단( )
# 2단~3단 까지 / 1~4곱 까지 의 반복문 순서도 작성

# 297p. 피보나치수열1  -------------------
counter = 0 
def fibonacci( n ) : 
    print( "fibonacci({})를 구합니다".format(n) )
    global counter
    counter += 1 
    if n == 1 :
        return 1 
    if n == 2 : 
        return 1 
    else : 
        return fibonacci( n-1 ) + fibonacci( n - 2 )
print( fibonacci( 5 ) ) 

# 301p. 피보나치수열2 메모화 -------------
dictionary = { 1 : 1 , 2 : 1 }
def fibonacci2( n ) : 
    if n in dictionary :
        return dictionary[n]
    else : 
        output = fibonacci2( n - 1 ) + fibonacci2( n - 2 )
        dictionary[n] = output
        return output
print( fibonacci2( 5 ) ) 


    