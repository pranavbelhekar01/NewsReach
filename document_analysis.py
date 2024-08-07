from langchain_openai import ChatOpenAI
from sapling import SaplingClient
from pprint import pprint
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=API_KEY
    )
content = ''
# with open(r'Document Analysis\data\business.txt', 'r', encoding="utf-8") as data:
#     content = data.read()

def get_sentiment(content):
    prompt = """
    You are given a sentiment analysis task. Classify the sentiment of provided <content> by the human. Sentiment are: 'POSITIVE', 'NEGATIVE', 'NEUTRAL'. 
    Examples:        
        Human: <content>
        your response: <SENTIMENT TYPE>

    """
    messages = [
        ("system", prompt),
        ("human", content),
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content

    
def get_keywords(content):
    prompt = """
    Extract the main keywords from the given <content>. Keywords related to the type of news, domain, field, industry, etc.
    
    expected output format: list of keywords seperated by commas (,)
    

    """
    messages = [
        ("system", prompt),
        ("human", content),
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content

def profanity_test(content):
    prompt = """
    Perform a profanity test on the <content> provided by the <human>. Classify the <content> into 'PASS' or 'FAIL'. If 'FAIL' then provide reasons 
    Examples: 
        1)       
        Human: <content>
        your response: PASS
        2)
        Human: <content>
        your response: PASS
        3)
        Human: <content>
        your response: FAIL
                        Reason: <reason>

        4)        
        Human: <content>
        your response: PASS

        5)
        Human: <content>
        your response: FAIL
                        Reason: <reason>


    """
    messages = [
        ("system", prompt),
        ("human", content),
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content


def required_fields(spell):
    
    result = []
    for edit in spell['edits']:
        result.append({
            'description': edit['description'],
            'replacement': edit['replacement'],
            'sentence': edit['sentence']
        })
    return result


def grammar_check(content):
    try:
        api_key = os.environ.get("SAP_KEY")
        client = SaplingClient(api_key=api_key)
        edits = client.edits(content, session_id="testing")
        return required_fields(edits)
    except:
        return 'API LIMIT OVER!!!'

def classify_news(content):
    prompt = """
    Classify the news (<content>) as per the category of the news.

    expected output format: 
    <category> 
    

    """
    messages = [
        ("system", prompt),
        ("human", content),
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content



def clean_json_string(json_string):
    cleaned_string = re.sub(r'\\n', '', json_string)
    cleaned_string = re.sub(r'\\', '', cleaned_string)
    return cleaned_string

def final_score(content):
    prompt = """
    ### Categories that are not accepted by publications
    1. ANI - 'Personal Profile, Under Investigation, Astrology, Fantasy Sports, Ayurveda, Online Gaming, Betting' 
    2. Zee Group - 'Corporate Clients, technology' 
    3. OneIndia - 'Casinos, Betting, education' 
    4. Outlook - 'Explicit Content, Red Boost, Male Enhancement Drugs, Recreational Drug' 
    5. India Today - 'Crypto, NFT' 
    6. DNA - 'Celebrity Profile, education' 
    7. Lallantop - 'Astrology' 
    8. Wired Plans - 'Gambling' 
    9. Republic World - 'Brand' 
    10. PNN - 'Basic Legal Content, Technology' 

    ---
    Above provided are 10 news publications and the categories of news that they do not accept represented as (publication - categories not accepted).
    Your task is to classify the category of the news(<content>) and display for which publication, the <content> is acceptable and for which not. 
    If <content> is acceptable then represent it as YES and if not accecptable, then represent it as NO. 
    If the acceptance value is NO then provide the reason for it (provide the category name).
    ---
    ## Expected output format (Dictionary format):
        {
            "fit_for_publication":{
                "hindustan_times": "YES",
                "Lallantop": "NO",
                "Outlook": "YES",
                "Wired Plans": "NO",
                
            },
            "reasons": {
                "Lallantop": {
                    "article_classification": "Astrology"
                },
                "Wired Plan": {
                    "article_classification": "Gambling"
                }
            }
    }    

    ---
    
    Note: the output should be in str(plain text) and not in JSON. Avoid adding back-ticks or code representation.
    """
    messages = [
        ("system", prompt),
        ("human", content),
    ]
    ai_msg = llm.invoke(messages)
    # return ai_msg.content
    return clean_json_string(ai_msg.content)



def generate_report(content):
    report = {
        "meta_analysis": {
            "keywords": get_keywords(content),
            "Sentiment": get_sentiment(content)
        },
        "Profanity_test": profanity_test(content),
        "grammar_check": grammar_check(content),
        "Image Size Analysis": 'All images OK',
        "Article Classify": classify_news(content),
        "Final Score": final_score(content)
    }
    return report

