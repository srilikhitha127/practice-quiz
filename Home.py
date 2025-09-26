import streamlit as st
from prompt import user_goal_prompt


st.set_page_config(page_title="MCP Learning Path", page_icon="🎓", layout="wide")


st.title("🎓 MCP Learning Path")
st.caption("Main app - your prompt-driven learning path")


st.subheader("Prompt used")
st.code(user_goal_prompt, language="markdown")


st.header("Your Learning Path")
st.write("Render your generated day-wise plan and playlist links here.")


