import pandas as pd

def clean_dataframe(df):
    '''
    Cleans the input looker csv to have clear column names, change ratings to 
    be 1-5 instead of strings, and change "Submission Date" col into datetime object

    Input: pandas dataframe
    Output: pandas dataframe
    '''
    
    # Renaming columns
    col_names = [
        'Submission Date',
        'Cohort Start Date',
        'Online Pacing',
        'Teacher Name',
        'Cares about my success',
        'Explains concepts clearly',
        'Inspires and motivates me',
        'Is highly knowledgeable',
        'Provides feedback',
        'Sets clear expectations',
        'Strikes a balance between supporting and challenging',
        'What part of your experience could be improved?',
        'What part of your experience has been the most valuable?'
    ]
    df.columns = col_names

    # Dropping unnecessary first row
    df = df.drop(0, axis=0)

    # Changing rating columns into numbers
    rating_cols = list(col_names[4:-2])
    rating_dict = {
        "Strongly agree": 5,
        "Agree": 4,
        "Neutral": 3,
        "Disagree": 2,
        "Strongly disagree": 1
    }
    df[rating_cols] = df[rating_cols].applymap(lambda x: rating_dict[x])

    # Changing Submission Date col to be datetime object
    df["Submission Date"] = pd.to_datetime(df["Submission Date"])

    return df