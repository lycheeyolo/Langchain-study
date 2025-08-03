import getpass
import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk
import os

load_dotenv()
model = ChatOpenAI(
    # 环境变量中配置您的API Key
    openai_api_key=os.getenv("VOLCES_KEY"), 
    # 替换为您需要调用的模型服务Base Url
    openai_api_base=os.getenv("VOLCES_URL"),
    # 替换为您创建推理接入点 ID
    model_name=os.getenv("VOLCES_MODEL_NAME")
)

print(model.invoke("你是谁？"))

# template = """Question: {question}

# Answer: """

# prompt = PromptTemplate.from_template(template)

# question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

# llm_chain = prompt | model

# print(llm_chain.invoke(question))

