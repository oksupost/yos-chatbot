import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 과천 맛집 여행 챗봇")

# 모델에 대한 내용을 작성한다-yos
st.write(
    "🐨🦘 아름다운 도시 과천의 맛집을 소개하는 챗봇입니다! 🦘🐨"
    "이 앱을 사용하기 위해서는 OpenAI API 키가 필요하며, "
    "여기에서 획득할 수 있습니다: [API 키 받기](https://platform.openai.com/account/api-keys)."
    "이 앱을 단계별로 만드는 방법은 [우리의 튜토리얼을 따라해보세요](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."  
 )

# OpenAI 클라이언트 생성
openai_api_key = st.text_input("OpenAI API Key", type="password")

# api_key 주의한다-yos
if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        
        #api_key
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
           
            # 여기에 수정한다 -yos
            # model="gpt-3.5-turbo",
            model="gpt-4o-mimi",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
