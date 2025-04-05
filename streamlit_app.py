import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 과천 맛집 여행 챗봇")

# 챗봇의 설명을 추가한다.
st.write(
    "🐨🦘 아름다운 도시 과천의 맛집을 소개하는 챗봇입니다! 🦘🐨"
    "이 앱을 사용하기 위해서는 OpenAI API 키가 필요하며, "
    "여기에서 획득할 수 있습니다: [API 키 받기](https://platform.openai.com/account/api-keys)."
    "이 앱을 단계별로 만드는 방법은 [우리의 튜토리얼을 따라해보세요](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# OpenAI API 키를 입력받는다.
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 채팅 메시지를 저장할 세션 상태 변수를 생성
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 채팅 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력을 받는 채팅 입력 필드 생성
    if prompt := st.chat_input("무엇을 도와드릴까요?"):
        # 현재 프롬프트 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        from openai import OpenAI
        
        client = OpenAI(api_key="your-api-key-here")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}]
        )
        print(response.choices[0].message.content)

        # 응답을 채팅에 스트리밍하고 세션 상태에 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
