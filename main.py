# Imports
import streamlit as st
from openai import OpenAI


# Statics

# Methods
apikey = st.secrets["OPENAI_SECRET"]

client = OpenAI(api_key = apikey)

def story_ai(msg, client):
  story_response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{
        "role": 'system',
        "content": '''You are Stephen King. You will take user's prompt and generate a 100 words short story for adults age 20-30'''
    },
    {
      "role": "user",
      "content": f'{msg}'              
    }],
    max_tokens = 400,
    temperature = 1.3
  )
  
  story = story_response.choices[0].message.content
  return story

def design_ai(story, client):
  design_response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{
        "role": 'system',
        "content": '''Based on the story given, you will design a detailed image prompt for the cover image of this story. 
        The image prompt should include the theme of the story with relevant color, suitable for adults.
        The output should be within 100 characters.
        '''
    },
    {
      "role": "user",
      "content": f'{story}'              
    }],
    max_tokens = 400,
    temperature = 0.8
  )
  
  design = design_response.choices[0].message.content
  return design

def image_ai(design, client):
  cover_response = client.images.generate(
    model='dall-e-2',
    prompt = f"{design}",
    size = "256x256",
    quality = "standard",
    n=1
  )

  image_url = cover_response.data[0].url
  return image_url
  
with st.form(' '):
  st.header("**Story Generator**")
  msg = st.text_input(label = "**Some keywords to generate a story**")
  submitted = st.form_submit_button("Submit")
  if submitted:
    with st.spinner('Generating story...'):
      story = story_ai(msg, client)
      refined_prompt = design_ai(story, client)
      st.write(story)
      image_url = image_ai(refined_prompt, client)
      st.image(f'{image_url}')
      st.success('Done!')