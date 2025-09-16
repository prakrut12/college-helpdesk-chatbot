import streamlit as st
import sqlite3
import pandas as pd
import os
import google.generativeai as genai

# --- Configure Gemini API key securely ---
genai.configure(api_key=os.getenv("AIzaSyAZ9VZde3PZSxoOYKEBj5OG8_XpZCq5lYo"))

st.title("🤖 College Helpdesk Chatbot")
st.write("Ask me about timetable, faculty, or events!")

user_query = st.text_input("Enter your question:")

# --- Detect which table to fetch ---
def detect_category(query):
    """Ask Gemini to classify the query into: timetable, faculty, events"""
    model = genai.GenerativeModel("models/gemini-1.5-flash")  # faster model
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
        cursor.execute("SELECT DISTINCT day, subject, time FROM timetable")
        data = cursor.fetchall()
        columns = ["Day", "Subject", "Time"]

    elif category == "faculty":
        cursor.execute("SELECT DISTINCT name, department, email FROM faculty")
        data = cursor.fetchall()
        columns = ["Name", "Department", "Email"]

    elif category == "events":
        cursor.execute("SELECT DISTINCT event, date, location FROM events")
        data = cursor.fetchall()
        columns = ["Event", "Date", "Location"]

    conn.close()
    if data:
        df = pd.DataFrame(data, columns=columns)
        return df
    return None

# --- Main chatbot flow ---
if st.button("Ask"):
    if user_query.strip() == "":
        st.warning("⚠ Please enter a question.")
    else:
        category = detect_category(user_query)

        if category is None:
            st.error("❌ Could not understand query. Please ask about timetable, faculty, or events.")
        else:
            df = fetch_data(category)

            if df is not None and not df.empty:
                st.subheader("📌 Relevant Info from College DB:")
                st.dataframe(df)

                # --- Gemini response with streaming output ---
                try:
                    model = genai.GenerativeModel("models/gemini-1.5-flash")
                    response = model.generate_content(
                        f"""You are a helpful assistant. 
                        The student asked: {user_query}.
                        Here is the database info: {df.to_dict(orient='records')}.

                        ✅ If timetable: give a short, day-wise summary.
                        ✅ If faculty: say which professor teaches what and how to contact them.
                        ✅ If events: summarize upcoming events.

                        Keep the answer student-friendly and short.""",
                        stream=True
                    )

                    st.subheader("🤖 Chatbot Response")
                    placeholder = st.empty()
                    final_text = ""

                    for chunk in response:
                        if chunk.text:
                            final_text += chunk.text
                            placeholder.markdown(final_text)  # fast streaming

                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.info("No data found in the database.")
