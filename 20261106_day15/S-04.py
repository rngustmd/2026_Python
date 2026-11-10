import pandas as pd
df = pd.read_csv( "./20261106_day15/Fish.csv" ) # 자료 수집
X = df[ [ 'Length2' , 'Height' , 'Width' ] ]    # 특성 선정/구성
Y = df[ 'Weight' ] # 타깃(정답) 선정/구성

# 3) 훈련/테스트 분리
from sklearn.model_selection import train_test_split
train_test_split( X , Y , test_size= 0.2 )
X_train,X_test,Y_train,Y_test = train_test_split( X, Y, test_size=0.2, random_state= 42 )

# 4) 과소적합 방지하고자 항 추가 PolynominalFeatures # 제곱 / 곱셈
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures( degree=2 , include_bias=False )
poly.fit( X_train )
X_train_poly = poly.transform( X_train )
X_test_poly = poly.transform( X_test )

# 5) 항 많아지면 항/특성 간에 단위 표준화 / 스케일링
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
ss.fit( X_train_poly )
X_train_scaled = ss.transform( X_train_poly )
X_test_scaled = ss.transform( X_test_poly )

# 6) 모델 선택 , 단순선형회귀 , 규제 ( 릿지 / 라쏘 )
from sklearn.linear_model import LinearRegression
model = LinearRegression() 
model.fit( X_train_scaled , Y_train )

# 7) 결정계수
print( 'r2: ' , model.score( X_train_scaled , Y_train ) )
print( 'r2: ' , model.score( X_test_scaled , Y_test ) )
# r2:  0.9833194466740021
# r2:  0.9719372415762589

# 8) ============  (4) ~ (6) 과정 묶음 
from sklearn.pipeline import Pipeline
# pipe_model = Pipeline( [ ("식별자" , 클래스명() ) ] ) # 파이썬 인스턴스생성 , 변수 = 클래스명( 인자값 )
# [] 리스트 ()튜플
pipe_model = Pipeline( [ 
    ( 'poly' , PolynomialFeatures( degree=2 , include_bias=False ) ) , # 4
    ( 'scaler' , StandardScaler( ) ) ,                                # 5
    ( 'regressor' , LinearRegression() )                              # 6 
])
# 9) 파이프라인 으로 학습 
pipe_model.fit( X_train , Y_train )
print( 'r2 : ' , pipe_model.score( X_train , Y_train ))
print( 'r2 : ' , pipe_model.score( X_test , Y_test ))

