# Study Notes Generator
Transform your lecture videos, PDFs, and handwritten notes into concise, exam-ready study guides.

---
# Project Description
Study Notes Generator is an AI application designed to help students efficiently prepare for exams by generating comprehensive study notes. Users can provide lecture videos (in MP4 format) and PDFs containing handwritten or course notes. The application uses locally run models (Whisper for transcription and Qwen2.5-VL for OCR) to extract text, which is then indexed in a Qdrant vector database. Leveraging retrieval-augmented generation with OpenAI's o3-mini, the system produces clear and organized study guides that highlight key topics and concepts.

---
# Features
- **Video Transcription:**  
  Locally runs Whisper to transcribe lecture videos quickly.
- **PDF OCR:**  
  Converts PDFs to images and processes them with Qwen2.5-VL to extract and summarize visual text.
- **Retrieval-Augmented Summarization:**  
  Indexes extracted text in a Qdrant vector database and uses OpenAI's o3-mini to generate study notes based on the provided course and topic.

---
# System Requirements
**Operating System:**  
- Currently supported: macOS

**Hardware:**  
- Minimum: 16 GB RAM (more is recommended)  
- M-series chip required to run local models (tested on M4; M2/M3 should also work)

**Software:**  
- Python 3.12

**API Requirements:**  
- Access to a Qdrant instance (local or cloud-hosted)  
- OpenAI API key

---
# Running the application
1. **Clone the Repository:**
```git clone https://github.com/akilgiri/Study-Notes-Generator.git```
```cd Study-Notes-Generator/macos```
2. **Install required python libraries**
```pip install -r requirements.txt```
3. **Configure environment variables**
Create a .env file in the project root with the following:
```QDRANT_URL="https://your-qdrant-instance"```
```QDRANT_API_KEY="your-qdrant-api-key"```
```OPENAI_API_KEY="your-openai-api-key"```
4. **Run the Streamlit application**
```streamlit run frontend_app.py```
5. **Input your data:**
- mp4 file path for lecture video
- pdf file path for course notes
- Folder in which you want application output
- Provide the course and the specific topic for which you want the notes generated
- Example image of filled inputs:
<img width="720" alt="Screenshot 2025-03-10 at 10 45 21 PM" src="https://github.com/user-attachments/assets/3fd7d7e0-42eb-4b20-8d8d-9cf5d8714ac3" />

6. **Generate study notes**
- Click the "Generate notes" button
- The application will take a few minutes to run and generate your notes
- The notes will be displayed on the Streamlit UI as well as saved to the specified output folder


---
# Example output:
- **Course Input:**  
  - Course: Compilers  
  - Topic: Regex to DFA

- **Video Input:**  
  - An 80-minute lecture video (approximately 5 minutes for transcription).

- **PDF Input:**  
  - 11-page course slides (approximately 2.5 minutes for OCR processing).

**Output Files:**
- ```study_notes.md``` – The final study notes generated using o3-mini.
- ```04a-regex2dfa.md``` – The summary generated from the PDF OCR by Qwen2.5-VL.
- ```uw_ece351_regex2dfa.txt``` – The transcription from the lecture video via Whisper.

All outputs can be found in the ```sample_output``` folder.

---
# Known Issues
- Qwen2.5-VL is a very demanding model hardware-wise, and due to this some pdfs don't work due to memory constraints. I am looking to implement a workaround to reduce memory usage by limiting the input image size.
- The following RuntimeError may occur when running the streamlit app, however the app work even if this occurs
 ```RuntimeError: Tried to instantiate class '__path__._path', but it does not exist! Ensure that it is registered via torch::class_```

