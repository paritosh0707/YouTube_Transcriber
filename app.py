import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt="""You are Yotube video summarizer for data science videos. You will be taking the transcript text
# and summarizing the entire video and providing the important summary in points. Give the detailed data sciece notes like a working professional can make best out of the video
# Please provide the summary of the text given here:  """

prompt="""You are an expert data science mentor and you have to provide the detailed notes with explanation to your students that will cover all the transcript information of the video lecture. Please provide notes in string format so that i can copy.
First provide the introdution, what the entire video lecture is about then
provide the notes with explanation of the text given here:  """

# prompt = """ Title: Comprehensive Notes on Data Science and Statistics from YouTube Video Transcript

#             Subject: Data Science and Statistics

#             Prompt:

#             As an expert in Data Science and Statistics, your task is to provide comprehensive notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate detailed notes covering the key concepts discussed in the video.

#             Your notes should:

#             Data Science:

#             Explain fundamental concepts in data science such as data collection, data cleaning, data analysis, and data visualization.
#             Discuss different techniques and algorithms used in data analysis and machine learning, including supervised and unsupervised learning methods.
#             Provide insights into real-world applications of data science in various fields like business, healthcare, finance, etc.
#             Include discussions on data ethics, privacy concerns, and best practices in handling sensitive data.
#             Statistics:

#             Outline basic statistical concepts such as measures of central tendency, variability, and probability distributions.
#             Explain hypothesis testing, confidence intervals, and regression analysis techniques.
#             Clarify the importance of statistical inference and its role in drawing conclusions from data.
#             Provide examples or case studies demonstrating the application of statistical methods in solving real-world problems.

#             Your notes should aim to offer a clear understanding of both the theoretical foundations and practical applications of data science and statistics discussed in the video. Use clear explanations, examples, and visuals where necessary to enhance comprehension.

#             Please provide the YouTube video transcript, and I'll generate the detailed notes on Data Science and Statistics accordingly.
#         """


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("?")[0].split("/")[-1]
        # video_id="EoauGRf_VCA"
        print(video_id)
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

def download_markdown(content, filename):
    """
    Function to download markdown content as a file.
    """
    # Convert content to bytes
    content_bytes = content.encode('utf-8')
    # Encode content as Base64
    b64 = base64.b64encode(content_bytes).decode()
    # Create a download link for the markdown file
    print("entered")
    # Create a download link for the markdown file
    href = f'<a href="data:text/markdown;base64,{b64}" download="{filename}">Click here to download</a>'
    # href = f'<a href="data:text/markdown;base64,{b64}" download="{filename}">Click here to download {filename}</a>'
    print("executing")
    st.markdown(f'{href}', unsafe_allow_html=True)
    # st.markdown(f'<a href="{href}" download="{filename}">Download {filename}</a>', unsafe_allow_html=True)
    print("executed")

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    # print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
summary = ""
if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        # global summary
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
if st.button("Download Markdown File"):
    # with open("result.md", "rb") as file:
    #     summary = file.read()
    download_markdown(summary, "Summary.md")
        # with open("Summary.md", "w") as md_file:
        #     md_file.write(summary)




