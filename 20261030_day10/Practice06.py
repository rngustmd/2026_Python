# [1. 타이타닉 생존 데이터 분석]
# 출처: Kaggle - Titanic: Machine Learning from Disaster

# [2. 가설]
# 가설 1: 여성과 아동의 생존율이 남성보다 월등히 높을 것이다. (사회적 보호 )
# 가설 2: 높은 객실 등급(1등석)을 이용한 승객일수록 생존율이 높을 것이다. (경제적 지위와 안전의 상관관계)
# 가설 3: 특정 항구(사우샘프턴 등)에서 탑승한 승객은 객실 등급 분포에 따라 생존율 차이가 발생할 것이다.

# [3. 자료수집 ]
# 3-1 : https://www.kaggle.com/competitions/titanic/overview
# 3-2 : train.csv 파일 판다스로 불러오기 

# [4. 데이터 전처리]
# 수치형 결측치 보정: '나이(Age)' 컬럼의 결측치는 이상치에 강건한(Robust) 분석을 위해 중앙값(Median)으로 대체해야 한다.
# 범주형 결측치 보정: '승선 항구(Embarked)' 컬럼의 결측치는 가장 빈번하게 등장하는 최빈값(Mode)으로 대체해야 한다.

# [5. 데이터 시각화 및 분석]
# 5-1 : 생존 분포 분석: 전체 생존자와 사망자의 비중을 파악할 수 있는 막대그래프 를 생성한다.
# 5-2 : 연령대별 상세 분석:나이에 따른 생존/사망 분포를 히스토그램으로 시각화한다.데이터의 흐름을 파악할 수 있도록 커널 밀도 추정 곡선(KDE)을 포함한다.
# 5-4 (성별): sns.countplot을 사용하여 성별(Sex)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
# 5-5 (객실 등급): sns.countplot을 사용하여 객실 등급(Pclass)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
# 5-6 (승선 항구): sns.countplot을 사용하여 승선 항구(Embarked)에 따른 생존 여부(Survived)별 인원수를 시각화한다.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(font='Malgun Gothic', rc={'axes.unicode_minus': False}, style='whitegrid')

# [3. 자료수집 ]
df = pd.read_csv( './20261030_day10./train.csv')
print( df.head() )
df.info( )
print(df.isnull().sum())

# [4. 데이터 전처리]
# 수치형 결측치 보정: '나이(Age)' 컬럼의 결측치는 이상치에 강건한(Robust) 분석을 위해 중앙값(Median)으로 대체해야 한다.
나이중앙값 = df['Age'].median()
df['Age'] = df['Age'].fillna(나이중앙값)
# 범주형 결측치 보정: '승선 항구(Embarked)' 컬럼의 결측치는 가장 빈번하게 등장하는 최빈값(Mode)으로 대체해야 한다.
항구최빈값 = df['Embarked'].mode()[0]
df['Embarked'] = df['Embarked'].fillna(항구최빈값)

print('나이 중앙값 :' , 나이중앙값 , '/ 항구 최빈값 :' , 항구최빈값 )
print(df[ ['Age' , 'Embarked' ] ].isnull().sum())

# [5. 데이터 시각화 및 분석]
# 5-1 : 생존 분포 분석: 전체 생존자와 사망자의 비중을 파악할 수 있는 막대그래프 를 생성한다.
생존자수 = df['Survived'].sum()
사망자수 = len(df) - 생존자수

plt.figure(figsize=(6, 4))
# plt.bar( x값 , y값 , color = [색상] , width = 막대크기 )
bars = plt.bar(['사망', '생존'], [사망자수, 생존자수], width=0.5, 
               color=['#888888', '#4C72B0'])
plt.bar_label(bars, padding=3, fontsize=10)
plt.title('전체 생존자와 사망자 비중')
plt.xlabel('생존 여부')
plt.ylabel('인원 수')
plt.grid(axis='y', alpha=0.5)
plt.show()
print('전체 생존율 :', round(생존자수 / len(df) * 100, 1), '%')

# 5-2 : 연령대별 상세 분석:나이에 따른 생존/사망 분포를 히스토그램으로 시각화한다.
# 데이터의 흐름을 파악할 수 있도록 커널 밀도 추정 곡선(KDE)을 포함한다.
plt.figure( figsize=(8,4))
sns.histplot( data=df , x='Age' , hue='Survived' , bins=30 , kde=True , palette='Set1')
plt.title('나이에 따른 생존/사망 분포')
plt.xlabel('나이')
plt.ylabel('인원 수')
plt.show()

# 5-4 (성별): sns.countplot을 사용하여 성별(Sex)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
sns.countplot( data=df , x='Sex' , hue='Survived' , palette='Set1' )
plt.title('성별에 따른 생존 여부')
plt.xlabel('성별')
plt.ylabel('인원 수')
plt.legend( title='생존 여부' , labels=['사망(0)' , '생존(1)'] )
plt.show()

# 5-5 (객실 등급): sns.countplot을 사용하여 객실 등급(Pclass)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
sns.countplot( data=df , x='Pclass' , hue='Survived' , palette='Set1' )
plt.title('객실 등급에 따른 생존 여부')
plt.xlabel('객실 등급')
plt.ylabel('인원 수')
plt.legend( title='생존 여부' , labels=['사망(0)' , '생존(1)'] )
plt.show()

