from io import BytesIO
import base64
import matplotlib.pyplot as plt


'''
Define a function that takes the ID
def get_recipename_from_id(val):
    recipe_name = Recipe.objects.get(id=val)
    The name is returned back
    return recipe_name
'''


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    # return the image/graph
    return graph

# chart_type: user input o type of chart, data: pandas dataframe


def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')

    fig = plt.figure(figsize=(8, 5))

    def get_genres():
        return list(set(sorted(data['genre'])))

    def get_totals():
        genres = get_genres()
        totals = []
        for gen in genres:
            counter = 0
            for i in data['genre']:
                if i == gen:
                    counter += 1
            totals.append(counter)
        return totals

    def get_avg_ratings():
        genres = get_genres()
        ratings = []
        for gen in genres:
            totalizer = 0
            counter = 0
            for e, g in enumerate(data['genre']):
                if g == gen:
                    totalizer += data['rating'][e]
                    counter += 1
            avg_rating = totalizer / counter
            ratings.append(avg_rating)
        return ratings

    def get_avg_cook_times():
        genres = get_genres()
        cook_times = []
        for gen in genres:
            totalizer = 0
            counter = 0
            for e, g in enumerate(data['genre']):
                if g == gen:
                    totalizer += data['cooking_time'][e]
                    counter += 1
            avg_cook_time = totalizer / counter
            cook_times.append(avg_cook_time)
        return cook_times

    # select chart_type based on user input from the form
    if chart_type == '#1':
        genres = get_genres()
        totals = get_totals()

        print('pie chart: ', genres, totals)
        plt.pie(totals, labels=genres)

    elif chart_type == '#2':
        genres = get_genres()
        ratings = get_avg_ratings()

        print('bar chart: ', genres, ratings)
        plt.bar(genres, ratings)

    elif chart_type == '#3':
        genres = get_genres()
        cook_times = get_avg_cook_times()

        print('line chart: ', genres, cook_times)
        plt.plot(genres, cook_times)

    else:
        print('Error with the chart type')

    # layout details
    plt.tight_layout()

    # render the graph to a file
    chart = get_graph()
    return chart
