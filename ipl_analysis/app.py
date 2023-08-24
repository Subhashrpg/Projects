import streamlit as st
import pandas as pd
import pandas as pd
import analysis as alt

st.sidebar.title("Ipl Analysis")
check_box = st.sidebar.selectbox("Select One",["batter","bowler","team"])

if check_box == "batter":
    st.sidebar.subheader("Batsman name")
    selected_batsman = st.sidebar.selectbox("Select Batsman",alt.batter)
    btn1 = st.sidebar.button("View batsman record")

    if btn1:
        st.header(f"{selected_batsman}")
        st.subheader(f"{selected_batsman}'s overall record")
        batsman_record = alt.batsman_analysis(selected_batsman)
        st.dataframe(batsman_record)

        st.subheader(f"{selected_batsman}'s record against team")

