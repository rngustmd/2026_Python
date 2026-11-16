import pandas as pd
url = 'https://raw.githubusercontent.com/rickiepark/hg-mldl/master/wine.csv'
df = pd.read_csv(url)
X = df[['alcohol', 'sugar', 'pH']]
Y = df['class'] 
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)
# 1) lightGBM : LGBMclassifier 분류모델 , LGBMRegressor 회귀모델
from lightgbm import LGBMClassifier
model = LGBMClassifier(
    # 다양한 매개변수(파라미터) 설정
    n_estimators=310 ,          # 1) 추정기(모델) 최대 개수 설정 , 기본값 100 , 넉넉 넣고 조기 종료
    learning_rate=0.05 ,        # 2) 학습률(각 트리의 축소 비율) , 기본값 0.1
    num_leaves=15 ,             # 3) 하나의 트리(모델) 가질 수 있는 최대 리프 노드 수 (과적합 억제)
    max_depth=10 ,               # 4) 하나의 트리 최대 깊이, 기본값 -1 (무제한)
    min_child_samples=20 ,      # 6) 리프 노드 최소 샘플 수
    subsample=0.8 ,             # 7) 매 반복 마다 랜덤으로 80% 만 무작위 샘플링 
    subsample_freq=1 ,          # 8) 7)와 같이 설정하되 , 매 트리마다 배깅을 활성화
    colsample_bytree=0.8 ,      # 9) 매 학습마다 랜덤으로 전체 특성 중 80% 만 무작위 선택 학습
    class_weight="balanced" ,   # 10) *분류모델* 에서 타깃/종속 변수에 비율 불균형 보정/완화
    verbose=-1 ,                # 매 학습마다 로그 숨김                                
    random_state=42 , n_jobs=-1 ,
)

from lightgbm import early_stopping
# 2) 모델 학습 수행 , 
# 조기 종료 하기 위한 (성능) 검증용 데이터셋 포함
# 만약에 여러번 학습 중에 손실함수 결과 오차/잔차가 최적이 되면 종료 모니터링
#
model.fit( X_train , Y_train , 
          eval_set=[ (X_test,Y_test) ] , 
          callbacks=[ early_stopping( stopping_rounds=50, verbose=False) ]
)

# 3) 주요 속성 확인
print( model.best_iteration_ ) # 최적의 트리 반복 수/번호 # 310
print( model.feature_name_ ) # 각 특성의 이름             # ['alcohol', 'sugar', 'pH']
print( model.feature_importances_ ) # 각 특성의 중요도    # [ 579 2264 1497]

# 4) 평가지표
from sklearn.metrics import f1_score
Y_pred = model.predict( X_test )
print( model.score(X_train , Y_train ) )
print( model.score(X_test , Y_test ) )
print( f1_score( Y_test , Y_pred , average="macro" ) )
# 0.885703290359823
# 0.8530769230769231 # 학습 - 테스트 => 0.03 -> 3% ( 10% 아래로 과적합 억제 )
# 0.8197484027443542

# 5) 예측하기
new_wine = pd.DataFrame( [ [11.5 , 2.3 , 3.1] , [ 13.8 , 11.2 , 3.3 ] ] )
new_pred = model.predict( new_wine )
print( "예측1:" , new_pred[0] ) # 0 : 레드 와인
print( "에측2:" , new_pred[1] ) # 1 : 화이트 와인