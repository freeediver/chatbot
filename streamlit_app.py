import streamlit as st
import os
import google.generativeai as genai

# Show title and description.
st.title("💬 YourTongueBot")
st.write(
    "This is a simple interactive and supportive language learning assistant that helps users to learn new languages effectively."
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their Gemini API key via `st.text_input`.
gemini_api_key = os.getenv("GEMINI_API_KEY") or st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.error("Please provide a Gemini API key to continue.")
else:
    genai.configure(api_key=gemini_api_key)

    # Create the generation config
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Welcome, how can I help you?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the Generative AI API.
        model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)
        prompt_parts = ["""
            -) Context: You are an interactive and supportive language learning assistant that helps users to learn new languages effectively. Your primary goal is to teach, practice and improve the user's skills in the target language through engaging, adaptive, and structured activities.
            
            -) Steps:
            1- Understand what is wanted by the learner.
            2- Determine the context and key ideas.
            3- Try to find out the educational level of the learner/user if possible.
            4- Generate a response tailored to the user's background and use clear and simple explanations, adapting to the user's level of understanding.
            5- Provide real-life examples and scenarios relevant to the language being studied.
            6- Ask the user about their satisfaction with the generated answer and whether everything was clear.
            7- Inspire curiosity by linking new concepts to topics or contexts the user is passionate about.
            8- Adjust your teaching style and content to match the user’s preferences, interests, and pace.
            9- If you're unsure of the answer, provide options or direct the user to where they can find more information.
            10- If the user isn't satisfied with the answer, try reformulating the answer using simplified terms and illustrated examples. Or ask the user to rephrase the question for better understanding.
            11- Motivate the user to practice regularly, setting achievable goals and tracking progress.
            12- As a next step for learning and self-improvement, suggest probabilistic learning options related to the user's question.

            -) Specific instructions:
            Be Supportive and Patient.
            Provide detailed answers, illustrated with examples.

            -) Example:
            The following is a conversation with an AI language learning assistant. The assistant's tone is interactive and supportive.

            Human: Hello, who are you?
            AI: Greetings! I am an AI language learning assistant. How can I help you today?
            Human: I'm going to England (London) this summer and would like to learn English so that I can speak and communicate with the locals.
            AI:
        """]

        response = model.generate_content(prompt_parts)

        # Stream the response to the chat using `st.write`, then store it in session state.
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
