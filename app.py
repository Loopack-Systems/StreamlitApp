import streamlit as st
import pandas as pd
import cv2
import datetime
import os
import numpy as np

# Path to CSV file
CSV_FILE = 'scanned_codes.csv'

image = st.camera_input("Show QR code")



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

def scan_qr_code():
    """Function to scan QR code using webcam."""
    cap = cv2.VideoCapture(0)
    qr_detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Error: Could not read from webcam.")
            break
        
        # Detect QR code
        data, bbox, _ = qr_detector(frame)

        # Draw the bounding box around the detected QR code
        if bbox is not None:
            for i in range(len(bbox)):
                cv2.line(frame, tuple(bbox[i][0]), tuple(bbox[(i+1) % 4][0]), (0, 255, 0), 3)
        
        # Display the image in the Streamlit app
        st.image(frame, channels='BGR', use_column_width=True)
        
        if data:
            cap.release()
            cv2.destroyAllWindows()
            return data

        if st.button("Stop Scanning"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

def main():
    st.title("QR Code Registration")

    if st.button("Scan QR Code"):
        if image is not None:
            bytes_data = image.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

            detector = cv2.QRCodeDetector()

            data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

            st.write("Here!")
            st.write(data)

if __name__ == "__main__":
    main()
