import streamlit as st
import psycopg2
from functools import lru_cache
import openai
import time

# Connection parameters
conn_params = {
    'dbname': 'EditAssist',
    'user': 'postgres',
    'password': 'mafmafm',
    'host': 'localhost',
    'port': 1234
}

# OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Function to get data from the database
def get_data_from_db(query):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        
        # Execute the query
        cur.execute(query)
        result = cur.fetchall()
        
        # Close cursor and connection
        cur.close()
        conn.close()
        
        return result
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []
    

# Functions to get data from specific tables
def get_course_details():
    query = "SELECT * FROM CourseDetails"
    return get_data_from_db(query)

def get_modules():
    query = "SELECT * FROM modules"
    return get_data_from_db(query)

def get_instructors():
    query = "SELECT * FROM instructors"
    return get_data_from_db(query)

def get_certification():
    query = "SELECT * FROM certification"
    return get_data_from_db(query)    

@lru_cache(maxsize=32)
def get_cached_answer(question):
    return _get_answer(question)

def _get_answer(question, retry_count=0):
    # Get data from multiple tables
    course_details = get_course_details()
    modules = get_modules()
    instructors = get_instructors()
    certification = get_certification()

    # Format database data for the prompt
    formatted_course_details = "\n".join(
        [f"{row[0]}: {row[1]} - {row[2]} (Start: {row[3]}, End: {row[4]}, Price: {row[5]}, Schedule: {row[6]}, Location: {row[7]}, Hours: {row[8]}, Category: {row[9]}, Type: {row[10]})" for row in course_details]
    )
    
    formatted_modules = "\n".join(
        [f"{row[0]}: {row[2]} - {row[3]}" for row in modules]
    )
    
    formatted_instructors = "\n".join(
        [f"{row[0]}: {row[1]}, {row[2]} at {row[3]}" for row in instructors]
    )
    
    formatted_certification = "\n".join(
        [f"{row[0]}: {row[2]}" for row in certification]
    )

    # Formulate prompt for OpenAI API
    prompt = (
        f"User asked: {question}\n\n"
        f"Course Details:\n{formatted_course_details}\n\n"
        f"Modules:\n{formatted_modules}\n\n"
        f"Instructors:\n{formatted_instructors}\n\n"
        f"Certification:\n{formatted_certification}\n\n"
        "Your response:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except openai.error.RateLimitError:
        if retry_count < 5:
            wait_time = min(60 * (2 ** retry_count), 3600)
            st.warning(f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            return _get_answer(question, retry_count + 1)
        else:
            return "Sorry, we are experiencing high demand. Please try again later."
    except openai.error.OpenAIError as e:
        if "quota" in str(e).lower():
            st.error("You have exceeded your current quota. Please check your plan and billing details.")
        else:
            st.error(f"An OpenAI error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"

def get_answer(question):
    return get_cached_answer(question)

