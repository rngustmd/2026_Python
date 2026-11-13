# 부스팅 앙상블
# 설치 : pip install lightgbm xgboost catboost

url = 'https://raw.githubusercontent.com/rickiepark/hg-mldl/master/wine.csv'

import time
import pandas as pd
df = pd.read_csv(url)
# alcohol , sugar , pH , class( 0:레드 / 1:화이트 )
X = df[ [ 'alcohol' , 'sugar' , 'pH' ] ]    # 독립변수
Y = df[ 'class' ]                           # 종속변수
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
# 분할
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=42,stratify=Y) 

# 3가지 부스팅 앙상블 사용 XGBClassifier(분류),XGBRFRegressor(회귀)
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier,XGBRFRegressor

# 1) 모델 비교 
# n_estimators  : 부스팅 사용할 트리 개수 기본값 100 , 권장 1000~3000( 최적 모델 탐색 후 중간 종료 )
# learning_rate : 학습률 , 경사하강법 에서 오차 보정 하기 위한 이동 단위 , 기본값 0.1
# max_depth : 트리의 최대 높이 제한 , LightGBM 기본값 제한 없음( 과대적합주의 )
# verbose=-1 : 실행 중 트리들이 처리하는 로그 끄기
models = {
    "XGBoost" : XGBClassifier( 
        n_estimators=100 , learning_rate=0.05 , 
        max_depth=4 , random_state=42, n_jobs=-1 ) ,
    "LightGBM" : LGBMClassifier( 
        n_estimators=100 , learning_rate=0.05 , 
        max_depth=4 , random_state=42, n_jobs=-1 , verbose=-1 ) 
}

# 2) 반복 이용하여 모델 학습 / 학습 시간 테스트
for name , model in models.items() : 
    start = time.time() # 학습 시작 시간
    model.fit( X_train , Y_train )
    end = time.time() - start # 현재 시간에서 시작시간 제외 ( 소요 시간 구하기 )
    Y_pred = model.predict( X_test ) # 예측

    print( "▶ 모델명:" , name )
    print( "> 학습 소요시간:" , end , "초" )
    print( "> train acc:" , model.score( X_train , Y_train ) )
    print( "> test acc:" , model.score( X_test , Y_test ) )
    print( "> f1 score:" , f1_score( Y_test , Y_pred , average="macro" ) )

# ▶ 모델명: XGBoost
# > 학습 소요시간: 0.18410277366638184 초
# > train acc: 0.8795458918606889
# > test acc: 0.8553846153846154
# > f1 score: 0.7995742182246408
# ▶ 모델명: LightGBM
# > 학습 소요시간: 0.08791708946228027 초       빠르다.
# > train acc: 0.8795458918606889
# > test acc: 0.8607692307692307                과대적합 우수
# > f1 score: 0.8068193666663657