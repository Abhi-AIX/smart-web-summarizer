import streamlit as st
from web_scraper import Summarize, SaveResult

st.title("Smart Web Summarizer")

password = st.text_input("Password", type="password")
if password != st.secrets["APP_PASSWORD"]:
    if password:
        st.error("Wrong password")
    st.stop()


st.write("Paste a link to get key points and a short summary.")

with st.form(key="summarize_form"):
    url = st.text_input("Enter a URL to summarize", key="url_input")
    submit = st.form_submit_button("Summarize")

if submit:
    with st.spinner("Reading and Summarizing..."):
        result = Summarize(url)
        SaveResult(url, result)

    if result.outcome == "success":
        st.subheader("Key points")
        for i, point in enumerate(result.summary.points, 1):
            st.markdown(f"{i}. {point}")
        st.divider()
        st.subheader("Summary")
        for sentence in result.summary.summary:
            st.write(sentence)
        st.caption(f"({result.seconds:.1f} seconds)")
        st.caption(f"Cost: ${result.cost:,.2f} USD")
   
        
    else:
            st.write(result.message)
       
