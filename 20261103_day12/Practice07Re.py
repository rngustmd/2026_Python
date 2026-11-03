# 1. 동적페이지(씨네21 동적 페이지네이션) vs 정적페이지
# 2. 주소: https://cine21.com/movie/point
# 3. 제목, 이미지 링크, 전문가 평점 = list_with_upthumb_item
# p.title  , .img_wrap>img , .star_wrap > p.num
# 4. 클릭이벤트 : dom.click() ,  .pagination .page a

# 1] 라이브러리 호출 
import asyncio # 비동기 라이브러리
from playwright.async_api import async_playwright # 크롤링 라이브러리

# 2] 비동기 통신( 씨네21 비동기 페이지 이라서 ) 하기 위한 함수 선언 
async def 실습7() : 

    # 3] 비동기 통신 실행하고 종료 까지 브라우저(크로미움) 관리 
    async with async_playwright() as 비동기통신 : 

        # 4] 크롬과 비슷한 백그라운드 실행 가능한 브라우저 프로그램 
        브라우저 = await 비동기통신.chromium.launch( headless= False ) # False = 뷰모드 # True = 백드라운드모드 

        # 5] 브라우저에 새탭/페이지 열기 
        페이지 = await 브라우저.new_page()

        # 6] 열린페이지에 원하는 홈페이지 주소로 이동 
        await 페이지.goto( "https://cine21.com/movie/point" )
        await 페이지.wait_for_timeout( 5000 ) # 밀리초 만큼 일시정지 

        # =============================================================  #

        for i in range( 1, 4 ) :                # 1 부터 3까지 반복 

            # 7] query_selector_all( 식별자 ) : 여러개 DOM 반환 , query_selector( 식별자 ) : 한개 DOM 반환 
            페이지버튼리스트 = await 페이지.query_selector_all( '.pagination .page a')

            # 8] 반복문 이용하여 버튼 하나씩 클릭 .click()
            await 페이지버튼리스트[ i - 1 ].click()       # 0 인덱스 부터 a 마크업 클릭이벤트 
            await 페이지.wait_for_timeout( 5000 )

            # 9] 
            items = await 페이지.query_selector_all('.list_with_upthumb_item')
            
            for item in items : 
                # p.title  , .img_wrap>img , .star_wrap > p.num
                영화제목 = await item.query_selector( '.title')
                영화제목 = await 영화제목.inner_text() if 영화제목 else "제목없음" 
                이미지링크 = await item.query_selector( '.img_wrap>img')
                이미지링크 = await 이미지링크.get_attribute('src') if 이미지링크 else "이미지없음" 
                전문가평점 = await item.query_selector( '.star_wrap > p.num')
                전문가평점 = await 전문가평점.inner_text() if 전문가평점 else "전문가평점없음" 

                print( 영화제목 , 이미지링크 , 전문가평점 )

asyncio.run( 실습7() )