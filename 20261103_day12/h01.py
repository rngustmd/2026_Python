# httpx 란? 외부 api 통신하는 라이브러릴 , API 연동 / SPRING API
# 설치1 : pip install httpx
# httpx 라이브러리 에는 .json() 타입변환 하지만 xml 변환 지원하지 않는다.
# xmltodict 란? xml 파싱 라이브러리
# 설치2 : pip install xmltodict

import httpx
import pandas as pd
import xmltodict

# 0] 
service_key = ""

# 1] 공공데이터포털 json 형식의 자료 요청
def test1() : 
    # 2] 신청한 API 의 주소 및 파라미터 분석 , page 현재페이지 , perPage=페이지당자료수 , serviceKey
    url = "https://api.odcloud.kr/api/15052602/v1/uddi:855807e2-fe8a-4e47-8a5a-ce1894e410d7_201909031553"
    url += "?page=1"
    url += "&perPage=147"
    url += f"&serviceKey={service_key}"

    # 3] httpx 이용하여 통신하기 , import httpx
    # httpx.HTTP메소드명( 통신할주소 )
    response = httpx.get( url )
    # print( response )

    # 4] 응답 결과 JSON 파싱
    response_json = response.json()
    # print( response_json )

    # 5] 판다스에 저장하기 , import pandas as pd
    df = pd.DataFrame( response_json['data'] ) # { "currentCount" : 10 , "data" : [실질자료] }
    df.info() # 확인
test1()

# 2]
def test2( ) : 
    # 1] 요청할 API 주소 
    url = "https://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyFullDown"
    url += f"?serviceKey={service_key}"
    url += "&pageNo=1&numOfRows=100"

    # 2] httpx 이용한 api 모형
    response = httpx.get( url )

    # 3] 요청 응답 자료를 문자열로 변환하여 파이썬 dict 형식으로 변환
    response_dict = xmltodict.parse(response.text)
    print( response_dict )

    # 4] <response> -> <body> -> <items> -> <item>
    df = pd.DataFrame( response_dict['response']['body']['items']['item'] )
    df.info()

test2()
