import pandas as pd
import joblib

class AptService : 

    # 생성자
    def __init__( self ) :
        self.model = joblib.load( './1112practice/apt_model.pkl' )
        self.metrics = joblib.load( './1112practice/apt_metrics.pkl' )

    # 예측함수
    def predict( self , apt ) : 
        sample = pd.DataFrame( [apt] )
        result = self.model.predict( sample )[0]
        return{ 
            'predict' : int( round( result ) ) , 
            'r2' : self.metrics['r2'] , 
            'cv_r2' : self.metrics['cv_r2'] , 
            'best_params' : self.metrics['best_params']
        }

# 서비스 객체 생성
apt_service = AptService()