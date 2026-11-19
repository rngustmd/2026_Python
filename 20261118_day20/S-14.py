import pandas as pd
from sklearn.model_selection import train_test_split
url = "https://raw.githubusercontent.com/bab2min/corpus/master/sentiment/naver_shopping.txt"
df = pd.read_table(url, names=['rating', 'review'])
df = df[df['rating'] != 3]
df['label'] = (df['rating'] >= 4).astype(int)
df_sample = df.sample(n=5000, random_state=42).reset_index(drop=True)

print( df_sample.shape ) # ( 5000 , 3 )

# 1) 텍스트에서 전처리 = 정규표현식 자주 사용됨. vs 리액트 / JS 입력 유효성 검사
import re # 정규표현식 함수
cleaned_list = [ ] # 정규현식 통과한 목록
for text in df_sample[ 'review' ] : # 리뷰 들을 반복
    # re.sub( r'[표현식]' , '치환문자' , str() )
    text = re.sub( r'[^가-힣a-zA-Z0-9\s]',' ', str(text) )
    # .join( 리스트 ) : 각 리스트 항목 사이에 특정 문자 연결
    # .split( ) : 하나의 문자열 내 특정문자로 분리하여 리스트 반환
    cleaned_text = ' '.join( text.split( ) ) # '대한 민국' -> [ '대한' , '민국' ]
    cleaned_list.append( cleaned_text )
df_sample[ 'cleaned_review' ] = cleaned_list
print( df_sample.head( 3 ) ) 

# 2) 한국어 형태소 분석기 , kiwi
# 설치 : pip install kiwipiepy
from kiwipiepy import Kiwi
kiwi = Kiwi( )
for word in [ '가성비' , '내돈내산' , '총알배송' ] :
    # 3. 사전 학습에 없는 단어 추가
    # kiwi.add_user_word( '새로운 단어' , '품사키워드' )
    kiwi.add_user_word( word , 'NNG' )

# 4. 불용어 : 핵심 의미가 없는 형태소를 1차적으로 걸러내기 위해
from kiwipiepy.utils import Stopwords
kiwi_stopwords = Stopwords( )
custom_stopwords = { '그냥' , '그저' , '모른다' }

# 5. kiwi 이용한 형태소 분석 함수
def tokenize_kiwi( text ) : 
    # kiwi.tokenize( 분석할 문장 , stopwords=불용어객체 )
    tokens = kiwi.tokenize( text , stopwords= kiwi_stopwords )
    # 추출할 품사 키워드 , NNG(일반명사) , NNP(고유명사) , VV(동사) , VA(형용사) , MAG(일반부사)
    target_tags = { 'NNG' , 'NNP' , 'VV' , 'VA' , 'MAG' }
    result = [ ]
    # 토큰나이즈가 된 리스트에서 원하는 것만 필터링 / 추출
    for t in tokens : 
        # t.tag : 품사 , t.from 형태소문자열 반환
        if t.tag in target_tags and t.form not in custom_stopwords : # 내가 원하는 품사에 포함된 단어이면 
            if len( t.form ) > 1 or t.form in { '못' , '잘' } : # 일부 제외한 한단어 제외
                # 동사 와 형용사가 어간 뒤에 다 붙인다. 좋고 좋아서 좋네요 -> 좋다
                # 파이썬 삼항연산자 : 표현식 if 조건 else 거짓
                word = t.form + '다' if t.tag in { 'VV' , 'VA' } else t.form
                result.append( word )
    return result
# 첫번째 리뷰만 토큰나이즈 실행
test_word = df_sample[ 'cleaned_review' ].iloc[0]
print( test_word )
print( tokenize_kiwi( test_word ) )  
# 마감이 안좋아요...실밥도 많고 바느질도 부족한 부분이 몇군데 있네요...교환받기 귀찮아서 그냥 씁니다
# ['마감', '실밥', '바느질', '부족', '부분', '교환', '귀찮다']

X_train,X_test,Y_train,Y_test=train_test_split(
    df_sample[ 'cleaned_review' ],df_sample[ 'label' ],
    random_state=42, stratify=df_sample['label'] )

# 7. 리뷰 --> 행렬(벡터) 변환 
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer( 
    tokenizer = tokenize_kiwi , # 생략 시 공백/띄어쓰기 기준으로 분리 # 직접 만든 함수
    token_pattern=None 
)
X_train_tfidf = tfidf.fit_transform( X_train ) # 학습 -> 변환 # 학습용
X_test_tfidf = tfidf.transform( X_test ) # 테스트용
print( X_train_tfidf.shape )
print( X_test_tfidf.shape )

# ( 문제점 ) 오타 등 유사한 단어들을 분별 불가능 해서 다른 단어로 취급
# ( 해결 ) 유사도 거리 계산 ( 임베딩 / BERT )

# 8. 긍정 / 부정 : 감성분석
from sklearn.linear_model import LogisticRegression # 실무적으로 LightGBM
model = LogisticRegression( C=1.0 , max_iter=1000 , random_state=42 )
model.fit( X_train_tfidf , Y_train ) # 분류 모델 학습
print( model.score( X_train_tfidf , Y_train ) )
print( model.score( X_test_tfidf , Y_test ) )
Y_pred = model.predict( X_test_tfidf )
from sklearn.metrics import f1_score
print( 'f1 : ' , f1_score( Y_test , Y_pred ) )
print( X_train_tfidf.toarray()[0] )

# 9. 예측하기 
new_reviews = [
    "배송도 정말 빠르고 가성비 최고입니다! 재구매 의사 있어요.",
    "마감 상태가 엉망이고 실밥이 다 터져서 왔네요. 최악입니다.",
    "그냥 가격만큼 하는 것 같아요. 특별히 좋지도 나쁘지도 않음."
]
# 정규표현식
cleaned_new = [ ] 
for text in new_reviews : 
    text = re.sub( r'[^가-힣a-zA-Z0-9\s]', ' ', str(next) )
    cleaned_new.append( ' '.join(text.split() ) )
# 정규표현식 이후 토큰나이즈
new_tfidf = tfidf.transform( cleaned_new )
# 토큰나이즈 이후 모델추론
probs = model.predict_proba( new_tfidf ) # predict 추론 # predict_proba 추론 확률
# 0.6 이상이면 긍정 , 0.6 이하이면 부정 그외 중립
for i in range( len(new_reviews) ) : # 리뷰 수 만큼 반복
    pos = probs[i][1]
    if pos >= 0.6 : 
        contents = '긍정'
    elif pos <= 0.4 : 
        contents = '부정'
    else : 
        contents = '중립'
    print( f'리뷰: , {new_reviews[i]}' )
    print( f'감성분석: , {contents} , 긍정확률:{ pos } , 부정확률:{ probs[i][0] } ')
# 리뷰: , 배송도 정말 빠르고 가성비 최고입니다! 재구매 의사 있어요.
# 감성분석: , 중립 , 긍정확률:0.4302930471649006 , 부정확률:0.5697069528350994 
# 리뷰: , 마감 상태가 엉망이고 실밥이 다 터져서 왔네요. 최악입니다.
# 감성분석: , 중립 , 긍정확률:0.4302930471649006 , 부정확률:0.5697069528350994 
# 리뷰: , 그냥 가격만큼 하는 것 같아요. 특별히 좋지도 나쁘지도 않음.
# 감성분석: , 중립 , 긍정확률:0.4302930471649006 , 부정확률:0.5697069528350994 