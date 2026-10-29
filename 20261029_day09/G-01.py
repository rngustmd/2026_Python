# 맷플롯립 : 파이썬에서 시각적으로 표현 하는 라이브러리
# 설치 : pip install matplotlib
# 확인
import matplotlib
print( matplotlib.__version__)

import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')      # 윈도우 맑은 고딕으로 설정
plt.rcParams['axes.unicode_minus'] = False  # 

# 1] 선 차트 
epochs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
train_loss = [0.9, 0.7, 0.55, 0.45, 0.38, 0.32, 0.28, 0.25, 0.23, 0.20]
val_loss = [0.95, 0.75, 0.60, 0.52, 0.48, 0.45, 0.44, 0.43, 0.44, 0.45]

# 1) 차트 전체크기 설정 : plt.figure( figsize=(가로inch , 세로inch) )
plt.figure( figsize=( 7 , 4 ) )
# 2) 선차트 : plt.plot( x축값 , y축값 , label="계열명" , color = "색상명" , linestyle = "선종류" , marker = "")
plt.plot( epochs , train_loss , label="Train Loss" , color = "blue" , linestyle = "-" , marker = "o" )
plt.plot( epochs , train_loss , label = "값 손실" , color = "red" , linestyle = "--" , marker = "s" )
# 3) 차트의 제목
plt.title( "학습별 모델 손실 추세") 
# 4) x축 제목
plt.xlabel("학습수")
# 5) y축 제목
plt.ylabel("손실")
# 6) 구분선
plt.grid( True ) 
# 7) 범례 표시
plt.legend( )
# plt # 맷플롯립 별칭
plt.show() # 차트 실행

# 2] 막대 차트(비교) plt.bar , 선 차트(추세) plt.plot
classes = ['Cat', 'Dog', 'Bird', 'Fish']
counts = [120, 150, 80, 45]
# 1) plt.bar( x값 , y값 , color = [색상] , width = 막대크기 )
bars = plt.bar( classes , counts , width=0.5 ,
        color=[ '#222222' , '#444444' , '#666666' , '#888888' ] )
# 2) 막대 값 레이블 , plt.bar_label( 막대차트변수 , padding=막대와레이블간격 , fontsize=폰트크기 )
plt.bar_label( bars , padding=3 , fontsize=8 )
plt.title( '클래스별 샘플수')
plt.xlabel("클래스")
plt.ylabel("샘플 수")
plt.grid( True , alpha=0.5 ) # alpha="투명도"
plt.show( )

# 3] 산점도 ( 상관관계 )
x = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]
y = [2.3, 3.8, 5.1, 7.0, 7.8, 9.2, 10.5]
# 1) 산점도 plt.scatter( x축값 , y축값 , color="색상" , s=점크기 , alpha=투명도)
plt.scatter( x , y , color = "purple" , s = 80 , alpha=0.8 )
plt.title( "공부시간과 시험점수의 상관관계" )
plt.xlabel( "공부시간" )
plt.ylabel( "시험점수" )
plt.show() 

# 4] 히스토그램 ( 연속형 수치 )
import numpy as np
# 평균 170 을 중심으로 표준편차 5 만큼 퍼져있는 종모양( 가우시안분포 )
heights = np.random.normal( loc=170 , scale=5 , size=1000 ) 
# 1) 히스토그램
plt.hist( heights , bins=30 , edgecolor="black" )
plt.xlabel( "키(cm)" )
plt.ylabel( "빈도/분포 수")
plt.show()

# 5] 박스플롯 ( 분포 범위 내 이상치 )
heights = np.random.normal(loc=170, scale=5, size=1000)
data_with_outliers = np.append(heights, [210, 215, 120]) # 이상치

# 1) plt.boxplot( 값 ) , 데이터들을 사분위수( 25% 50% 75% ) 표현 
plt.boxplot( data_with_outliers , vert=True , patch_artist=True )
plt.title( '데이터 이상치(Outliner) 탐지용 Boxplot' )
plt.ylabel("값")
plt.grid( axis='y' , linestyle=':' , alpha=0.6)
plt.show()

# 6] 한 창에 2개 이상 그래프 표현
# fig, axs = plt.subplots( 행개수 , 열개수 , figsize  = ( 가로,세로 ) )
fig, axs = plt.subplots( 1 , 2 , figsize  = ( 10 , 4 ) ) # 1줄(행) 차트 2개
# 1행 1열 차트 , axs[인덱스].차트종류()
axs[0].plot( [ 1,2,3] , [4,5,6] )
axs[0].set_title("서브1: 선그래프")
axs[0].set_xlabel('X축')
axs[0].set_ylabel('Y축')
axs[0].grid(True)
# 1행 2열 차트
axs[1].bar( [ 'A','B',"C" ] , [ 30,15,40 ] )
axs[1].set_title("서브2: 막대그래프")
axs[1].set_xlabel('범주')
axs[1].set_ylabel('값')
axs[1].grid(axis='y')
# 여백 자동 조정 (레이블 겹침 방지 필수 옵션)
plt.tight_layout()
# ※ 주의: plt.show() 호출 전에 savefig를 실행해야 백지 저장 방지
plt.savefig('eda_summary.png', dpi=200)
plt.show()