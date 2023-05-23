import streamlit as st
import openai
from utils import define_prompt, model_request, compare_texts

st.write('# GrammarGPT')

_, psw_col2, _ = st.columns([1,2,1])
OPENAI_API_KEY = psw_col2.text_input('OpenAI API Key', type='password')

_, col2, col3, _ = st.columns(4)
model = col2.selectbox(
    'Model',
    ('gpt-3.5-turbo', 'gpt-4'))

action = col3.selectbox(
    'Action',
    ('summarize',  'rewrite', 'spellcheck'))

if action == 'rewrite':

    sub_col1, sub_col2, sub_col3, sub_col4 = st.columns(4)

    audience = sub_col1.selectbox(
        'audience',
        ('Select an option', 'general', 'knowledgeable', 'expert'))

    formality = sub_col2.selectbox(
        'formality',
        ('Select an option', 'informal', 'neutral', 'formal'))
    
    domain = sub_col3.selectbox(
        'domain',
        ('Select an option',
         'academica',
         'business',
         'general',
         'email',
         'casual',
         'creative'))

    intent = sub_col4.selectbox(
        'intent',
        ('Select an option', 'inform', 'describe', 'convince', 'tell a story'))
    
    style = st.text_input("Person's style (Steve Jobs, Yoda, García Márquez ...)", )

input_text = st.text_area('', height =350)

if st.button('Run'):
    openai.api_key = OPENAI_API_KEY
    if action == 'summarize':
        prompt = define_prompt(action, input_text)
        resumen = model_request(model, prompt)
        st.markdown(resumen)

    elif action == 'rewrite':
        text_goals = {'audience' : audience,
                      'formality' : formality,
                      'domain' : domain,
                      'intent' : intent,
                      'style': style}
        prompt = define_prompt(action, input_text, text_goals)
        new_text = model_request(model, prompt)
        st.markdown(new_text)

    elif action == 'spellcheck':
        prompt = define_prompt(action, input_text)
        spellchecked_text = model_request(model, prompt)
        styled_text = compare_texts(input_text, spellchecked_text)
        st.markdown(styled_text, unsafe_allow_html=True)