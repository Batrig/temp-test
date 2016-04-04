import plotly
import datetime

from plotly.graph_objs import *
# auto sign-in with credentials or use py.sign_in()
token1 = "b29gyiuuqg"
token2 = "ddev15zx4p"
plotly.tools.set_credentials_file(username='Girtab', api_key='6osdll41pt')

trace1 = plotly.graph_objs.Scatter(
        x=[],
        y=[],
        stream=dict(token=token1)
    )

trace2 = plotly.graph_objs.Scatter(
        x=[],
        y=[],
        stream=dict(token=token2)
    )

data = plotly.graph_objs.Data([trace1, trace2])

plotly.plotly.plot(data)
