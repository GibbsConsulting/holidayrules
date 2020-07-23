import dash
import dash_html_components as html
import dash_core_components as dcc

import dash_table
import plotly.express as px

import pandas as pd


from holidayrules.ruleset import RuleSet
from holidayrules.rules import (HolidayRule,
                                new_year_roll_back,
                                fixed_date_roll_both,
                                fixed_date_roll_forward,
                                )


rules = [HolidayRule("New year, rolling back",
                     "New year rolling backwards if a Saturday",
                     new_year_roll_back),
         HolidayRule("New year, rolling forwards on sunday",
                     "NY2",
                     fixed_date_roll_both(1, 1)),
         HolidayRule("Canada Day",
                     "First of July",
                     fixed_date_roll_forward(7, 1)),
]


hrs = RuleSet(rules)
date_items = RuleSet.values_by_ymd(hrs.dates_for_years(range(2018, 2038)))
dfHols = pd.DataFrame(date_items)


dfHols['DateYear'] = dfHols['date_string'].apply(lambda x: int(x[:4]))
dfHols['DateMonth'] = dfHols['date_string'].apply(lambda x: int(x[4:6]))
dfHols['DateDay'] = dfHols['date_string'].apply(lambda x: int(x[6:]))


fig = px.bar(dfHols, x='date_string', y='DateDay', color='year')

def year_choices(df):
    years = df['year'].sort_values().unique()
    return [{'label': str(y), 'value': y} for y in years]


month_names = ['Jan', 'Feb', 'Mar',
               'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep',
               'Oct', 'Nov', 'Dec',
               ]

month_choices = [{'label': month_names[mth - 1], 'value': mth} for mth in range(1, 13)]


app = dash.Dash(__name__)


app.layout = html.Div(children=[html.H1("App here and there"),
                                dcc.Dropdown(id="year_choice",
                                             options=year_choices(dfHols),
                                             multi=True,
                                             ),
                                dcc.Dropdown(id="month_choice",
                                             options=month_choices,
                                             multi=True,
                                             ),
                                dash_table.DataTable(id='hol_table',
                                                     columns=[{"name": i, "id": i} for i in dfHols.columns],
                                                     data=dfHols.to_dict('records'),),
                                dcc.Graph(figure=fig),
                                ])


@app.callback(dash.dependencies.Output('hol_table', 'data'),
              [dash.dependencies.Input('year_choice', 'value'),
               dash.dependencies.Input('month_choice', 'value')])
def callback_fix_choices(years, months):
    if years:
        in_years = dfHols['year'].apply(lambda year: year in years)
        df = dfHols[in_years]
    else:
        df = dfHols

    if months:
        df = df[df['month'].apply(lambda month: month in months)]

    return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
