import streamlit as st
from test_rag_function import ask_question


if "history" not in st.session_state:
    st.session_state.history = []


st.title("📦 AI Retail Demand Forecasting Copilot")

st.caption(
    "Ask inventory policy and stockout risk questions using the company knowledge base."
)


if st.button("🗑️ Clear Chat"):
    st.session_state.history = []
    st.rerun()


question = st.text_input(
    "Ask a question",
    placeholder="Example: What should I do for critical stockout risk?"
)


if st.button("Submit"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Generating answer..."):
            answer = ask_question(question)

        st.session_state.history.append(
            {
                "question": question,
                "answer": answer
            }
        )


st.markdown("---")

for item in reversed(st.session_state.history):

    st.markdown("### 👤 You")
    st.write(item["question"])

    st.markdown("### 🤖 Copilot")
    st.markdown(item["answer"])

    st.markdown("---")  