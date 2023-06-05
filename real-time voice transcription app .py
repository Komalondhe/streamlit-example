import streamlit as st
import os
from google.cloud import speech
import io

# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'

# Create a client for the Google Cloud Speech-to-Text API
client = speech.SpeechClient()

# Create a Streamlit app
st.title("Real-time Voice Transcription App")

# Create a microphone button
if st.button("Start Transcription"):
    # Set up audio recording
    st.write("Listening...")
    with st.spinner():
        # Configure audio input stream
        audio_stream = st.audio(sampling_rate=44100, format="wav", channels=1)

        # Set up streaming recognition
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="en-US",
        )
        streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

        # Create a generator to continuously stream audio data to the API
        def audio_generator():
            while True:
                data = audio_stream._get_frame().astype("int16").tobytes()
                yield speech.StreamingRecognizeRequest(audio_content=data)

        # Perform streaming speech recognition
        requests = audio_generator()
        responses = client.streaming_recognize(streaming_config, requests)

        # Iterate through the API responses and display the transcriptions in real-time
        for response in responses:
            for result in response.results:
                if result.is_final:
                    st.write("Transcription:", result.alternatives[0].transcript)

# Run the Streamlit app
if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.write("Click the button to start transcription")
