import streamlit as st
import sqlite3
import pandas as pd
import os
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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

# Gemini model
GEN_MODEL = "models/gemini-2.5-pro"

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
        
        # Generate AI response using Gemini
        try:
            model = genai.GenerativeModel(GEN_MODEL)
            response = model.generate_content(
                f"Answer the student query using this data: {df.to_dict(orient='records')}. Question: {user_query}"
            )
            st.subheader("🤖 Chatbot Response")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
