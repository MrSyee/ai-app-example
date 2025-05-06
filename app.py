import base64
import os

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv(".env")


# 기존 페이지 타이틀 및 설명
st.set_page_config(page_title="Report Writer Chat Agent", page_icon="🤖")
st.title("💬 보고서 작성 챗봇 애플리케이션")
st.markdown("✨ Multi Agent를 활용해 보고서를 작성합니다. 원하는 내용을 입력하세요.")
st.image("./resource/cover.jpg", use_container_width=True)


def initialize_session():
    with st.spinner("🔄 Agent 초기화 중..."):
        model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            max_tokens=16000,
        )

        # agent = create_react_agent(
        #     model,
        #     prompt=SYSTEM_PROMPT,
        # )

        st.session_state.agent = model
        st.session_state.session_initialized = True
        return True


# 세션 상태 초기화
if "session_initialized" not in st.session_state:
    st.session_state.session_initialized = True  # 세션 초기화 상태 플래그
    st.session_state.agent = None  # 에이전트 객체 저장 공간
    st.session_state.history = []  # 대화 기록 저장 리스트

    initialize_session()


def print_message():
    """채팅 기록을 화면에 출력합니다.

    사용자와 어시스턴트의 메시지를 구분하여 화면에 표시하고, 도구 호출 정보는 어시스턴트 메시지 컨테이너 내에 표시합니다.
    """
    i = 0
    while i < len(st.session_state.history):
        message = st.session_state.history[i]

        if message["role"] == "user":
            st.chat_message("user", avatar="🧑‍💻").markdown(message["content"])
            i += 1
        elif message["role"] == "assistant":
            # 어시스턴트 메시지 컨테이너 생성
            with st.chat_message("assistant", avatar="🤖"):
                # 어시스턴트 메시지 내용 표시
                st.markdown(message["content"])

                # 다음 메시지가 도구 호출 정보인지 확인
                if (
                    i + 1 < len(st.session_state.history)
                    and st.session_state.history[i + 1]["role"] == "assistant_tool"
                ):
                    # 도구 호출 정보를 동일한 컨테이너 내에 expander로 표시
                    with st.expander("🔧 도구 호출 정보", expanded=False):
                        st.markdown(st.session_state.history[i + 1]["content"])
                    i += 2  # 두 메시지를 함께 처리했으므로 2 증가
                else:
                    i += 1  # 일반 메시지만 처리했으므로 1 증가
        else:
            # assistant_tool 메시지는 위에서 처리되므로 건너뜀
            i += 1


# --- 사이드바: API 키 설정 ---
with st.sidebar:
    st.info(
        " * 이 앱은 OpenAI API를 사용하여 텍스트를 생성합니다. API 키를 입력해주세요."
        "\n\n * 기본적으로 'gpt-4o-mini' 모델을 사용합니다.."
        "\n\n * OpenAI API 키를 확인하려면 [링크](https://platform.openai.com/signup)를 확인하세요."
    )
    openai_key_input = st.text_input("OpenAI API Key", type="password")

    # 설정 적용하기 버튼을 여기로 이동
    if st.button(
        "설정 적용하기",
        key="apply_button",
        type="primary",
        use_container_width=True,
    ):
        # 적용 중 메시지 표시
        apply_status = st.empty()
        with apply_status.container():
            st.warning("🔄 변경사항을 적용하고 있습니다. 잠시만 기다려주세요...")
            progress_bar = st.progress(0)

            # 세션 초기화 준비
            st.session_state.session_initialized = False
            st.session_state.agent = None

            progress_bar.progress(30)

            os.environ["OPENAI_API_KEY"] = openai_key_input
            progress_bar.progress(60)

            success = initialize_session()
            progress_bar.progress(100)

            if success:
                st.success("✅ 새로운 설정이 적용되었습니다.")
            else:
                st.error("❌ 설정 적용에 실패하였습니다.")

# --- 대화 기록 출력 ---
print_message()

# --- 사용자 입력 및 처리 ---
user_query = st.chat_input("💬 질문을 입력하세요")
if user_query:
    if st.session_state.session_initialized:
        messages = [
            ("user", user_query),
        ]
        final_text = st.session_state.agent.invoke(messages)

        st.session_state.history.append({"role": "user", "content": user_query})
        st.session_state.history.append({"role": "assistant", "content": final_text.content})
        st.rerun()

    else:
        st.warning("⚠️ 에이전트가 초기화 되지 않았습니다. 설정을 확인해주세요.")
