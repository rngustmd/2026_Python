# 사이킷런 ? 방대한 머신러닝 알고리즘 모델 제공 라이브러리
# pip install scikit-learn

# 특성 : 모델이 학습하는 자료 정보 , 타깃 : 모델이 맞혀야 하는 정답 정보

# 지도학습 : 특성과 타깃을 모두 제공하여 학습 ( 회귀 / 분류 )
# 비지도학습 : 타깃 없이 특성만으로 제공하는 학습 ( 군집 /  )

# 1] 단순 선형 회귀
# 

# 1) 판다스로 자료 불러오기
import pandas as pd
df = pd.read_csv( './20261104_day13/Fish.csv' )
df.info()
# 2) 모델 학습에 사용할 데이터 추출
# 특성 : Length2 ( 물고기의 대각선 cm ) # 사이킷런 모델 구조상 학습할 특성은 2차원
feature = ['Length2']
# 타깃 : Weight( 물고기의 무게 g )
target = 'Weight'
# 3) x y 구조
X = df[feature] # 2차원
Y = df[target] # 1차원
# 4) 데이터 분리 , 학습용/테스트용 나누기 , 학습 과 평가/예측성능 자료 구분
from sklearn.model_selection import train_test_split
# 타깃학습자료, 특성테스트자료, 타깃학습자료, 타깃테스트자료 = train_test_split( 특성 , 타깃 , test_size=비율 , random_state=난수시드값)
X_train,X_test,Y_train,Y_test = train_test_split( X , Y , test_size=0.2 , random_state=42)
# 훈련세트 : 모델 에서 규칙을 찾는 자료
# 테스트세트 : 모델 학습 후 모델 평가/예측성능 점수/지표
# 5) 단순 선형회귀 모델
from sklearn.linear_model import LinearRegression
model = LinearRegression() # 파이썬에서 객체 생성 방법 , 변수명 = 클래스명()
# 6) 모델 학습 , model.fit( 특성자료 , 타깃자료 )
model.fit( X_train , Y_train )
# 7) 모델 가중치( 기울기 ) 확인 , model.coef_
print( model.coef_ ) # [30.43452394]
# 8) 모델 편향( y절편 ) 확인
print( model.intercept_ ) # -477.30634978973194
# 9) 학습한 모델의 예측 , y = ax+b , 기울기/y절편 , 새로운 x값을 넣어서 y값 구하기 , model.predict( 2차원 특성자료 )
print( model.predict( [ [ 30 ] ] ) ) # 만약 물고기 길이가 30일 때 무게 예측
# *) 단순회귀모델 : y = ax+b , [30.43452394]*[ 30 ] + [-477.30634978973194]
# 10) 시각화
import matplotlib.pyplot as plt
plt.scatter( X_train , Y_train ) # 학습 자료들
plt.scatter( [30] , model.predict( [[30]] ) , color="red" )
plt.plot( [0,100] , model.predict( [ [0] , [100] ] ) ) # 회귀선 : 임의의 최솟값/최댓값
plt.show()
# 11) 문제점
# x , y 가 직선 관계이며 실 자료들은 꼭 비례 증가가 아닐 수 있다. 
# 해결 : 다항 회귀 로 확장하여 특성 추가한다.  

# 12) 모델 평가
Y_pred = model.predict( X_test ) # 테스트용 특성을 넣어서 테스트 예측 결과
# -평균 제곱근 오차계산
import numpy as np # sqrt(제곱근) 넘파이 함수 사용
from sklearn.metrics import mean_squared_error # 평균 오차 ( 학습자료 와 테스트자료 )
rmse = np.sqrt( mean_squared_error( Y_test , Y_pred ) )
print( "rmse: ", rmse ) # 160.01413830813442
# 모델이 실제 무게 와 얼마나 틀렸는지 평균 오차

# -결정계수 (R SCORE): 타깃 데이터의 전체 변동성 대비 모델이 얼마나 잘 설명하는지 0~1 비율
from sklearn.metrics import r2_score # 결정계수
r2 = r2_score( Y_test , Y_pred ) # 정답지 와 예측값
print( "r2: " , r2 ) # 0.8199897860284712


