import streamlit as st
from openai import OpenAI

# 이미지 추가 (URL 사용)
st.image(
    
    "https://github.com/oksupost/yos-chatbot/blob/main/cafe.jpg?raw=true",
    caption="맛있는 브런치 카페 메뉴를 추천받아보세요!",
    use_column_width=True
)

# 타이틀 설정
st.title("🍳 브런치 카페 메뉴 추천 챗봇")

# 챗봇 설명 추가
st.write(
    "🥐☕ 브런치 카페에서 당신의 취향에 맞는 메뉴를 추천해 드립니다! "
    "선호하는 맛과 식이 제한을 알려주시면 최적의 메뉴를 찾아드려요. "
    "이 앱을 사용하려면 OpenAI API 키가 필요합니다. 키는 [여기](https://platform.openai.com/account/api-keys)에서 받을 수 있습니다."
)

# OpenAI API 키 입력 필드
openai_api_key = st.text_input("OpenAI API Key", type="password")

# API 키가 없는 경우 안내 메시지
if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태에 메시지 저장소 생성 (대화 내역 유지)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 맛 선호도 및 식이 제한 입력 UI 추가
    flavor = st.selectbox("선호하는 맛을 선택하세요:", ["달콤한", "쌉쌀한", "고소한", "상큼한", "기본"])
    dietary = st.multiselect("식이 제한이 있나요?", ["비건", "글루텐 프리", "유당 프리", "없음"])

    # 기존 대화 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("추가로 원하는 점이 있으면 말씀해주세요 (예: '가벼운 메뉴 추천해줘')"):
        # 사용자 입력과 선택된 옵션 결합
        full_prompt = f"나는 {flavor} 맛을 좋아하고, 식이 제한은 {dietary}이야. {prompt}"

        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": full_prompt})
        with st.chat_message("user"):
            st.markdown(full_prompt)

        # OpenAI API로 응답 생성 (메뉴 추천 로직 포함)
        try:
            # 시스템 메시지로 메뉴 추천 가이드라인 제공
            system_message = {
                "role": "system",
                "content": (
                    "당신은 브런치 카페 메뉴 추천 챗봇입니다. 다음 메뉴 중에서 사용자의 선호도와 식이 제한에 맞는 메뉴를 추천하세요:\n"
                    "- 팬케이크 (달콤한, 유당 포함)\n"
                    "- 아보카도 토스트 (고소한, 비건 가능)\n"
                    "- 스크램블 에그 (기본, 글루텐 프리)\n"
                    "- 레몬 타르트 (상큼한, 글루텐 포함)\n"
                    "- 에스프레소 (쌉쌀한, 비건, 글루텐 프리)\n"
                    "추가 요청이 있다면 반영해서 추천해 주세요."
                )
            }

            # 대화 메시지에 시스템 메시지 추가
            messages = [system_message] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True,
            )

            # 응답을 스트리밍 방식으로 표시하고 저장
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
            st.write("API 키가 올바른지, 또는 네트워크 연결을 확인해주세요.")
