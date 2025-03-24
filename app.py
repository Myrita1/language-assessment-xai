from assessment_criteria import create_ilr_prompt
import streamlit as st
import requests
import base64  # for encoding audio

# Hugging Face API details
HUGGINGFACE_API_TOKEN = "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"
model_name = "HuggingFaceH4/zephyr-7b-beta"

# Function to transcribe audio using Hugging Face Whisper
def transcribe_audio_from_huggingface(audio_file):
    api_url = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

    audio_bytes = audio_file.read()
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    payload = {
        "inputs": audio_b64,
        "parameters": {"task": "automatic-speech-recognition"}
    }

    response = requests.post(api_url, headers=headers, json=payload)
    result = response.json()
    return result.get("text", "Could not transcribe audio.")

# Function to get assessment feedback from Hugging Face model
def get_feedback_from_huggingface(prompt):
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 500}}

    response = requests.post(api_url, headers=headers, json=payload)
    result = response.json()

    if isinstance(result, dict) and "error" in result:
        return f"Error: {result['error']}"
    else:
        return result[0]['generated_text']

# Streamlit app UI
st.title("Language Assessment XAI Tool (Powered by Hugging Face Zephyr)")
st.write("Enter your assessment question, learner’s response, or speaking sample:")

question = st.text_input("Assessment Question:")
learner_response = st.text_area("Learner’s Written Response:", height=250)
audio_file = st.file_uploader("Upload your speaking sample (optional):", type=["wav", "mp3"])

if st.button("Assess Response"):
    # If there's audio, transcribe it and append to learner response
    if audio_file is not None:
        with st.spinner("Transcribing audio..."):
            transcription = transcribe_audio_from_huggingface(audio_file)
            learner_response += "\n\nTranscribed Speaking Sample:\n" + transcription
        st.success("Audio transcribed and added!")

    with st.spinner("Generating academic feedback from Zephyr..."):
        prompt = create_ilr_prompt(question, learner_response)
        feedback = get_feedback_from_huggingface(prompt)

    st.success("Assessment Complete!")
    st.write("### AI Assessment Feedback")
    st.markdown(feedback)
