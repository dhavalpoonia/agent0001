import os
import json
from groq import Groq
from dotenv import load_dotenv
import re 



load_dotenv()

groq_api_key = os.environ.get("GROK_API_KEY")
# Initialize the Groq client
client = Groq(api_key = groq_api_key)



def refine_output(output_text):
    pattern = r'<think>[\s\S]*?</think>\s*' 

    cleaned_text = re.sub(pattern, '', output_text, flags=re.DOTALL).strip()
    return cleaned_text


def get_analysis(original_text, transcript, topic):
    chat_completion = client.chat.completions.create(
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "You are a helpful articulation coach."
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": f"""You are provided with two version of text. One is original version of text which was shown to person for two minutes to read. And later that content was removed from screen and asked the person to speak about the same topic in his own language based on his own understanding. \n
                The transcript what user spoke about the topic and content based on his understanding after reading about the topic for 2 mins. This exercise is being done to analyze the current state of speaking skills of the person. What is the score of the users in different sectors of speaking skills like articulation of thoughts, Overall flow of his speech, Is he maintaining good cohesion with the reference subject or not, If not is the extra content true about the subject or is it somopletely off topic. \n
                In the output You can share the overall Summary in Three lines maximum and then give score on this speaking skills like articulation, flow awareness etc. 
                Please find the topic name, reference content and transcript of user below:
                Topic: {topic} 
                Reference Content: {original_text} 
                User Transcript: {transcript}""",
                
            }
        ],

        # The language model which will generate the completion.
        model="qwen/qwen3-32b"
    )
    print(chat_completion.choices[0].message.content)
    analysis = chat_completion.choices[0].message.content

    refined_analysis = refine_output(analysis)
    return refined_analysis

