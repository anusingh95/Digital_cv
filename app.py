from pathlib import Path
import streamlit as st 
from PIL import Image
import re
from chatbot import cool_header, user_input, display_chat
from contact import send_email
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId  # To work with ObjectId in MongoDB
import os


from datetime import datetime
import pytz
from datetime import timedelta

import requests
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd
def get_image_from_drive(link):
    # Extract the file ID from the Google Drive link
    file_id = link.split("/")[-2]
    url = f"https://drive.google.com/uc?export=view&id={file_id}"
    response = requests.get(url)
    return response.content
connection_string = st.secrets['api']['mongo']
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)


def validate_phone_number(phone_number):
    phone_regex = r'^[6-9]\d{9}$'
    return re.match(phone_regex, phone_number)

css_file = current_dir/"styles"/ "main.css"
resume_file = current_dir/"assests"/"Anu_Kumari_CV.pdf"
profile_pic = current_dir/"assests"/"anu.jpeg"
social_logo = current_dir/"assests"

PAGE_TITLE = "Digital CV | Anu Kumari"
PAGE_ICON = ":wave:"
NAME ="Anu Kumari"
EMAIL ="anusinghpu26@gmail.com"
PROJECTS={
    "📄 Multi-Dimensional CV with AI":"https://github.com/anusingh95/Digital_cv",
    "🤖 Machine Learning: AI-Driven Customer Support Chatbots":"https://chatbot-amy.streamlit.app/",
    "🛒 Web Development Project: Online Shopping Website":"https://github.com/anusingh95/MCA-miniproject",
    "🎥 Machine Learning: AI-Powered Violence Detection through Surveillance Cameras":"Under Development",
}

st.set_page_config(page_title = PAGE_TITLE,page_icon=PAGE_ICON ,initial_sidebar_state="collapsed")


with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()),unsafe_allow_html = True)
with open(resume_file, "rb") as pdf_file:
    PDF = pdf_file.read()
profile_pic = Image.open(profile_pic)

col1, spacer, col2 = st.columns([10, 2, 8])

# Display the image in the first column with a specified width
with col1:
    st.image(profile_pic, width=400)
with col2:
    st.title(NAME)
    st.markdown('''
<div style="text-align: justify">Greetings! I'm Anu Kumari, and I'm thrilled to welcome you to my corner of the digital universe. My passion for technology knows no bounds, and I specialize in the dynamic realms of Machine Learning, Data Science, AI, and Web Development</div>
''', unsafe_allow_html=True)
    st.download_button(
        label="📄 Download Resume",
        data = PDF,
        file_name="ANU_KUMARI_CV.pdf",
        mime = "application/octet-sream"
        
    )
    
    subcol1, subcol2 = st.columns([0.12, 1])
    subcol1.write("📨")
    subcol2.write(f"{EMAIL}")
SOCIAL_MEDIA = {
    "LinkedIN": "https://www.linkedin.com/in/anu-singh-in/",
    "GitHub": "https://github.com/anusingh95",
}

# Define platform images
platform_images = {
    "LinkedIN": "linkedin.png",
    "GitHub": "github.png",
}

# Create columns for each social media platform
col0, col1,col2,col3,col4=st.columns(5)
cols = [col0,col1,col2,col3,col4]
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    # Display the image with a width of 24
    image_path = f"{social_logo}/{platform_images[platform]}"
    img = Image.open(image_path)
    with cols[2*index+1]:
        subcol1, subcol2 = st.columns([0.3, 1])
        subcol1.image(img, width=24, use_column_width=False)
        subcol2.write(f"[{platform}]({link})")
        hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''
        st.markdown(hide_img_fs, unsafe_allow_html=True)

listtabs = ["About Me", "Ask Anything", "Contact", "Leave Your Review", "My Blog"]
whitespace = 13
tabs = st.tabs([s.center(whitespace,"\u2001") for s in listtabs])



