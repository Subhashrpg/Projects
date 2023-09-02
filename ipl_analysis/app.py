import streamlit as st
import pandas as pd
import numpy as np
import analysis as alt
import matplotlib.pyplot as plt

st.set_page_config(layout= "wide", page_title= "ipl analysis")
st.sidebar.title("Ipl Analysis")
check_box = st.sidebar.selectbox("Select One",["batter","bowler","team"])

unique_batter = alt.batter
unique_bowler = alt.bowler

if check_box == "batter":
    st.sidebar.subheader("Batsman name")
    selected_batsman = st.sidebar.selectbox("Select Batsman",unique_batter)
    btn1 = st.sidebar.button("Batsman's Record")

    if btn1:
        st.header(f"{selected_batsman}")
        st.subheader(f"{selected_batsman}'s overall record")
        batsman_record = alt.batsman_analysis(selected_batsman)
        st.dataframe(batsman_record)

        st.subheader(f"{selected_batsman}'s record against team")
        batsman_overall = alt.batsman_overall(selected_batsman)
        st.dataframe(batsman_overall)

        
        fig,axs = plt.subplots(4,1, layout = "constrained",figsize = (8,16))
        axs[0].bar(data = batsman_overall,x = batsman_overall.index,height = "Runs")
        axs[0].set_xticklabels(batsman_overall.index,rotation = -20)
        # axs[0].set_title(f"{selected_batsman}'s runs", fontdict= {"fontsize": 18,"color": "red"})
        axs[0].set_ylabel("Total runs", fontdict= {"fontsize": 14,"color": "red"})
        axs[0].tick_params(axis= "both",which = "both", labelsize = 8)
        
        axs[1].bar(data = batsman_overall, x = batsman_overall.index,height = "average")
        axs[1].set_xticklabels(batsman_overall.index,rotation = -20)
        axs[1].set_ylabel("Average", fontdict= {"fontsize": 14,"color": "red"})
        axs[1].tick_params(axis= "both",which = "both", labelsize = 8)

        axs[2].bar(data = batsman_overall,x = batsman_overall.index,height = "strike_rate")
        axs[2].set_xticklabels(batsman_overall.index,rotation = -20)
        axs[2].set_ylabel("Strik rate", fontdict= {"fontsize": 14,"color": "red"})
        axs[2].tick_params(axis= "both",which = "both", labelsize = 8)

        axs[3].bar(data = batsman_overall,x = batsman_overall.index,height = "HS")
        axs[3].set_xticklabels(batsman_overall.index,rotation = -20)
        axs[3].set_ylabel("Highest score", fontdict= {"fontsize": 14,"color": "red"})
        axs[3].tick_params(axis= "both",which = "both", labelsize = 8)
        st.pyplot(fig)

elif check_box == "bowler":
    st.sidebar.subheader("Bowler name")
    select_bowler = st.sidebar.selectbox("Select Bowler", unique_bowler)
    btn2 = st.sidebar.button("Bowler's Record")

    if btn2:
        st.header(f"{select_bowler}")
        st.subheader(f"{select_bowler}'s overall record")
        
        