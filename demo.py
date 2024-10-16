import streamlit as st
from langdetect import detect
from langchain.llms import Cohere
import os 
import langcodes
import cohere
from langchain_core.messages import AIMessage, HumanMessage




co = "fA27Eq8tBBJ6JqdI4wT1jYitJneVYylSrQiVzVBB"

llm = Cohere(model='summarize-xlarge', temperature=0.1, max_tokens=1000)

def find_language(text, target_lang):
    source_lang = detect(text)
    detected_language_full = langcodes.get(source_lang).language_name()
    return detected_language_full 

def translate_text(detected_language, text, target_lang):
    # source_lang = detect(text)
    # return source_lang  
    # summary_prompt = (
    #                     f"The following text is in {detected_language}. "
    #                     f"Summarize it by translating it in {target_lang} perfectly. "
    #                     f"Here is the text:\n\n"
    #                     f"{text}"
    #                 )

    summary_prompt = (
                        f"The following text is in {detected_language}. "
                        f"Summarize it by translating it in English the following instructions strictly. "
                        # f"The summary should be {length_instruction}, "
                        # f"Ensure the summary maintains a {extractiveness_option} level of closeness to the original text. "
                        # f"Present it in {format_option} format. "
                        f"Do not use any information beyond what is provided in the text. Display only the summary. we don't need the translation"
                        f"Here is the text:\n\n"
                        f"{text}"
                    )

    # response = co.generate(
    # model='command-r-plus', 
    # prompt=summary_prompt,
    # temperature=0.2,
    # max_tokens=300
    # )

    # response = llm([HumanMessage(content=summary_prompt)])
    # result = response.content

    response = llm.generate([summary_prompt])  
    result = response.generations[0][0].text

    return result

st.title("Real time Translation")

input_text = st.text_area("Enter text to translate:", value="", height=150)

col1, col2 = st.columns(2)

detected_language = ""
if input_text:
    detected_language = find_language(input_text, target_lang=None) 
  

with col1:
    st.text_input("Detected Language", value=detected_language if detected_language else 'N/A')

with col2:
    target_lang = st.selectbox("Select Target Language", ["English", "Spanish", "French", "German", "Chinese"] , index = 0)

output_text = ""

if input_text:
    output_text = translate_text(detected_language , input_text, target_lang)
    print((output_text))
st.text_area("Translation Output:", value=output_text, height=150)
