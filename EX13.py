import altair as alt
from vega_datasets import data

cars = data.cars()

chart = alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
).interactive()

chart.save('ex13_cars_scatter.html')
import webbrowser, os
webbrowser.open('file://' + os.path.realpath('ex13_cars_scatter.html'))
