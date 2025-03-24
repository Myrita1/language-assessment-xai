from assessment_criteria import create_ilr_prompt
import streamlit as st
import requests

HUGGINGFACE_API_TOKEN = "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"
model_name = "HuggingFaceH4/zephyr-7b-beta"

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

# Streamlit UI
st.title("Language Assessment XAI Tool (Powered by Hugging Face Zephyr)")
st.write("Enter your assessment question and learner’s response:")

question = st.text_input("Assessment Question:")
learner_response = st.text_area("Learner’s Response:", height=250)

if st.button("Assess Response"):
    with st.spinner("Generating academic feedback from Zephyr..."):
        prompt = create_ilr_prompt(question, learner_response)
        feedback = get_feedback_from_huggingface(prompt)

    st.success("Assessment Complete!")
    st.write("### AI Assessment Feedback")
    st.markdown(feedback)