with tabs[0]:
    st.write('#')
    st.subheader("About Me")
    st.markdown('''
<div style="text-align: justify">
    I am an aspiring computer scientist with strong skills in C++, Java,Python, Web development, and applied machine learning. I have demonstrated the ability to create data-driven solutions using statistical modeling and algorithmic optimization techniques. I am passionate about innovation and learning new technologies. I am seeking a challenging role in a forward-thinking organization where I can contribute my expertise, collaborate on impactful projects, and push the technological boundaries.
</div>
''', unsafe_allow_html=True)
    st.markdown("""<font color=red>*If you want to learn more about me, just hop over to the "Ask Anything" tab. My AI assistant will provide you all the details about me and my career projects.*</font>""", unsafe_allow_html=True)
    st.write("---")
    
    st.subheader("Experience & Qualifications")
    st.write("""
            - 🎓 Pursuing a Master's degree in Computer Science from Pondicherry University, expected to graduate in May 2024        
            - 🎓 Earned a Bachelor's degree in Bachelor of Computer Application from Deen Dayal Upadhyaya University Gorakhpur(UP) in August 2021
            - 🔎 Strong problem-solving and analytical skills
            - 💬 Good communication and teamwork skills
            """)
    st.write("---")
    st.subheader("Skills")
    st.write(
    '''
    - 👩🏻‍💻 Programming: C++, Java, React.js, HTML, CSS, javaScrit
    - 🐍 Python Programming: Numpy, Pandas, sklearn, Pytorch, Keras, Streamlit, Seaborn, Mathplotlib, tensorflow, nltk, Plotly, Faiss, langchain
    - 🧠 Machine Learning: Decision Tree, Neural Networks, Clustering, Classification, Deep Learning
    - 🐧 Linux: Linux System Administration,C/C++/Java/Python coding debugging in terminal
    - 💾 Databases: MongoDB, MySql
    
    '''
    )
    st.write("---")
    st.write("---")
    st.subheader("Projects & Accomplishments")
    for project, link in PROJECTS.items():
      st.write(f"- [{project}]({link})")
    
    st.write("---")

with tabs[1]:
    cool_header()
    user_question = st.text_input("Enter you question here")
    chats = st.session_state.get('chats', [])
    
    if st.button("Ask", key="ask_button"):
        with st.spinner("Amy is thinking..."):
            if user_question:
                chats = user_input(user_question, chats)
                st.session_state['chats'] = chats
                user_question = ""  # Clear input field after asking
                
    display_chat(chats)
                
    display_chat(chats)
with tabs[2]:
    st.title("Email Form")

    # Input fields
    name = st.text_input("Your Name:")
    subject = st.text_input("Subject:")
    message = st.text_area("Message:")
    email_address = st.text_input("Your Email Address:")

    # Optional fields
    phone_number = st.text_input("Phone Number (Optional):")
    # uploaded_files = st.file_uploader("Upload up to 5 files (max 20MB each, Optional):", accept_multiple_files=True)

    # # Check if more than 5 files are uploaded or if any file exceeds 20MB
    # if uploaded_files:
    #     total_size = sum(f.size for f in uploaded_files)
    #     if len(uploaded_files) > 5 or total_size > 20 * 1024 * 1024:
    #         st.error("Please upload a maximum of 5 files, each less than 20MB.")
    #         return

    if st.button("Send Email"):
        if not email_address:
            st.error("Please fill in the required field 'Your Email Address'.")
        elif not subject or not message or not name:
            st.error("Please fill in all required fields (Name, Email Address, Subject, and Message).")
        else:
            # Process the files
            # file_contents = [file.read() for file in uploaded_files] if uploaded_files else []

            # Combine email address, phone number, and message into a single string
            combined_info = f"""{'Email Address: ' + email_address if email_address else 'Email not given'}
{'Phone Number: ' + phone_number if phone_number else 'Number not given'}

{message}"""

            # Call send_email function
            send_email( combined_info, subject, name)
            st.success("Email sent successfully!")
    
