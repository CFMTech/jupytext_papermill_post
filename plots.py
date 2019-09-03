import pandas as pd
import world_bank_data as wb
import plotly.graph_objs as go
import plotly.offline as offline


def sundial_plot(metric='SP.POP.TOTL', title='World Population', year=2000):
    """Plot the given metric as a sundial plot"""
    countries = wb.get_countries()
    values = wb.get_series(metric, date=year, id_or_value='id', simplify_index=True)

    df = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[
        countries.region != 'Aggregates']
    df['values'] = values

    # The sunburst plot requires weights (values), labels, and parent (region, or World)
    # We build the corresponding table here
    columns = ['parents', 'labels', 'values']

    level1 = df.copy()
    level1.columns = columns
    level1['text'] = level1['values'].apply(lambda pop: '{:,.0f}'.format(pop))

    level2 = df.groupby('region')['values'].sum().reset_index()[['region', 'region', 'values']]
    level2.columns = columns
    level2['parents'] = 'World'
    # move value to text for this level
    level2['text'] = level2['values'].apply(lambda pop: '{:,.0f}'.format(pop))
    level2['values'] = 0

    level3 = pd.DataFrame({'parents': [''], 'labels': ['World'],
                           'values': [0.0], 'text': ['{:,.0f}'.format(values.loc['WLD'])]})

    all_levels = pd.concat([level1, level2, level3], axis=0).reset_index(drop=True)

    offline.iplot(go.Figure(
        data=[go.Sunburst(hoverinfo='text', **all_levels)],
        layout=go.Layout(title='{} (World Bank, {})'.format(title, year),
                         width=800, height=800)))
