# K리그 득점 상위 30명 기록 분석
# 출처 : https://www.kleague.com/record/player.do ( 정적 페이지 , requests + BeautifulSoup )

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# ============================================================
# 0. 출력 설정
# ============================================================
pd.set_option( 'display.unicode.east_asian_width' , True )   # 한글 줄맞춤
pd.set_option( 'display.max_columns' , None )                 # 컬럼 생략 없이
pd.set_option( 'display.width' , 200 )                        # 한 줄 출력 폭

# ============================================================
# 1. 크롤링
# ============================================================
player_list = []

url = "https://www.kleague.com/record/player.do"
response = requests.get( url )
print( response )

soup = BeautifulSoup( response.text , "html.parser" )
rows = soup.select( "#player_rank tr" )

for row in rows :
    cells = row.select( "td" )
    if len( cells ) < 17 :          # 칸이 모자란 줄( 빈 줄 등 )은 건너뛰기
        continue
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

print( "총" , len( player_list ) , "명 수집" )

# ============================================================
# 2. 데이터프레임 변환 + 숫자 변환
# ============================================================
df = pd.DataFrame( player_list )

for col in [ "순위" , "득점" , "도움" , "파울" , "슈팅" , "경고" , "퇴장" , "출장" ] :
    df[ col ] = pd.to_numeric( df[ col ] )

# ============================================================
# 3. 파생 변수 ( 계산 컬럼은 여기서 한 번에 )
# ============================================================
df[ "공격포인트" ] = df[ "득점" ] + df[ "도움" ]
df[ "골결정력" ] = ( df[ "득점" ] / df[ "슈팅" ] * 100 ).round( 1 )   # 슈팅 100번 중 골( % )
df[ "경기당득점" ] = ( df[ "득점" ] / df[ "출장" ] ).round( 2 )
df[ "경기당파울" ] = ( df[ "파울" ] / df[ "출장" ] ).round( 2 )

# ============================================================
# 4. 범주 컬럼 ( np.where 겹치기 )
# ============================================================
df[ "선수유형" ] = np.where( df[ "도움" ] >= 7 , "도우미형" ,
                   np.where( df[ "도움" ] <= 2 , "골잡이형" , "균형형" ) )

df[ "결정력등급" ] = np.where( df[ "골결정력" ] >= 22 , "효율형" ,
                     np.where( df[ "골결정력" ] < 15 , "물량형" , "보통" ) )

df[ "출전비중" ] = np.where( df[ "출장" ] >= 30 , "주전" ,
                   np.where( df[ "출장" ] < 20 , "로테이션" , "준주전" ) )

df[ "플레이스타일" ] = np.where( df[ "경기당파울" ] >= 1.0 , "거친편" ,
                       np.where( df[ "경기당파울" ] >= 0.6 , "보통" , "깨끗한편" ) )

# ============================================================
# 5. 출력 함수
# ============================================================
def print_title( title ) :
    print( "\n" + "=" * 60 )
    print( f"  { title }" )
    print( "=" * 60 )

# 순위표 : 정렬 → 상위 n명 → 1위부터 번호 붙여서 출력
def print_rank( title , sort_by , ascending , show_cols , n = 10 ) :
    print_title( title )
    result = df.sort_values( by = sort_by , ascending = ascending ).head( n )
    result.index = range( 1 , len( result ) + 1 )      # 인덱스를 1, 2, 3 ... 순위로
    print( result[ show_cols ] )

# 범주별 출력 : 범주 하나씩 나눠서 출력
def print_group( col , order , show_cols , sort_by ) :
    print_title( f"{ col } 별 선수" )
    for name in order :
        group = df[ df[ col ] == name ].sort_values( by = sort_by , ascending = False )
        group.index = range( 1 , len( group ) + 1 )
        print( f"\n { name } ( { len( group ) }명 )" )
        print( group[ show_cols ] )

