import streamlit as st
import openai
import os
from dotenv import load_dotenv
import requests

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit 앱 구성
st.set_page_config(page_title="맛집 블로그 글 생성기", layout="centered")

st.title("맛집 블로그 글 생성기")

# 사용자 입력 폼
with st.form("blog_form"):
    restaurant_name = st.text_input("식당 이름", placeholder="예: 홍길동네")
    location = st.text_input("위치", placeholder="예: 서울특별시 강남구")
    main_menu = st.text_input("주요 메뉴와 가격", placeholder="예: 김치찌개 8500원, 된장찌개 8000원")
    visit_date = st.date_input("방문 날짜")
    taste_evaluation = st.text_area("음식 맛에 대한 평가", placeholder="예: 음식이 매우 맛있었어요.")
    service_evaluation = st.text_area("서비스에 대한 평가", placeholder="예: 직원들이 친절했어요.")
    atmosphere_evaluation = st.text_area("분위기에 대한 평가", placeholder="예: 아늑하고 편안했어요.")
    price_evaluation = st.text_area("가격에 대한 평가", placeholder="예: 합리적인 가격이었어요.")
    recommended_menu = st.text_input("추천 메뉴", placeholder="예: 김치찌개")
    visit_tips = st.text_area("방문 팁", placeholder="예: 주차 공간이 협소하니 대중교통을 이용하세요.")
    submitted = st.form_submit_button("블로그 글 생성")
    

# 사용자 입력 처리
if submitted:
    # OpenAI 프롬프트 생성
    prompt = f"""
    당신은 한국의 네이버 블로그에서 활동하는 맛집 블로거입니다. 아래 제공된 정보를 바탕으로, 네이버 블로그 스타일에 맞춰 자연스럽고 상세한 맛집 리뷰를 작성해주세요. 글은 친근하고 생동감 있는 어조로 작성하며, 독자가 실제로 방문한 듯한 느낌을 받을 수 있도록 노력해주세요. 각 섹션은 소제목을 사용하여 구성하고, 사진이 포함될 위치를 명시해주세요.

    **제공 정보:**
    - **식당 이름:** {restaurant_name}
    - **위치:** {location}
    - **주요 메뉴와 가격:** {main_menu}
    - **방문 날짜:** {visit_date}
    - **음식 맛에 대한 평가:** {taste_evaluation}
    - **서비스에 대한 평가:** {service_evaluation}
    - **분위기에 대한 평가:** {atmosphere_evaluation}
    - **가격에 대한 평가:** {price_evaluation}
    - **추천 메뉴:** {recommended_menu}
    - **방문 팁:** {visit_tips}

    **글 구조:**
    1. **매장 정보**
       - 식당 이름, 위치, 영업시간 등의 기본 정보를 제공해주세요.
       - [매장 외부 사진 위치]

    2. **위치 및 주차**
       - 식당의 위치와 주차 가능 여부를 안내해주세요.
       - [지도 및 주차 공간 사진 위치]

    3. **외관 및 내부 인테리어**
       - 식당의 외부 모습과 내부 분위기를 상세히 묘사해주세요.
       - [매장 내부 사진 위치]

    4. **메뉴 및 가격**
       - 주요 메뉴와 가격대를 소개하고, 메뉴판 사진을 포함해주세요.
       - [메뉴판 사진 위치]

    5. **주문한 음식**
       - 직접 주문한 음식의 사진과 간단한 설명을 제공해주세요.
       - [음식 사진 위치]

    6. **맛 평가**
       - 음식의 맛과 품질에 대한 개인적인 평가를 상세히 작성해주세요.

    7. **서비스 및 직원 친절도**
       - 직원들의 서비스와 친절도에 대한 경험을 공유해주세요.

    8. **청결도 및 위생 상태**
       - 매장의 청결 상태와 위생에 대한 평가를 포함해주세요.

    9. **전반적인 분위기**
       - 식당의 전체적인 분위기와 느낌을 묘사해주세요.

    10. **재방문 의사 및 추천 여부**
        - 다시 방문할 의사가 있는지, 독자들에게 추천할 만한지에 대한 의견을 작성해주세요.

    11. **방문 팁**
        - 방문 시 유용한 팁이나 주의사항을 공유해주세요.

    12. **지도 및 위치 안내**
        - 식당의 위치를 안내하는 지도를 포함해주세요.
        - [지도 이미지 위치]

    13. **마무리 인사**
        - 독자들에게 감사 인사와 함께 다음 포스팅에 대한 예고나 기대감을 표현해주세요.
        - "읽어주셔서 감사합니다. 다중이었습니다!" 를 마지막 줄에 꼭 추가해 주세요. 
    """

    # OpenAI API 호출
    with st.spinner("블로그 글 생성 중..."):         
        try:
            response = openai.ChatCompletion.create(
                messages=[
                    {"role": "system", "content": "당신은 한국의 네이버 블로그에서 활동하는 맛집 블로거입니다."},
                    {"role": "user", "content": prompt}
                ],
                model="gpt-4",
                temperature=0.7,
                max_tokens=1024
            )
            blog_post = response.choices[0].message.content.strip()
            
            st.success("블로그 글 생성 완료!")
            st.markdown("### 생성된 블로그 글")
            st.write(blog_post)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
