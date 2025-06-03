# import plotly.express as px
# import pandas as pd
# data = pd.DataFrame(dict(keys=[10000, 20000, 15000, 5000],
# values=["Labour Cost", "Manufacturing Cost", "Promotion Cost", "Selling Cost"]))
# figure = px.line_polar(data, r='keys', theta='values', line_close=True)
# figure.update_traces(fill="toself")
# figure.write_image("g_radar.png")


import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame(dict(
    value = [8, 12, 7, 14, 10],
    variable = ['V1', 'V2', 'V3', 'V4', 'V5']))
           
fig = px.line_polar(df, r = 'value', theta = 'variable', line_close = True)
fig.update_traces(fill = 'toself')

fig.write_image("g_radar.png")
