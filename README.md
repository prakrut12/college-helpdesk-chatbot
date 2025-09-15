🎓 College Helpdesk Chatbot 🤖

An AI-powered chatbot built using Python, Streamlit, SQLite, and Google Gemini API to assist students with timetables, faculty details, and events.
The chatbot integrates a college database with natural language processing (NLP), making it easy for students to get real-time answers to their queries.



🚀 Features

🗓 Timetable Queries – Ask about classes, subjects, and timings.

👩‍🏫 Faculty Info – Retrieve faculty names, departments, and contact details.

🎉 Events – Get details of upcoming events with date and location.

🤖 AI-Powered Responses – Uses Google Gemini API for natural, conversational answers.

📦 SQLite Database – Stores timetable, faculty, and events data.

🌐 Deployed on Streamlit Cloud for easy access.



🛠 Tech Stack

Frontend/UI: Streamlit

Backend: Python

Database: SQLite

AI/NLP: Google Gemini API

Version Control: Git & GitHub



📂 Project Structure

college-helpdesk-chatbot/
│── app.py                # Main Streamlit app
│── db_setup.py           # Script to create & populate SQLite database
│── college.db            # SQLite database file (auto-created)
│── requirements.txt      # Dependencies
│── README.md             # Documentation



⚙ Installation & Usage

1. Clone the repository
git clone https://github.com/your-username/college-helpdesk-chatbot.git
cd college-helpdesk-chatbot


2. Install dependencies
pip install -r requirements.txt


3. Set up database (run once)
python db_setup.py


4. Run the app
streamlit run app.py


🌐 Live Demo
https://college-appdesk-chatbot-mibdjq4u8lhbr4vvreph5l.streamlit.app/

