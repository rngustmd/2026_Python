# 로지스틱 회귀 : 범주형 을 예측하는 대표적인 분류 알고리즘
import pandas as pd
df = pd.read_csv( './20261106_day15/Fish.csv' )

# 1) 이진 분리 실습하기 위한 정답지 2개 사용
df = df[ (df[ 'Species' ] == 'Bream') | (df[ 'Species' ] == 'Smelt') ]
X = df[ [ 'Weight','Length1','Length2','Length3','Height','Width' ] ]
Y = df[ 'Species' ] # Bream 또는 Smelt

# 2) 분리
# stratify = Y : 타깃 무작위 분리 한 경우 클래스 비율 일정 유지 , 분류모델
from sklearn.model_selection import train_test_split
X_train , X_test , Y_train , Y_test = train_test_split( 
    X , Y , test_size= 0.2 , random_state= 42, stratify= Y )

# 3) 스케일링
from sklearn.preprocessing import StandardScaler
ss = StandardScaler() 
ss.fit( X_train )
X_train_scaled = ss.transform( X_train )
X_test_scaled = ss.transform( X_test )

# 4) 로지스틱 모델 사용
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit( X_train_scaled , Y_train )
Y_pred = model.predict( X_test_scaled )
print( Y_pred ) 
# ['Bream' 'Bream' 'Smelt' 'Bream' 'Bream' 'Smelt' 'Smelt' 'Bream' 'Bream' 'Bream']

# 5) 결과 속성
print( model.classes_ ) # 정답지 종류
print( model.predict_proba( X_test_scaled[ : 3 ] ) )

# 6) 정확도 평가 : accuracy_score( 테스트정답지 , 테스트예측 )
from sklearn.metrics import accuracy_score
acc = accuracy_score( Y_test , Y_pred )
print( acc ) # 1.0 => 100% 현재 실습은 데이터가 적다.


