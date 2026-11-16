import pandas as pd
url = 'https://raw.githubusercontent.com/rashida048/Datasets/master/USA_cars_datasets.csv'
df = pd.read_csv(url)

df = df[df['price'] > 0]
num_cols = ['year', 'mileage']                                  # 수치형
cat_cols = ['brand', 'model', 'title_status', 'color', 'state'] # 범주형 
# *만약에 모델의 성능 향상 하기 위한 도메인 지식의 특성 추가 좋다.*
# 범주형 자료들을 원핫인코딩이 아닌 판다스 '카테고리' 타입 변경 # lightGBM 내장 원핫인코딩 사용 목적
for col in cat_cols: 
    df[col] = df[col].astype('category')
X = df[num_cols + cat_cols]
Y = df['price']
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 1) 튜닝 -> optuna
# 1. optuna 설치 : $env:PYYAML_FORCE_LIBYAML = "0" , pip install optuna,shap

# 2) optuna 로그 숨기기 / 경고만 출력
import optuna
from lightgbm import LGBMRegressor , early_stopping
import numpy as np

optuna.logging.set_verbosity( optuna.logging.WARNING )

# 4) 목적함수 만들기 : 각 탐색 시도 마다 교차 검증 수행 후 평균 성능 반환, * 콜백함수( trial )
def objective( trial ) :
    # 4-1 교차검증 KFold
    from sklearn.model_selection import KFold
    cv = KFold( n_splits=5 , shuffle=True, random_state=42 )
    cv_r2_scores= [ ]       # 각 폴더별 검증 점수 저장 
    best_iterations = [ ]   # 각 폴더별 최적 트리 번호 저장 
    for train_idx, val_idx in cv.split( X_train , Y_train ) :
        # K번째 폴드의 훈련용/검증용 인덱스 반환 
        # 훈련 데이터 세트 내부에서 훈련용/검증용 분할 수행 , K=5 , 5개 폴드, 각각 한번씩 검증용
        X_tr, X_val = X_train.iloc[ train_idx ] , X_train.iloc[val_idx]
        Y_tr, Y_val = Y_train.iloc[ train_idx ] , Y_train.iloc[val_idx]
        # k폴드에서 분할한 훈련용 모델 만들기
        model = LGBMRegressor(
            n_estimators=1000, 
            # trial.suggest_XXX( '파라미터명' , 시작값, 끝값 )
            learning_rate=trial.suggest_float( 'learning_rate' , 0.01 , 0.1 )  ,
            num_leaves=trial.suggest_int( 'num_leaves' , 10, 30 ),
            max_depth=trial.suggest_int( 'max_depth' , 3 , 10 ),
            min_child_samples=trial.suggest_int( 'min_child_samples', 10 , 50 ),
            subsample=trial.suggest_float( 'subsample' , 0.6 , 1.0 ) , 
            subsample_freq=1, verbose=-1,random_state=42, n_jobs=-1 , 
            colsample_bytree=trial.suggest_float('colsample_bytree',0.6,1.0),
            # class_weight 회귀모델 이므로 생략 
        )
        # 4-2 교차별 학습 모델
        # K폴드별 훈련용/검증용 으로 학습 
        model.fit( X_tr , Y_tr , eval_set=[ (X_val,Y_val)] , 
                  callbacks=[ early_stopping( stopping_rounds=50, verbose=False ) ] )
         # 4-3 교차별 학습 성능 저장 
        # K폴드별 검증 평가 r2
        r2 = model.score( X_val , Y_val )
        cv_r2_scores.append( r2 )                       # k폴드별 평가 점수 저장 
        best_iterations.append( model.best_iteration_ ) # k폴드별 최적 트리 번호 저장 
    # k폴드에서 산출된 최적 트리 개수의 평균값을 trial의 속성으로 저장 
    # k폴드만큼 구한 최적의 트리 리스트에서 평균값으로 trial 저장!
    trial.set_user_attr( 'best_n_estimators' , int( np.mean( best_iterations ) ) )
    return np.mean( cv_r2_scores ) # 검증 평가 평균 점수 반환 

# 3) optuna.create_study( direction='maximize/minimize' )
# 현재 실습은 회귀모델이며 r2 결정계수 평가지표 사용할 예정
sampler = optuna.samplers.TPESampler( seed=42 )
study = optuna.create_study( direction='maximize' , sampler= sampler )
# study.optimize( 목적함수 , n_trials=반복수 )
study.optimize( objective , n_trials=20 ) # -> 반복 수 만큼 목적함수 실행

# 5) 최적 모델
print( '최적 하이퍼파라미터:', study.best_params )
optimal_model = study.best_trial.user_attrs['best_n_estimators']
print( '최적 트리:' , optimal_model )

# 6) 최적 파라미터로 모델 학습 , 조기종료 없이 최적으로
final_model = LGBMRegressor(
    random_state=42 , verbose=-1 , n_jobs=-1 ,
    **study.best_params , 
    n_estimators=optimal_model
)
final_model.fit( X_train , Y_train )
print( 'train r2:' , final_model.score(X_train , Y_train ) )
print( 'test r2:' , final_model.score(X_test , Y_test ) )
print( final_model.feature_name_ )
print( final_model.feature_importances_)
# train r2: 0.8019492459052838
# test r2: 0.7205797276257827
# ['year', 'mileage', 'brand', 'model', 'title_status', 'color', 'state']
# [310 870 200 389  50 228 467]

# 7) joblib 저장 / 로드
import joblib
joblib.dump( final_model , './20261116_day19/gbm_model.pkl') 
model = joblib.load('./20261116_day19/gbm_model.pkl') # 다른 .py파일 또는 메소드 가정
# 8) 예측
new_cars = pd.DataFrame([
    {'year': 2019, 'mileage': 25000, 'brand': 'ford',   'model': 'f-150',  'title_status': 'clean vehicle',     'color': 'white', 'state': 'texas'},
    {'year': 2014, 'mileage': 85000, 'brand': 'nissan', 'model': 'altima', 'title_status': 'salvage insurance', 'color': 'black', 'state': 'california'}
])
for col in cat_cols:
    new_cars[col] = new_cars[col].astype('category')
    ### 
preds = model.predict( new_cars )
print( '서빙 모델 에측 (1번차량) 가격: ', preds[0] ) # 27983.4777071311
print( '서빙 모델 에측 (2번차량) 가격: ', preds[1] ) # 635.4763331040908