# ============================================================
# 6. 순위표
# ============================================================
print_rank( "득점 순위 TOP 10" ,
            [ "득점" , "출장" ] , [ False , True ] ,
            [ "선수명" , "팀" , "득점" , "출장" , "경기당득점" ] )

print_rank( "공격포인트 순위 TOP 10 ( 득점 + 도움 )" ,
            [ "공격포인트" , "득점" ] , [ False , False ] ,
            [ "선수명" , "팀" , "득점" , "도움" , "공격포인트" ] )

print_rank( "골결정력 순위 TOP 10 ( 득점 ÷ 슈팅 × 100 )" ,
            "골결정력" , False ,
            [ "선수명" , "팀" , "득점" , "슈팅" , "골결정력" ] )

print_rank( "경기당 득점 순위 TOP 10" ,
            "경기당득점" , False ,
            [ "선수명" , "팀" , "득점" , "출장" , "경기당득점" ] )

print_rank( "경기당 파울 순위 TOP 10" ,
            "경기당파울" , False ,
            [ "선수명" , "팀" , "파울" , "경고" , "퇴장" , "출장" , "경기당파울" ] )

# ============================================================
# 7. 범주별 선수 목록
# ============================================================
print_group( "선수유형" , [ "도우미형" , "균형형" , "골잡이형" ] ,
             [ "선수명" , "팀" , "득점" , "도움" , "공격포인트" ] , "공격포인트" )

print_group( "결정력등급" , [ "효율형" , "보통" , "물량형" ] ,
             [ "선수명" , "팀" , "득점" , "슈팅" , "골결정력" ] , "골결정력" )

print_group( "출전비중" , [ "주전" , "준주전" , "로테이션" ] ,
             [ "선수명" , "팀" , "출장" , "득점" , "경기당득점" ] , "출장" )

print_group( "플레이스타일" , [ "거친편" , "보통" , "깨끗한편" ] ,
             [ "선수명" , "팀" , "파울" , "출장" , "경기당파울" ] , "경기당파울" )

# ============================================================
# 8. 요약 표 ( groupby + agg )
# ============================================================

# 8-1) 범주별 평균 비교
print_title( "선수유형별 평균 기록" )
type_summary = df.groupby( "선수유형" ).agg(
    인원 = ( "선수명" , "count" ) ,
    평균득점 = ( "득점" , "mean" ) ,
    평균도움 = ( "도움" , "mean" ) ,
    평균슈팅 = ( "슈팅" , "mean" ) ,
    평균골결정력 = ( "골결정력" , "mean" )
).round( 1 )
print( type_summary )

print_title( "결정력등급별 평균 기록" )
grade_summary = df.groupby( "결정력등급" ).agg(
    인원 = ( "선수명" , "count" ) ,
    평균득점 = ( "득점" , "mean" ) ,
    평균슈팅 = ( "슈팅" , "mean" ) ,
    평균출장 = ( "출장" , "mean" )
).round( 1 )
print( grade_summary )

# 8-2) 팀별 요약 : 득점 상위 30명 안에 몇 명 , 합계 득점
print_title( "팀별 요약 ( 득점 상위 30명 기준 )" )
team_summary = df.groupby( "팀" ).agg(
    인원 = ( "선수명" , "count" ) ,
    합계득점 = ( "득점" , "sum" ) ,
    합계도움 = ( "도움" , "sum" ) ,
    평균골결정력 = ( "골결정력" , "mean" )
).round( 1 ).sort_values( by = "합계득점" , ascending = False )
print( team_summary )

# 8-3) 범주 2개 교차 : 선수유형 x 결정력등급 인원
print_title( "선수유형 및 결정력등급 인원" )
cross = df.groupby( [ "선수유형" , "결정력등급" ] ).agg(
    인원 = ( "선수명" , "count" ) ,
    선수 = ( "선수명" , lambda x : ", ".join( x ) )      # 해당 선수 이름 나열
)
pd.set_option( 'display.max_colwidth' , None )    # 칸 안의 글자 생략 없이
print( cross )