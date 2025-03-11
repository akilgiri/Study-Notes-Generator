import streamlit as st
from backend.speech2text import speech2text
from backend.parse_notes import parse_handwriting
from backend.qdrant_indexer import index2qdrant
from backend.create_notes import create_notes
import os


st.title("AI Study Notes Generator")
st.write("Provide your course notes and lecture video to get comprehensive study notes.")

lecture_video_path = st.text_input("Enter the file path to the lecture video in mp4 format")
notes_path = st.text_input("Enter the file path to the study notes in pdf format")
output_folder = st.text_input("Enter the output folder path to save the generated notes")
# print("NOTES PATH: ", notes_path)
user_query = st.text_input("Enter the course and topic to generate notes on (Example -> Course: Compilers, Topic: Regex to DFA)")

if st.button("Generate notes"):
    with st.spinner("Generating notes..."):
        try:
            if not os.path.isdir(output_folder):
                os.mkdir(output_folder)

            # Check if lecture video path is provided
            if lecture_video_path != "":
                st.info("Transcribing lecture video (this may take a while depending on the length of the video)")
                text_file_name = os.path.split(lecture_video_path)[-1].replace(".mp4", ".txt")
                text_file = os.path.join(output_folder, text_file_name)

                # For testing purposes, we will not transcribe the video if the transcribed file already exists
                if not os.path.exists(text_file):
                    speech2text(lecture_video_path, output_folder)
                    st.success("Lecture video transcribed successfully!")
                else:
                    st.success("Existing lecture video transcription found in output folder.")
            
            # Check if notes path is provided
            if notes_path != "":
                st.info("Parsing study notes (this may take a while depending on the number of pages in the notes)")
                parse_handwriting(output_folder, notes_path)
                st.success("Notes parsed successfully!")
            st.info("Indexing notes to Qdrant")
            # Index notes to Qdrant
            index2qdrant(output_folder, lecture_video_path, notes_path)
            st.success("Notes indexed to Qdrant successfully!")
            st.info("Generating study notes")
            # Run LLM chain to generate study notes
            chain = create_notes()
            response = chain.invoke(user_query)
            st.success("Generated study notes (they are also available in your output folder):")
            st.write(response)

            # Save study notes in a markdown file in the output folder
            output_path = os.path.join(output_folder, "study_notes.md")
            with open(output_path, "w") as f:
                f.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")