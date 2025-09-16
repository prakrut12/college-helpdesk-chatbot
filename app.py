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

# --- Decide which table to fetch ---
def detect_category(query):
    """Ask Gemini to classify the query into: timetable, faculty, events"""
    model = genai.GenerativeModel("models/gemini-2.5-pro")
    response = model.generate_content(
        f"""Classify this student query into one category: timetable, faculty, or events.
        Query: {query}
        Answer with only one word: timetable OR faculty OR events."""
    )
    category = response.text.strip().lower()
    if category not in ["timetable", "faculty", "events"]:
        return None
    return category

# --- Database fetch ---
def fetch_data(category):
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()
    data, columns = None, None

    if category == "timetable":
        cursor.execute("SELECT day, subject, time FROM timetable")
        data = cursor.fetchall()
        columns = ["Day", "Subject", "Time"]

    elif category == "faculty":
        cursor.execute("SELECT name, department, email FROM faculty")
        data = cursor.fetchall()
        columns = ["Name", "Department", "Email"]

    elif category == "events":
        cursor.execute("SELECT event, date, location FROM events")
        data = cursor.fetchall()
        columns = ["Event", "Date", "Location"]

    conn.close()
    if data:
        df = pd.DataFrame(data, columns=columns)
        return df
    return None

# --- Main ---
if st.button("Ask"):
    if user_query.strip() == "":
        st.warning("⚠️ Please enter a question.")
    else:
        category = detect_category(user_query)

        if category is None:
            st.error("❌ Could not understand query. Please ask about timetable, faculty, or events.")
        else:
            df = fetch_data(category)

            if df is not None and not df.empty:
                st.subheader("📌 Relevant Info from College DB:")
                st.dataframe(df)

                # Ask Gemini to summarize
                try:
                    model = genai.GenerativeModel("models/gemini-2.5-pro")
                    response = model.generate_content(
                        f"""You are a helpful assistant. 
                        The student asked: {user_query}.
                        Here is the database info: {df.to_dict(orient='records')}.
                        
                        ✅ If timetable: give a short, day-wise summary like 
                        'On Monday you have Math at 9AM, Physics at 11AM...'.
                        ✅ If faculty: say which professor teaches what and how to contact them.
                        ✅ If events: summarize upcoming events with date and location.

                        Keep the answer student-friendly and short."""
                    )
                    st.subheader("🤖 Chatbot Response")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.info("No data found in the database.")
