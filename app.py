import streamlit as st
import sqlite3
import pandas as pd
import google.generativeai as genai
import time

# Configure Gemini API key correctly
genai.configure(api_key=st.secrets["genai"]["AIzaSyAZ9VZde3PZSxoOYKEBj5OG8_XpZCq5lYo"])

st.title("🤖 College Helpdesk Chatbot")
st.write("Ask me about timetable, faculty, or events!")

user_query = st.text_input("Enter your question:")

# Search DB and remove duplicates
def search_database(query):
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    if "timetable" in query.lower():
        cursor.execute("SELECT DISTINCT day, subject, time FROM timetable")
        data = cursor.fetchall()
        columns = ["Day", "Subject", "Time"]
    elif "faculty" in query.lower():
        cursor.execute("SELECT DISTINCT name, department, email FROM faculty")
        data = cursor.fetchall()
        columns = ["Name", "Department", "Email"]
    elif "event" in query.lower():
        cursor.execute("SELECT DISTINCT event, date, location FROM events")
        data = cursor.fetchall()
        columns = ["Event", "Date", "Location"]
    else:
        conn.close()
        return None, None

    conn.close()
    df = pd.DataFrame(data, columns=columns)
    return df, columns

# Function to call Gemini API with retry
def call_gemini(prompt, model_name="models/gemini-1.5-flash"):
    model = genai.GenerativeModel(model_name)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):  # Quota exceeded
            st.warning("⚠ Too many requests. Waiting 15s and retrying...")
            time.sleep(15)
            try:
                response = model.generate_content(prompt)
                return response.text
            except Exception as e2:
                st.error(f"Still failing after retry: {e2}")
                return None
        else:
            st.error(f"Error: {e}")
            return None

GEN_MODEL = "models/gemini-1.5-flash"

if st.button("Ask"):
    if user_query.strip() == "":
        st.warning("⚠ Please enter a question.")
    else:
        df, columns = search_database(user_query)

        if df is not None and not df.empty:
            st.subheader("📌 Relevant Info from College DB:")
            st.dataframe(df)
        else:
            st.info("No relevant data found in the database.")

        # Create prompt
        db_info = df.to_dict(orient="records") if df is not None else []
        prompt = f"Answer the student's query using this data: {db_info}. Question: {user_query}"

        # Call Gemini API
        response_text = call_gemini(prompt, GEN_MODEL)

        if response_text:
            st.subheader("🤖 Chatbot Response")
            st.write(response_text)
