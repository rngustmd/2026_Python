# PythonML Practice 3: 머신러닝 파이프라인 구축 및 하이퍼파라미터 최적화
# 데이터 출처: https://www.kaggle.com/datasets/shambhurajejagadale/student-performance-prediction-dataset

# 1. 데이터 준비 및 전처리
# - Kaggle 데이터셋('student_dataset_10000_rows.csv')을 불러옵니다.
# - 범주형 변수를 제외한 6개 수치형 컬럼을 독립변수(X, 문제지)로 추출하세요:
#   ['study_hours', 'attendance', 'sleep_hours', 'internet_usage', 'assignments_completed', 'previous_score']

# - 최종 시험 성적인 'exam_score' 컬럼을 종속변수(y, 정답지)로 설정하세요.
import pandas as pd
df = pd.read_csv( './20261110_day15/student_dataset_10000_rows.csv' )
X = df[ ['study_hours', 'attendance', 'sleep_hours', 'internet_usage', 'assignments_completed', 'previous_score'] ] # 특성(문제지)
Y = df[ 'exam_score' ] # 타깃(정답지)

# 2. 데이터 분할
# - train_test_split을 사용하여 전체 데이터를 훈련 세트(80%)와 테스트 세트(20%)로 분할하세요. 재현성을 위해 random_state=42로 고정합니다.
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split( X, Y, test_size=0.2, random_state=42 )

# 3. 단일 파이프라인(Pipeline) 구축
# - 데이터 누수(Data Leakage)를 방지하고 전처리부터 모델 학습까지 일괄 수행하기 위해 Pipeline 객체를 구성하세요. 파이프라인 단계는 아래 순서대로 3개의 변환기 및 예측기를 연결합니다:
#   1) 'poly': PolynomialFeatures(include_bias=False)
#   2) 'scaler': StandardScaler()
#   3) 'ridge': Ridge(random_state=42)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge
pipe_model = Pipeline( [
    ( 'poly' , PolynomialFeatures( include_bias=False ) ) ,
    ( 'scaler' , StandardScaler() ) ,
    ( 'ridge' , Ridge( random_state=42 ) )
] )

# 4. K-Fold 및 GridSearchCV 기반 하이퍼파라미터 최적화
# - KFold(n_splits=5, shuffle=True, random_state=42) 분할기를 생성하세요. 파이프라인 내부 파라미터를 탐색하기 위한 탐색 격자(param_grid)를 딕셔너리로 정의하세요:
#   - 다항식 차수('poly__degree'): [1, 2]
#   - 릿지 규제 강도('ridge__alpha'): [0.01, 0.1, 1.0, 10.0, 100.0]
# - GridSearchCV 객체를 생성하고 학습을 수행하세요:
#   - scoring='r2', cv=kf, n_jobs=-1
from sklearn.model_selection import KFold, GridSearchCV
kf = KFold( n_splits=5, shuffle=True, random_state=42 )
param_grid = {
    'poly__degree' : [ 1, 2 ] ,
    'ridge__alpha' : [ 0.01, 0.1, 1.0, 10.0, 100.0 ]
}
grid = GridSearchCV(
    estimator=pipe_model ,
    param_grid=param_grid ,
    scoring='r2' ,
    cv=kf ,
    n_jobs=-1
)
grid.fit( X_train , Y_train )
best_model = grid.best_estimator_ # 가장 성능 좋은 파이프라인
print( '최적 파라미터:' , grid.best_params_ )
print( '교차 검증 평균 r2:' , grid.best_score_ )
print( 'Train r2:' , best_model.score( X_train , Y_train ) )
print( 'Test r2:' , best_model.score( X_test , Y_test ) )

# 5. 최적 모델 파일 저장 및 복원 (joblib)
# - 최적 파이프라인 모델(best_estimator_)을 joblib.dump()를 사용하여 './best_student_performance_pipe.pkl' 파일로 저장하세요.
# - 저장된 피클 파일을 joblib.load()로 다시 불러와 새로운 파이프라인 객체(loaded_model)로 복원하세요.
import joblib
joblib.dump( best_model , './20261110_day15/best_student_performance_pipe.pkl' )
loaded_model = joblib.load( './20261110_day15/best_student_performance_pipe.pkl' )

# 6. 복원된 파이프라인 기반 신규 대조군 데이터 일괄 추론
# - 아래 대조군 샘플 2개를 독립변수와 동일한 컬럼 규격의 데이터프레임으로 생성하세요:
#   - 샘플 1 (상위권): study_hours=9, attendance=95, sleep_hours=7, internet_usage=2, assignments_completed=18, previous_score=85
#   - 샘플 2 (하위권): study_hours=2, attendance=60, sleep_hours=5, internet_usage=9, assignments_completed=4, previous_score=50
# - 복원된 파이프라인 객체의 .predict() 메서드에 원시 데이터프레임을 직접 전달하여 최종 예상 시험 점수를 산출하고 비교 출력하세요.
sample = pd.DataFrame( [
    [ 9 , 95 , 7 , 2 , 18 , 85 ] , # 샘플 1 (상위권)
    [ 2 , 60 , 5 , 9 , 4 , 50 ]    # 샘플 2 (하위권)
] , columns=['study_hours', 'attendance', 'sleep_hours', 'internet_usage', 'assignments_completed', 'previous_score'] )
# 파이프라인 안에서 poly -> scaler -> ridge 가 자동으로 수행되므로 원본 그대로 전달
sample_pred = loaded_model.predict( sample )
print( '샘플1(상위권) 예상 성적:' , sample_pred[0] )
print( '샘플2(하위권) 예상 성적:' , sample_pred[1] )
