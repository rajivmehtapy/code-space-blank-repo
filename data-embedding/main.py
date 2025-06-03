from bertopic import BERTopic
# from bertopic.representation import OpenAI
from langchain.chains.question_answering import load_qa_chain
# from langchain.llms import OpenAI as LangChainOpenAI
import numpy as np
import pandas as pd
import plotly.express as px  # Reference: https://plotly.com/python/radar-chart/  [[7]]
from umap import UMAP
from datasets import load_dataset
import openai
from bertopic.representation import OpenAI
import os
os.environ["OPENAI_API_KEY"] = "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"
# Load dataset from Hugging Face Hub
dataset = load_dataset("rajivmehtapy/md_highland_ds")
# Extract documents from the 'train' split - adjust split/column name as needed
# Step 1: Fit BERTopic model with calculate_probabilities=True
# docs = dataset["train"]["text"]  # Assuming 'text' is the column name
# topic_model = BERTopic(calculate_probabilities=True)
# topics, probs = topic_model.fit_transform(docs)

docs = dataset["train"]["text"]  # Assuming 'text' is the column name
# Step 1: Fit BERTopic model with calculate_probabilities=True
docs_part = docs[:1000]
# LangChain QA Chain initialization
# llm = LangChainOpenAI(temperature=0.4)
llm = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
# qa_chain = load_qa_chain(llm, chain_type="stuff")

# BERTopic Representation Model
# Initialize OpenAI representation model directly with API key
prompt = "What are these documents about? Please give a single label."

representation_model = OpenAI(
    client=llm,
    model="gpt-4.1-nano", 
    api_key=os.environ["OPENAI_API_KEY"],
    prompt=prompt
)

topic_model = BERTopic(
    calculate_probabilities=True,
    representation_model=representation_model  # Added representation model
)
topics, probs = topic_model.fit_transform(docs_part)

# Step 2: Compute average topic probabilities across documents
avg_probs = np.mean(probs, axis=0)

# Step 3: Prepare data for radar chart
topic_names = [f"Topic {i}" for i in range(len(avg_probs))]
df = pd.DataFrame({"variable": topic_names, "value": avg_probs})

# Step 4: Create and save radar chart using Plotly
fig = px.line_polar(df, r="value", theta="variable", line_close=True)
fig.update_traces(fill="toself")  # Fill area inside the radar chart
fig.write_image("radar_chart_plotly.png", engine="kaleido")  # Save as PNG

print("Radar chart saved as 'radar_chart_plotly.png'")


# import plotly.express as px
# import pandas as pd
# data = pd.DataFrame(dict(keys=[10000, 20000, 15000, 5000],
# values=["Labour Cost", "Manufacturing Cost", "Promotion Cost", "Selling Cost"]))
# figure = px.line_polar(data, r='keys', theta='values', line_close=True)
# figure.update_traces(fill="toself")
# figure.write_image("g_radar.png")


# import plotly.express as px
# import pandas as pd

# # Sample data
# df = pd.DataFrame(dict(
#     value = [8, 12, 7, 14, 10],
#     variable = ['V1', 'V2', 'V3', 'V4', 'V5']))
           
# fig = px.line_polar(df, r = 'value', theta = 'variable', line_close = True)
# fig.update_traces(fill = 'toself')

# fig.write_image("g_radar.png")


# Modify BERTopic initialization with custom UMAP parameters
