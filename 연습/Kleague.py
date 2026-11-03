import requests
from bs4 import BeautifulSoup
import pandas as pd

player_list = []

url = "https://www.kleague.com/record/player.do"
response = requests.get( url )
print( response )

soup = BeautifulSoup( response.text , "html.parser" )
rows = soup.select( "#player_rank tr" )

for row in rows :
    cells = row.select( "td" )
    player_list.append( {
        "순위" : cells[0].get_text().strip() ,
        "선수명" : cells[1].get_text().strip() ,
        "팀" : cells[2].get_text().strip() ,
        "득점" : cells[3].get_text().strip() ,
        "도움" : cells[4].get_text().strip() ,
        "파울" : cells[8].get_text().strip() ,
        "슈팅" : cells[9].get_text().strip() ,
        "경고" : cells[11].get_text().strip() ,
        "퇴장" : cells[12].get_text().strip() ,
        "출장" : cells[14].get_text().strip()
    } )

print( "총" , len( player_list ) , "명" )

# ================= 여기부터 추가 =================

# 1) 리스트 → 데이터프레임
df = pd.DataFrame( player_list )

# 2) 숫자 컬럼 문자열 → 숫자 변환
for col in [ "순위" , "득점" , "도움" , "파울" , "슈팅" , "경고" , "퇴장" , "출장" ] :
    df[ col ] = pd.to_numeric( df[ col ] )

# 3) 정렬
pd.set_option('display.unicode.east_asian_width', True)
print( df.sort_values( by = "득점" , ascending = False ).head( 10 ) ) # 슈팅 많은 순 TOP 10

# 4) 골 결정력 컬럼 만들기 : 득점 ÷ 슈팅 × 100 ( 슈팅 100번 중 몇 골인지, % )
df[ "골결정력" ] = ( df[ "득점" ] / df[ "슈팅" ] * 100 ).round( 1 )

# 5) 골 결정력 높은 순으로 정렬해서 필요한 컬럼만 표로 보기
result1 = df.sort_values( by = "골결정력" , ascending = False )
print( result1[ [ "선수명" , "팀" , "득점" , "슈팅" , "골결정력" ] ].head( 10 ) )

# 6) 경기당 득점 컬럼 : 득점 ÷ 출장
df[ "경기당득점" ] = ( df[ "득점" ] / df[ "출장" ] ).round( 2 )

result2 = df.sort_values( by = "경기당득점" , ascending = False )
print( result2[ [ "선수명" , "팀" , "득점" , "출장" , "경기당득점" ] ].head( 10 ) )

# 7) 공격포인트 컬럼 : 득점 + 도움
df[ "공격포인트" ] = df[ "득점" ] + df[ "도움" ]

# 공격포인트 높은 순 → 같으면 득점 높은 순
result3 = df.sort_values( by = [ "공격포인트" , "득점" ] , ascending = [ False , False ] )
print( result3[ [ "선수명" , "팀" , "득점" , "도움" , "공격포인트" ] ].head( 10 ) )

# 8) 경고 대비 퇴장 비율 : 퇴장 ÷ 경고 ( 경고 1개 이상만 )
card = df[ df[ "경고" ] >= 1 ].copy()
card[ "퇴장비율" ] = ( card[ "퇴장" ] / card[ "경고" ] ).round( 2 )

result4 = card.sort_values( by = [ "퇴장비율" , "경고" ] , ascending = [ True , False ] )
print( result4[ [ "선수명" , "팀" , "경고" , "퇴장" , "퇴장비율" ] ].head( 10 ) )

# 9) 경기당 파울 : 파울 ÷ 출장
df[ "경기당파울" ] = ( df[ "파울" ] / df[ "출장" ] ).round( 2 )

result5 = df.sort_values( by = "경기당파울" , ascending = False )
print( result5[ [ "선수명" , "팀" , "파울" , "출장" , "경기당파울" ] ].head( 10 ) )