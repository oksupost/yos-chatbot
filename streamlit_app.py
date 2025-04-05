import streamlit as st
from openai import OpenAI

# 타이틀 설정
st.title("💬 과천 맛집 여행 챗봇")

# 챗봇 설명 추가
st.write(
    "🐨🦘 아름다운 도시 과천의 맛집을 소개하는 챗봇입니다! 🦘🐨 "
    "이 앱을 사용하려면 OpenAI API 키가 필요합니다. 키는 [여기](https://platform.openai.com/account/api-keys)에서 받을 수 있습니다. "
    "앱 제작 과정을 단계별로 배우고 싶다면 [튜토리얼](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)을 참고하세요."
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

    # 기존 대화 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("과천 맛집에 대해 궁금한 점을 물어보세요!"):
        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API로 응답 생성
        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",  # 올바른 모델 이름 사용
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            # 응답을 스트리밍 방식으로 표시하고 저장
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
            st.write("API 키가 올바른지, 또는 네트워크 연결을 확인해주세요.")
