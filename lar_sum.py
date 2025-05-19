from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")

# Define the stop sequence
stop_sequence = ["\n", "END"]

# Initialize the language model
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    max_tokens=100,
    temperature=0.3,
    top_p=0.9,
    # top_k=50,
    stop=stop_sequence
)

# Define the prompt template for summarizing chunks
map_template = """Summarize the following content into a concise 1–2 line summary:
                        {content}
                        Summary:
                """


map_prompt = PromptTemplate.from_template(map_template)

# Initialize the LLMChain
map_chain = LLMChain(prompt=map_prompt, llm=llm, output_parser=StrOutputParser())

# Define the context
context="""
            Speech is the use of the human voice as a medium for language. Spoken language combines vowel and consonant sounds to form units of meaning like words, 
            which belong to a language's lexicon. There are many different intentional speech acts, such as informing, declaring, asking, persuading, directing; 
            acts may vary in various aspects like enunciation, intonation, loudness, and tempo to convey meaning. Individuals may also unintentionally 
            communicate aspects of their social position through speech, such as sex, age, place of origin, physiological and mental condition, education, and experiences.
            While normally used to facilitate communication with others, people may also use speech without the intent to communicate. Speech may nevertheless express 
            emotions or desires; people talk to themselves sometimes in acts that are a development of what some psychologists (e.g., Lev Vygotsky) have maintained is 
            the use of silent speech in an interior monologue to vivify and organize cognition, sometimes in the momentary adoption of a dual persona as self addressing 
            self as though addressing another person. Solo speech can be used to memorize or to test one's memorization of things, and in prayer or in meditation.
        """

# Split the context into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=500,
    separators=["\n\n", "\n", " ", ""]
)

chunks = text_splitter.split_text(context)
total = [chunk for chunk in chunks]
# print(total)

summaries = [map_chain.invoke({"content": chunk})["text"] for chunk in chunks]
final_summary = " ".join(summaries)
print(final_summary)


# Check for Missing Keys: Before accessing the "text" key, verify its existence to prevent KeyError
# summaries = [
#     map_chain.invoke({"content": chunk}).get("text", "Summary not available")
#     for chunk in chunks
# ]
# final_summary = " ".join(summaries)
# print(final_summary)
