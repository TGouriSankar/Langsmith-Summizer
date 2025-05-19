from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.base import Chain

import os
from dotenv import load_dotenv; load_dotenv()

os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"]=os.getenv("LANGSMITH_PROJECT")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGSMITH_TRACING"]=os.getenv("LANGSMITH_TRACING")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Given a context and question, provide a concise summary in 1–2 sentences."),
        ("user", "Question: {question}\nContext: {context}")
    ]
)
output_parser = StrOutputParser()
llm = ChatGroq(model="qwen-qwq-32b", max_tokens=100, temperature=0.3, top_p=0.9)
question = "Can you summarize this speech?"
context = """Speech is the use of the human voice as a medium for language. Spoken language combines vowel and consonant sounds to form units of meaning like words, which belong to a language's lexicon. There are many different intentional speech acts, such as informing, declaring, asking, persuading, directing; acts may vary in various aspects like enunciation, intonation, loudness, and tempo to convey meaning. Individuals may also unintentionally communicate aspects of their social position through speech, such as sex, age, place of origin, physiological and mental condition, education, and experiences.
While normally used to facilitate communication with others, people may also use speech without the intent to communicate. Speech may nevertheless express emotions or desires; people talk to themselves sometimes in acts that are a development of what some psychologists (e.g., Lev Vygotsky) have maintained is the use of silent speech in an interior monologue to vivify and organize cognition, sometimes in the momentary adoption of a dual persona as self addressing self as though addressing another person. Solo speech can be used to memorize or to test one's memorization of things, and in prayer or in meditation.
"""

chain = prompt | llm | output_parser
response = chain.invoke({"question":question,"context":context})
print(response)