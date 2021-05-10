import pandas as pd
import streamlit as st
import utils as ut

st.title("Explore Your Feedback!")

file = st.file_uploader(label='Upload your Looker feedback csv here to get started:', type='csv')

if file is not None:
    df = pd.read_csv(file)

    if len(df.columns) != 13:
        st.warning(f"Expected 13 columns, received a file with {len(df.columns)} columns instead.")
        st.stop()
        
    df = ut.clean_dataframe(df)

    display = st.radio("How would you like to display the data?",
                       ["By Cohort", "By Pacing", "By Timeframe"])

    if display == "By Cohort":
        cohort_options = df['Cohort Start Date'].unique()
        cohort = st.selectbox("Which cohort?", options=cohort_options)

        subset = df.loc[df['Cohort Start Date'] == cohort]

    elif display == "By Pacing":
        pacing_options = df['Online Pacing'].unique()
        pacing = st.selectbox("Which pacing?", options=pacing_options)

        subset = df.loc[df['Online Pacing'] == pacing]

    elif display == "By Timeframe":
        min_date = df['Submission Date'].min().date()
        max_date = df['Submission Date'].max().date()
        start, end = st.date_input("Which dates?", 
                                   value=[min_date, max_date],
                                   min_value=min_date,
                                   max_value=max_date)

        subset = df.loc[(df['Submission Date'].dt.date >= start) & (df['Submission Date'].dt.date <= end)]

    else:
        subset = df.copy()

    st.write(f"### Number of responses: {len(subset)}")

    rating_cols = list(subset.columns[4:-2])

    text_col1, text_col2 = st.beta_columns(2)

    for ind, col in enumerate(rating_cols):
        if ind % 2 == 0:
            text_col1.write(f"### {col}")
            text_col1.write(f"Average value: {subset[col].mean():.4f}")
            text_col1.write(f"Range: {subset[col].min():.4f} - {subset[col].max():.4f}")
        else: 
            text_col2.write(f"### {col}")
            text_col2.write(f"Average value: {subset[col].mean():.4f}")
            text_col2.write(f"Range: {subset[col].min():.4f} - {subset[col].max():.4f}")

    st.write("## Random Sample of Written Feedback:")

    written_cols = list(subset.columns[-2:])

    sample1 = subset[subset[written_cols[0]].isna() == False].sample()
    sample2 = subset[subset[written_cols[1]].isna() == False].sample()

    if st.button('Refresh'):
        sample1 = subset[subset[written_cols[0]].isna() == False].sample()
        sample2 = subset[subset[written_cols[1]].isna() == False].sample()

    st.write("### What part of your experience could be improved?")
    st.write(f"{sample1[written_cols[0]].values[0]}")

    st.write("### What part of your experience has been the most valuable?")
    st.write(f"{sample2[written_cols[1]].values[0]}")
