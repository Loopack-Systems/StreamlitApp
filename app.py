import streamlit as st
import pandas as pd
import datetime
import os

# Paths to CSV files
CODES_CSV_FILE = 'codes.csv'
CUPS_CSV_FILE = 'cups.csv'

# Create CSV files if they don't exist
if not os.path.exists(CODES_CSV_FILE):
    df_codes = pd.DataFrame(columns=['code', 'timestamp'])
    df_codes.to_csv(CODES_CSV_FILE, index=False)

if not os.path.exists(CUPS_CSV_FILE):
    df_cups = pd.DataFrame(columns=['code', 'number_of_cups', 'timestamp'])
    df_cups.to_csv(CUPS_CSV_FILE, index=False)

def check_code(code, file_path):
    df = pd.read_csv(file_path)
    if code in df['code'].values:
        timestamp = df.loc[df['code'] == code, 'timestamp'].values[0]
        return True, timestamp
    return False, None

def save_code(code, file_path):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(file_path)
    df = df.append({'code': code, 'timestamp': timestamp}, ignore_index=True)
    df.to_csv(file_path, index=False)

def save_cups_data(code, number_of_cups):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(CUPS_CSV_FILE)
    df = pd.DataFrame(df)
    df = df.append({'code': code, 'number_of_cups': number_of_cups, 'timestamp': timestamp}, ignore_index=True)
    df.to_csv(CUPS_CSV_FILE, index=False)

def main():
    st.title("Loopack Registration System")
    
    # Tabs for different actions
    tab1, tab2 = st.tabs(["1st SHOT", "Receive CUPS"])

    with tab1:
        st.header("1st SHOT")
        
        # Text input for code
        user_input = st.text_input("Enter your code:", "")
        
        if st.button("Submit", key="submit_1st_shot"):
            if user_input:
                # Convert input to uppercase
                code = user_input.upper()
                
                # Add "LPU" prefix if not present
                if not code.startswith("LPU"):
                    code = "LPU" + code
                
                # Check if the code already exists
                exists, timestamp = check_code(code, CODES_CSV_FILE)
                if exists:
                    st.write(f"❌ The code '{code}' was already registered at {timestamp}.")
                else:
                    save_code(code, CODES_CSV_FILE)
                    st.write(f"✅ New code registered: '{code}' at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
        
        # Display the contents of codes.csv
        st.subheader("Registered Codes")
        df_codes = pd.read_csv(CODES_CSV_FILE)
        st.dataframe(df_codes)

    with tab2:
        st.header("Receive CUPS")
        
        # Text input for code in the "Receive CUPS" tab
        user_input = st.text_input("Enter your code to receive cups:", "", key="receive_cups")
        
        # Number input for cups
        number_of_cups = st.number_input("Enter number of cups:", min_value=1, step=1, key="num_cups")
        
        if st.button("Submit", key="submit_receive_cups"):
            if user_input:
                # Convert input to uppercase
                code = user_input.upper()
                
                # Add "LPU" prefix if not present
                if not code.startswith("LPU"):
                    code = "LPU" + code
                save_cups_data(code, number_of_cups)
                st.write(f"✅ New cups entry registered: 'User {code}' with {number_of_cups} cups at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

        # Display the contents of cups.csv
        st.subheader("Cup Transactions")
        df_cups = pd.read_csv(CUPS_CSV_FILE)
        st.dataframe(df_cups)

if __name__ == "__main__":
    main()
