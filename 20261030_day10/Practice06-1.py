# 1. 가설 
# 2. 가설 에 따른 자료 수집 
import pandas as pd
df = pd.read_csv( './day10/train.csv')
# 3. 자료 전처리 
# 수치형 결측치 보정: '나이(Age)' 컬럼의 결측치는 이상치에 강건한(Robust) 분석을 위해 중앙값(Median)으로 대체해야 한다.
df['Age'] = df['Age'].fillna( df['Age'].median() )
# 범주형 결측치 보정: '승선 항구(Embarked)' 컬럼의 결측치는 가장 빈번하게 등장하는 최빈값(Mode)으로 대체해야 한다.
# mode() : 문자열내 빈도가 높은 순으로 배열 반환 , [0] 첫번째/가장 빈번한
df['Embarked'] = df['Embarked'].fillna( df['Embarked'].mode()[0] )
df.info() # 결측 데이터 확인 

import matplotlib.pyplot as plt
import seaborn as sns 
# 윈도우 기준 한글 폰트 설정 및 마이너스 부호 깨짐 방지
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False
# 시본 기본 테마 적용 (폰트 설정 유지)
sns.set_theme(font='Malgun Gothic', rc={'axes.unicode_minus': False}, style='whitegrid')
# 5-1 : 생존 분포 분석: 전체 생존자와 사망자의 비중을 파악할 수 있는 막대그래프 를 생성한다.
#	0 = No(사망자) 1 = Yes(생존자)
# sns.countplot( data="판다스자료" , x = "컬럼명" ) # 그룹별 개수 
sns.countplot( data=df , x = "Survived")
plt.xticks( [0,1] , ['사망' , '생존'] ) # x축의 수치값을 범주값 으로 변경 
plt.show() 

# 5-2 : 연령대별 상세 분석:나이에 따른 생존/사망 분포를 히스토그램으로 시각화한다.데이터의 흐름을 파악할 수 있도록 커널 밀도 추정 곡선(KDE)을 포함한다.
# KDE : 밀도 추정 곡선 속성 
사망자나이 = df[df['Survived'] == 0 ]['Age']  # 사망자들의 나이만 추출 
생존자나이 = df[df['Survived'] == 1 ]['Age']  # 생존자들의 나이만 추출 
sns.histplot( data= 사망자나이 , label="사망자" , kde=True )
sns.histplot( data= 생존자나이 , label="생존자" , kde=True )
plt.legend()
plt.show() 
# 5-3 (성별): sns.countplot을 사용하여 성별(Sex)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
sns.countplot( data=df , x = "Sex" , hue="Survived")
plt.show()
# 5-4 (객실 등급): sns.countplot을 사용하여 객실 등급(Pclass)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
sns.countplot( data=df , x = "Pclass", hue="Survived")
plt.show()
# 5-5 (승선 항구): sns.countplot을 사용하여 승선 항구(Embarked)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
# C = Cherbourg, Q = Queenstown, S = Southampton( 사우샘프턴 )
sns.countplot( data=df , x = "Embarked" , hue="Survived")
plt.show()

