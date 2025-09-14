import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

# Create tables
cursor.execute("CREATE TABLE IF NOT EXISTS timetable(day TEXT, subject TEXT, time TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS faculty(name TEXT, department TEXT, email TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS events(event TEXT, date TEXT, location TEXT)")

# Populate timetable
timetable_entries = [
    ('Monday','AI','10:00 AM'),
    ('Monday','ML','12:00 PM'),
    ('Tuesday','Data Science','2:00 PM'),
    ('Tuesday','Networks','11:00 AM'),
    ('Wednesday','Python','9:00 AM'),
    ('Wednesday','Cybersecurity','1:00 PM'),
    ('Thursday','Database','10:30 AM'),
    ('Friday','Cloud Computing','2:00 PM')
]

cursor.executemany("INSERT INTO timetable VALUES(?,?,?)", timetable_entries)

# Populate faculty
faculty_entries = [
    ('Dr. Smith','CSE','smith@college.edu'),
    ('Dr. Johnson','ECE','johnson@college.edu'),
    ('Dr. Lee','IT','lee@college.edu'),
    ('Dr. Patel','CSE','patel@college.edu'),
    ('Dr. Kumar','ECE','kumar@college.edu'),
    ('Dr. Reddy','IT','reddy@college.edu')
]

cursor.executemany("INSERT INTO faculty VALUES(?,?,?)", faculty_entries)

# Populate events
event_entries = [
    ('Tech Fest','2025-09-20','Auditorium'),
    ('AI Workshop','2025-10-05','Lab 2'),
    ('Cultural Fest','2025-11-15','Auditorium'),
    ('Sports Meet','2025-12-01','Grounds'),
    ('Guest Lecture: Cloud Computing','2025-10-20','Auditorium')
]

cursor.executemany("INSERT INTO events VALUES(?,?,?)", event_entries)

conn.commit()
conn.close()
print("✅ Database created with expanded sample data!")
