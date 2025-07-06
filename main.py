import streamlit as st
import google.generativeai as genai

# ✅ Use the API key from Streamlit secrets
genai.configure(api_key=st.secrets["api_key"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# System Prompt
system_prompts = [
    """
    You are an expert chef with years of experience creating delicious and innovative recipes.
    Based on the ingredients provided, your task is to generate a unique and mouth-watering recipe.

    Your responsibilities include:
    1. Recipe Name
    2. Ingredients List
    3. Instructions
    4. Serving Suggestions
    5. Dietary Considerations
    """
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Page Configuration
st.set_page_config(page_title="AI Recipe Generator", page_icon="🍽️", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #f5f5f5; }
    .main-header {
        text-align: center; padding: 2rem;
        background: rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 2rem;
    }
    .main-header h1 {
        color: #ff9800; font-size: 3rem; font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header h2 { color: #e0e0e0; font-size: 1.5rem; font-weight: 400; }
    .stTextArea>textarea {
        background-color: #333; color: #fff; border-radius: 10px;
        border: 1px solid #555; padding: 1rem; width: 100%;
    }
    .stButton>button {
        background: linear-gradient(to right, #ff5722, #ff9800); color: white;
        padding: 0.8rem 2rem; border-radius: 30px; border: none;
        font-weight: 600; transition: all 0.3s ease; width: 100%; margin-top: 1rem;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .recipe-output {
        background: rgba(255, 255, 255, 0.15);
        padding: 2rem; border-radius: 10px; margin-top: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    p, li { color: #e0e0e0; line-height: 2.6; }
    .disclaimer {
        font-size: 0.9rem; color: #ffcccb; font-style: italic; margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
    <div class="main-header">
        <h1>AI Recipe Generator 🍽️</h1>
        <h2>Enter the ingredients, and let the AI suggest a recipe for you!</h2>
    </div>
""", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    ingredients_input = st.text_area("Enter the ingredients you have", placeholder="E.g., chicken, garlic, tomatoes, spinach")
    submit = st.button("Generate Recipe")

with col2:
    if submit and ingredients_input:
        with st.spinner("Generating recipe..."):
            prompt = f"Given these ingredients: {ingredients_input}, create a recipe."

            try:
                response = model.generate_content({'text': prompt})

                if response:
                    st.markdown("""<div class="recipe-output"><h2 style="color: #ff9800;">Recipe Suggestions</h2>""", unsafe_allow_html=True)
                    st.write(response.text)
                    st.markdown("""<p class="disclaimer">⚠️ Disclaimer: This recipe is AI-generated. Please follow standard food safety procedures.</p></div>""", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred during recipe generation: {str(e)}")

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 1rem;
                background: rgba(255, 255, 255, 0.1); border-radius: 10px;">
        <p style="color: #e0e0e0; font-size: 0.9rem;">
            Made with ❤️ for food lovers
        </p>
    </div>
""", unsafe_allow_html=True)

# python -m streamlit run main.py 
