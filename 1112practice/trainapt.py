import joblib
import pandas as pd
df = pd.read_csv('./1112practice/apt_data.csv')
df.info()

num_features = [ 'area' , 'floor' , 'build_year' , 'contract_year' ]
cat_features = [ 'dong' ]

# 다중분류 특성 / 타깃 구성
X = df.drop( columns=['price'] )
Y = df['price']

# 분리
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

# 복합 특성
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, OneHotEncoder
pp = ColumnTransformer( transformers=[ 
    ('num', StandardScaler(), num_features) , # 수치형 특성
    ('cat', OneHotEncoder(drop='first', sparse_output=False, 
                          handle_unknown='ignore'), cat_features)
] )

# 파이프라인
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
pipe = Pipeline( [ 
    ('pp' , pp) , 
    ('poly' , PolynomialFeatures( include_bias=False ) ) , 
    ('scaler' , StandardScaler() ) , 
    ('ridge' , Ridge() )
] )

# 하이퍼 파라미터 후보
param_grid = { 
    'poly__degree' : [ 1, 2, 3 ] , 
    'ridge__alpha' : [ 0.001 , 0.01 , 0.1 , 1 , 10 , 100 ] 
}

# K-Fold , GridSearchCV
kf = KFold( n_splits = 5 , shuffle = True , random_state = 42 )
grid = GridSearchCV( pipe , param_grid , cv=kf , scoring='r2' , n_jobs=-1 )
grid.fit( X_train , Y_train )

# 최적 모델 및 파라미터 확인
best_model = grid.best_estimator_
print( grid.best_params_ )
print( '교차검증 평균 r2:' , grid.best_score_ ) # 교차검증 평균 r2

# 결정계수 r2
from sklearn.metrics import r2_score
Y_pred = best_model.predict( X_test )
test_r2 = r2_score( Y_test , Y_pred )
print( '훈련 r2:' , best_model.score( X_train , Y_train ) ) # 훈련 r2
print( '테스트 r2:' , test_r2 ) # 테스트 r2

# 서빙
joblib.dump( best_model , './1112practice/apt_model.pkl' )
metrics = {
    'r2' : round( float( test_r2 ) , 4 ) ,
    'cv_r2' : round( float( grid.best_score_ ) , 4 ) ,
    'best_params' : grid.best_params_
}

joblib.dump( metrics , './1112practice/apt_metrics.pkl' )

model = joblib.load( './1112practice/apt_model.pkl' )
sample = pd.DataFrame( { 'dong' : ['여의도동'] , 'area' : [105.72] , 
                        'floor' : [2] , 'build_year' : [1975] ,
                        'contract_year' : [2026] 
} )
predict = model.predict( sample )
print( '예측 거래액(만원):' , predict )