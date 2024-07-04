import streamlit as st
import assemblyai as aai
from download import download_video_audio
import yt_dlp
from datetime import datetime
import json
import pandas as pd

def current_time():
    return datetime.now().strftime("%H:%M:%S")

def transcribe_yt_assembly2(url):
    aai.settings.api_key =st.secrets['ASSEMBLYAI_API_KEY']
    config = aai.TranscriptionConfig(
     speaker_labels=True,
    )
    transcript = aai.Transcriber().transcribe(url, config)
    return transcript

def save_transcript_to_file(ts, file_path):
    df=pd.DataFrame(columns=["start","duration","speaker","text"])
    for t in ts:
        duration=(t.end-t.start)/1000
        df.loc[len(df)]=[t.start//1000,duration,t.speaker,t.text]
    df.to_csv(file_path,index=False)
    xxx="""
    
    with open(file_path, 'w') as f:
        for t in ts:
            duration=(t.end-t.start)/1000
            df.loc[len(df)]=[t.start//1000,duration,t.speaker,t.text]
            f.write(f"{t.start//1000},{duration},{t.speaker},{t.text}\n")
    """

youtube_link = st.text_input("Enter YouTube link:", "")
if youtube_link:
    st.write(f"{current_time()} About to fetch audio from URL {youtube_link}")
    audio_file = download_video_audio(youtube_link)
    st.write(f"{current_time()} Transcribing audio from URL {youtube_link} file: {audio_file}")
    transcript = transcribe_yt_assembly2(audio_file)
    st.write(f"{current_time()} Completed transcribing {youtube_link}")
    if transcript.status == aai.TranscriptStatus.error:
        st.write(transcript.error)
    else:
        save_transcript_to_file(transcript.utterances, audio_file+".csv")
        #st.write("# First five lines:")
        for utterance in transcript.utterances:
            duration=(utterance.end-utterance.start)/1000
            st.write(f"{utterance.start//1000} - {duration} : Speaker {utterance.speaker}: {utterance.text}")