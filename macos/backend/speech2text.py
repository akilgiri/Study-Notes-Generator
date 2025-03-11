import mlx_whisper
import os
from openai import OpenAI

def speech2text(speech_file, output_folder):
    # Run whisper transcription
    print("Starting whisper transcription!")
    result = mlx_whisper.transcribe(speech_file, path_or_hf_repo="mlx-community/whisper-turbo")

    # print(result["text"])

    text_file_name = os.path.split(speech_file)[-1].replace(".mp4", ".txt")
    text_file = os.path.join(output_folder, text_file_name)
    
    # Write the video transcript to a text file in the output folder
    print("Writing result to text file!")
    with open(text_file, "w") as f:
        f.write(result["text"])


# Attempting to use OpenAI API for speech to text
# def speech2text2(speech_file, output_folder):

#     client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#     audio_file = open(speech_file, "rb")
#     try:
#         transcription = client.audio.transcriptions.create(
#             model="whisper-1",
#             file=audio_file
#         )
#         text_file_name = os.path.split(speech_file)[-1].replace(".mp4", ".txt")
#         text_file = os.path.join(output_folder, text_file_name)
    
#         print("Writing result to text file!")
#         print(transcription.text)
#         with open(text_file, "w") as f:
#             f.write(transcription.text)
#     except Exception as e:
#         print(f"An error occurred: {e}")


