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
        try:
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            response = model.generate_content(
                f"""You are a helpful college helpdesk assistant.

                Student asked: {user_query}.

                Step 1: Classify the query into one of these: timetable, faculty, or events.
                Step 2: Based on that category, provide a useful, short, student-friendly answer.
                Step 3: If database info is needed, ask me (the system) which category was chosen.

                Answer format:
                CATEGORY: <timetable/faculty/events>
                RESPONSE: <final answer to student>"""
            )

            raw_text = response.text.strip()
            if "CATEGORY:" in raw_text:
                lines = raw_text.splitlines()
                category_line = [l for l in lines if l.startswith("CATEGORY:")]
                response_line = [l for l in lines if l.startswith("RESPONSE:")]

                category = category_line[0].replace("CATEGORY:", "").strip().lower() if category_line else None
                answer = response_line[0].replace("RESPONSE:", "").strip() if response_line else "I’m not sure."

                if category:
                    df = fetch_data(category)
                    if df is not None and not df.empty:
                        st.subheader("📌 Relevant Info from College DB:")
                        st.dataframe(df)

                st.subheader("🤖 Chatbot Response")
                st.write(answer)

            else:
                st.error("⚠ Could not classify query properly.")

        except Exception as e:
            st.error(f"Error: {e}")
