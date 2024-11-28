from transformers import BartTokenizer, BartForConditionalGeneration
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
import pandas as pd

class GroqChatAgent:
    def __init__(self, api_key, system_prompt, memory_length, csv_file):
        self.groq_api_key = api_key
        self.model = 'llama3-8b-8192'  # model
        self.system_prompt = system_prompt
        self.memory = ConversationBufferWindowMemory(k=memory_length, memory_key="chat_history", return_messages=True)
        self.groq_chat = ChatGroq(groq_api_key=self.groq_api_key, model_name=self.model)
        self.chat_history = []
        self.data = pd.read_csv(csv_file)

    def get_response(self, user_question):
        if not self.is_farming_related(user_question):
            if "give me news about" in user_question.lower():
                return self.handle_news_request(user_question)
            elif "website to buy and sell goods" in user_question.lower():
                return "You can visit this website to buy and sell goods: http://127.0.0.1:5000"
            else:
                return "I can only answer farming-related questions. Please ask about farming."

        # Extracting insights from the CSV data
        csv_insight = self.extract_insight(user_question)

        for message in self.chat_history:
            self.memory.save_context(
                {'input': message['human']},
                {'output': message['AI']}
            )

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=self.system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template(f"{user_question}\n\nData Insight: {csv_insight}")
            ]
        )

        conversation = LLMChain(
            llm=self.groq_chat,
            prompt=prompt,
            verbose=True,
            memory=self.memory,
        )

        response = conversation.predict(human_input=user_question)
        self.chat_history.append({'human': user_question, 'AI': response})
        return response

    def is_farming_related(self, question):
        farming_keywords = ["crop", "yield", "farm", "agriculture", "soil", "plant", "harvest", "irrigation", "pest", "fertilizer", "weather", "climate"]
        for keyword in farming_keywords:
            if keyword in question.lower():
                return True
        return False

    def extract_insight(self, question):
        if "crop" in question.lower():
            return self.data["Crop"].unique().tolist()
        elif "yield" in question.lower():
            return self.data[["Crop", "Yield"]].groupby("Crop").mean().to_dict()
        else:
            return "No specific insights found for this question."

    def summarize_article(self, article_text):
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        summarization_model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        inputs = tokenizer(article_text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = summarization_model.generate(inputs['input_ids'], num_beams=4, max_length=150, early_stopping=True)
        summarized_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summarized_text

    def handle_news_request(self, request):
        return "Please provide a valid request in the format 'Give me news about {topic}'."

# Config
groq_api_key = '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'
system_prompt = "You're an AI bot here to help farmers. Make sure to be understanding and give kind replies without any slurs or bad language."
memory_length = 5
csv_file = 'Crop_Recommendation.csv'

# Initialization
agent = GroqChatAgent(groq_api_key, system_prompt, memory_length, csv_file) 