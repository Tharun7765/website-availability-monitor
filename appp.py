import streamlit as st

from monitor import check_website


st.set_page_config(
    page_title="Website Availability Monitor",
    page_icon="🌐"
)

st.title("Website Availability Monitor")
st.write("Check the availability and response time of a website.")

url = st.text_input(
    "Website URL",
    placeholder="https://example.com"
)

if st.button("Check Website"):
    if not url:
        st.warning("Please enter a website URL.")
    else:
        with st.spinner("Checking website..."):
            result = check_website(url)

        st.subheader("Result")

        st.write(f"**Website:** {result['url']}")
        st.write(f"**Status:** {result['status']}")

        if "status_code" in result:
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "HTTP Status",
                    result["status_code"]
                )

            with col2:
                st.metric(
                    "Response Time",
                    f"{result['response_time']:.2f}s"
                )