with tabs[3]:
    

    # Create a connection to MongoDB
    client = MongoClient(connection_string)

    # Specify the database and collection
    db = client.review  # Database name
    collection = db.site_review  # Collection name

    st.title("Leave your Review")

    # User's Name
    name = st.text_input("Your Name:", "Enter Name")

    # User's Review Message
    review = st.text_area("Your Review:", "Share your thoughts about the product.")

    # Select the star rating using a slider (from 1 to 5)
    star_count = st.slider("Select Star Rating:", min_value=1, max_value=5, value=3)

    # Display the stars dynamically
    star_symbols = ["⭐" for _ in range(star_count)]
    empty_stars = ["☆" for _ in range(5 - star_count)]
    displayed_stars = "".join(star_symbols + empty_stars)
    st.write("Your Star Rating ")
    st.write(displayed_stars)

    # Get the current date and time in IST
    os.environ['TZ'] = 'Asia/Kolkata'
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(ist)

    # Format the date and time in a readable format with AM/PM
    formatted_time = current_time.strftime("%Y-%m-%d %I:%M:%S %p %Z")  # %I for 12-hour clock and %p for AM/PM

    # When the "Submit" button is clicked, insert data into MongoDB
    if st.button("Submit"):
        review_data = {
            "name": name,
            "review": review,
            "rating": star_count,
            "submitted_at": current_time,  # Save the original datetime object
        }
        collection.insert_one(review_data)

        st.success("Thank you for your review!")
        st.write("Review submitted:")
        st.write(f"Name: {name}")
        st.write(f"Review: {review}")
        st.write(f"Rating: {star_count} out of 5 stars")
        st.write(f"Submitted on: {formatted_time}")

    # Display all reviews
    st.header("All Reviews")

    # Retrieve all reviews from the collection
    with st.spinner("Loading reviews..."):
        # Retrieve all reviews from the collection
        all_reviews = list(collection.find({}))

    # Display the reviews in a cool format below the submit button
    with st.expander("Reviews"):
        for review in all_reviews:
            st.subheader(f"{review['name']}")
            st.write(f"Rating: {'⭐' * review['rating']}")
            st.write(f"Review: {review['review']}")
            if 'submitted_at' in review:
                submitted_time = review['submitted_at'] + timedelta(hours=5, minutes=30)  # Add 5 hours and 30 minutes        
                st.write(f"Submitted on: {submitted_time.strftime('%Y-%m-%d %I:%M %p %Z')}")
            st.write("----")
with tabs[4]:
    client = MongoClient(connection_string)
    blog_db = client.blog
    blog_collection = blog_db.site_blog

    # Fetch blogs from the MongoDB collection
    blogs = blog_collection.find().sort("created_at", -1)  # Sort by creation date, latest first

    # Display each blog
    for blog in blogs:
        col1, col2 = st.columns(2)
        with col1:st.header(blog["header"])  # Display header in bold and big
        with col2: st.image(get_image_from_drive(blog["image_link"]),width=300)  # Display image
        submitted_time = blog['created_at'] + timedelta(hours=5, minutes=30)  # Add 5 hours and 30 minutes        
        st.write(f"Created on: {submitted_time.strftime('%Y-%m-%d %I:%M %p %Z')}")
        with st.expander("Show article"):
            st.write("Article:")
            st.write(blog["body"])  # Display the body as an article

            # Display like count
            if "like_count" not in blog:
                blog["like_count"] = 0

            # Like button
            if st.button(f"Like ({blog['like_count']})", key=str(blog["_id"]) + "_like"):
                blog_collection.update_one(
                    {"_id": blog["_id"]},
                    {"$inc": {"like_count": 1}},
                )
                st.rerun()  # Rerun to update the like count in the UI

            # Display comments
            st.write("Comments:")
        with st.expander("All comments"):
            if "comments" not in blog:
                blog["comments"] = []

            # Show existing comments
            for comment in blog["comments"]:
                st.write(f"- {comment['comment']} (by {comment['author']})")

            # Input for adding a comment
            comment_text = st.text_area(f"Add a comment:", key=str(blog["_id"]) + "_comment")
            name = st.text_input("Enter name:")

            # Button to add comment
            if st.button("Submit Comment", key=str(blog["_id"]) + "_submit_comment"):
                new_comment = {
                                "_id": ObjectId(),  # Generate a unique identifier for the comment
                                "comment": comment_text,
                                "author": name,
                                "timestamp": datetime.datetime.now(),
                            }
                blog_collection.update_one(
                    {"_id": blog["_id"]},
                    {"$push": {"comments": new_comment}},
                )
                st.rerun()  # Rerun to update the comments in the UI
        st.write("----")
