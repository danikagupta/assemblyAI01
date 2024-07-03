import streamlit as st
import assemblyai as aai
from download import download_video_audio
import yt_dlp
from datetime import datetime
import json

def current_time():
    return datetime.now().strftime("%H:%M:%S")

def transcribe_yt_assemblyAI(url):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)

    for format in info["formats"][::-1]:
        if format["resolution"] == "audio only" and format["ext"] == "m4a":
            new_url = format["url"]
            break

    transcriber = aai.Transcriber()
    st.write(f"About to fetch audio from URL {new_url}")
    transcript = transcriber.transcribe(new_url)
    return transcript

def transcribe_yt_assembly2(url):
    config = aai.TranscriptionConfig(
     speaker_labels=True,
    )
    transcript = aai.Transcriber().transcribe(url, config)
    return transcript

def save_transcript_to_file(ts, file_path):
    with open(file_path, 'w') as f:
        for t in ts:
            f.write(f"{t.speaker}: {t.text}\n")

youtube_link = st.text_input("Enter YouTube link:", "")
if youtube_link:
    st.write(f"{current_time()} About to fetch audio from URL {youtube_link}")
    audio_file = download_video_audio(youtube_link)
    st.write(f"{current_time()} Transcribing audio from URL {youtube_link} file: {audio_file}")
    #transcriber = aai.Transcriber()
    #transcript = transcriber.transcribe(audio_file)
    transcript = transcribe_yt_assembly2(audio_file)
    st.write(f"{current_time()} Completed transcribing {youtube_link}")
    if transcript.status == aai.TranscriptStatus.error:
        st.write(transcript.error)
    else:
        save_transcript_to_file(transcript.utterances, audio_file+".json")
        for utterance in transcript.utterances:
            st.write(f"Speaker {utterance.speaker}: {utterance.text}")