from bertopic import BERTopic
import numpy as np
import pandas as pd
import plotly.express as px  # Reference: https://plotly.com/python/radar-chart/  [[7]]

# Sample documents
docs = [
    "I love machine learning and data science",
    "Deep learning is fascinating and powerful",
    "Natural language processing opens up many possibilities",
    "Data visualization helps in understanding complex models",
    "Python libraries like scikit-learn and Hugging Face are great"
]

# Step 1: Fit BERTopic model with calculate_probabilities=True
topic_model = BERTopic(calculate_probabilities=True)
topics, probs = topic_model.fit_transform(docs)

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