# 5-6 (승선 항구): sns.countplot을 사용하여 승선 항구(Embarked)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
sns.countplot( data=df , x='Embarked' , hue='Survived' , palette='Set1')
plt.title('승선 항구에 따른 생존 여부')
plt.xlabel('승선 항구')
plt.ylabel('인원 수')
plt.legend( title='생존 여부' , labels=['사망(0)' , '생존(1)'])
plt.show()

# [1. 서울시 공공자전거 대여이력 분석]
# 출처: 서울 열린데이터 광장

# [2. 가설]
# 가설 1: 출퇴근 시간대(08시, 18시 전후)의 자전거 대여량이 다른 시간대에 비해 압도적으로 높을 것이다.
# 가설 2: 특정 지하철역 인근이나 유동인구가 많은 지역의 대여소가 대여량 상위권을 차지할 것이다.
# 가설 3: 이용시간과 이용거리 사이에는 강한 양의 상관관계가 존재할 것이다.

# [3. 자료수집]
# 3-1 : https://data.seoul.go.kr/dataList/OA-15182/F/1/datasetView.do
# https://drive.google.com/file/d/1tXfjwXu5HQUyKupqWeEiNk7ZlN0Xf7xw/view
# 3-2 : 2025년 1월, 2월 대여이력 CSV 파일 로드 (encoding='cp949')

pd.set_option('display.unicode.east_asian_width', True)

data1 = pd.read_csv('./20261030_day10./서울특별시 공공자전거 대여이력 정보_2501.csv', encoding='cp949')
data2 = pd.read_csv('./20261030_day10./서울특별시 공공자전거 대여이력 정보_2502.csv', encoding='cp949')

# [4. 데이터 전처리 및 병합]
# 4-1 (병합): pd.concat을 사용하여 분리된 월별 데이터를 하나로 통합하고 인덱스를 재부여한다.
df = pd.concat( [data1 , data2] , ignore_index=True )
print( '1월:' , len(data1) , '건 / 2월:' , len(data2) , '건 / 병합:' , len(df) , '건' )
df.info()
print( df.columns )

# 4-2 (정제): 결측치의 문자열 표현('\N')을 None으로 치환하고, 성별 데이터를 대문자로 통일 및 결측치를 'U'로 보정한다.
df = df.replace( '\\N' , None )
df['성별'] = df['성별'].str.upper()
df['성별'] = df['성별'].fillna( 'U' )
print( df.isnull().sum() )
print( df['성별'].value_counts() )

# 4-3 (형변환): 이용시간, 거리 등 주요 수치형 변수는 pd.to_numeric으로 변환하고, 날짜 데이터는 pd.to_datetime으로 객체화한다.
df['이용시간(분)'] = pd.to_numeric( df['이용시간(분)'] )
df['이용거리(M)'] = pd.to_numeric( df['이용거리(M)'] )
df['대여일시'] = pd.to_datetime( df['대여일시'] )
df.info()

# 4-4 (파생변수): 대여일시에서 시간(Hour) 
df['대여시간대'] = df['대여일시'].dt.hour
print( df[ ['대여일시' , '대여시간대'] ].head() )

# [5. 데이터 시각화 및 분석]
# 5-1 (성별 분포): sns.countplot을 사용하여 성별에 따른 따릉이 이용 비중을 시각화한다.
sns.countplot( data=df , x='성별' , hue='성별' , palette='Set2' )
plt.title( '성별에 따른 따릉이 이용 비중' )
plt.xlabel('성별')
plt.ylabel('이용건수')
plt.show()

# 5-2 (시간대 분석): sns.barplot을 사용하여 24시간 중 어느 시간대에 대여가 집중되는지 분석한다.
시간대별건수 = df['대여시간대'].value_counts()
시간대별건수 = 시간대별건수.sort_index()

plt.figure( figsize=( 10 , 4 ) )
sns.barplot( x=시간대별건수.index , y=시간대별건수.values , color="#B368D6" )
plt.title( '시간대에 따른 따릉이 대여 건수' )
plt.xlabel( '대여시간대' )
plt.ylabel( '대여건수' )
plt.show()

# 5-3 (인기 대여소): value_counts().head(10)를 활용하여 가장 활발한 상위 10개 대여소를 가로 막대 그래프로 시각화한다.
상위대여소 = df['대여 대여소명'].value_counts().head(10)
print( 상위대여소 )

plt.figure( figsize=(8 , 5) )
bars = plt.barh( 상위대여소.index[::-1] , 상위대여소.values[::-1] , color="#3A7256")
plt.bar_label( bars , padding=3 , fontsize=8 )
plt.title('상위 10개 대여소')
plt.xlabel('대여건수')
plt.show()

# 5-4 (상관관계): sns.heatmap을 통해 이용시간, 이용거리, 시간대 등 수치 데이터 간의 밀접도를 분석한다.
numeric_df = df[ ['이용시간(분)' , '이용거리(M)' , '대여시간대'] ]
corr_matrix = numeric_df.corr()
sns.heatmap( corr_matrix , cmap='coolwarm' , fmt='.2f' , annot=True )
plt.title( '데이터 간 밀접도')
plt.show()