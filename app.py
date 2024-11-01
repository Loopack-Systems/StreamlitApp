import streamlit as st
import pandas as pd
import datetime
import os

# Path to CSV file
CSV_FILE = 'codes.csv'

# Create CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['code', 'timestamp'])
    df.to_csv(CSV_FILE, index=False)

def check_code(code):
    df = pd.read_csv(CSV_FILE)
    if code in df['code'].values:
        timestamp = df.loc[df['code'] == code, 'timestamp'].values[0]
        return True, timestamp
    return False, None

def save_code(code):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(CSV_FILE)
    df = df.append({'code': code, 'timestamp': timestamp}, ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def main():
    st.title("Code Registration")

    # Text input for the user code
    user_input = st.text_input("Enter your code:", "")
    
    if st.button("Submit"):
        if user_input:
            # Convert input to uppercase
            code = user_input.upper()
            
            # Add "LPU" prefix if not present
            if not code.startswith("LPU"):
                code = "LPU" + code
            
            exists, timestamp = check_code(code)
            if exists:
                st.write(f"❌ The code '{code}' was already registered at {timestamp}.")
            else:
                save_code(code)
                st.write(f"✅ New code registered: '{code}' at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

    # Display the contents of the CSV file
    st.subheader("Registered Codes")
    df = pd.read_csv(CSV_FILE)
    st.dataframe(df)

if __name__ == "__main__":
    main()
