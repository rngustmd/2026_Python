# 지도학습 : X특성(독립)과 Y타깃(종속) 모델에 학습 하여 예측
# 비지도학습 : X특성(독립) 모델 이용하여 거리/밀도 군집/클러스터/그룹

import pandas as pd
url = "https://raw.githubusercontent.com/arunk13/MSDA-Assignments/master/IS607Fall2015/Assignment3/student-mat.csv"
df = pd.read_csv(url, sep=';')

# 공부시간 , 결석일수 , 1학기성적~3학기성적
X = df[['studytime', 'absences', 'G1', 'G2', 'G3']]

# 타깃/종속 없다. -> 비지도학습 이라서
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split # 학습 98% 검증용 2% (중요도 떨어짐)
X_train, X_test = train_test_split(X, test_size=0.02, random_state=42)

# 1) 스케일링/단위표준화 , 
from sklearn.preprocessing import StandardScaler
ss = StandardScaler( )
X_train_scaled = ss.fit_transform( X_train ) # fit + transform => fit_transform
X_test_scaled = ss.transform( X_test )

# 2) 군집 = 그룹만들기 = 클러스터 , K개의 군집을 찾는 Kmeans 모델 , k_means( n_clusters=k )
from sklearn.cluster import KMeans
model = KMeans( n_clusters=3 )
model.fit( X_train_scaled )
train_labels = model.predict( X_train_scaled )
print( '앞에서 10명 그룹 확인:' , train_labels[ : 10 ] )
# 앞에서 10명 그룹 확인: [1 0 0 1 0 2 0 2 1 2]
print( '테스트 학생: ' , model.predict( X_test_scaled ) )

# 3) 시각화 : 특성 여러개이므로 2D 시각화 한계
# 판다스 복습
# list_2 = [[2,3] , [4,5]]
# print(list_2[ : 1 ]) # [[2, 3]] # 리스트[ 시작행:끝행-1 ] 
# print(list_2[ : , 1])

import matplotlib.pyplot as plt
plt.scatter( X_train_scaled[ : , 4 ] , X_train_scaled[ : , 1 ] , c = train_labels )
plt.scatter( X_test_scaled[ : , 4 ] , X_test_scaled[ : , 1 ] , c = "red" , marker='*' )
plt.show( )

# 4) 최적의 K(군집/그룹) 수 찾기 VS 지도핟습( F1 분류 / R2 회귀 )
from sklearn.metrics import silhouette_score
sse_list= [ ]
sil_list= [ ]
for k in range( 2, 20 ) : # range( 시작값 : 끝값-1 )
    k_teamp = KMeans( n_clusters=k , random_state=42 ) # K반복마다 학습 모델생성 
    preds = k_teamp.fit_predict( X_train_scaled )  # 모델 학습/추론 동시에 , fit + predict
    sse_list.append( k_teamp.inertia_ ) # 군집 결과에 각 샘플과 중심점 거리 제곱의 합 저장 
    sil_list.append( silhouette_score( X_train_scaled , preds ) ) # 실루엣 점수를 저장 
plt.plot( range( 2, 20 ) , sse_list , marker='o' ) # 
plt.show()
plt.plot( range( 2, 20 ) , sil_list , marker='o' ) # 
plt.show()
# sse : 엘보우지점(기울기가 완만하게 꺾이는 변곡점) , 오차제곱합 
# 실루엣: 높은 값 일 수록 이상적, 응집도 와 분리도
# 두 차트 해석하여 최적의 K 해석 ,
# 최적 k 군집하기 
best_model = KMeans( n_clusters=5 )
pred =best_model.fit_predict( X_train_scaled )
print( pred[:10] ) # [3 2 2 1 0 1 2 1 1 1]

# 5) HDBSCAN # k-means 다르게 밀도 기반으로 군집 , 이상치(-1) 자동 탐지 
from sklearn.cluster import HDBSCAN
#HDBSCAN( min_cluster_size=군집하기위한최소데이터수/5, min_samples=군집판별할 때 계산되는 이웃 수 )
model = HDBSCAN( min_cluster_size=15, min_samples=5 )
pred = model.fit_predict( X_train_scaled )
print( pred ) # 군집/그룹 4개 , # 이상치 1개(-1)