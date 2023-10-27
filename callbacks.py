from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

def get_callbacks(app, shark_sorted_df, sharks_species, fig_age, fig_usa, fig_aus, fig_sa, fig_world):
    @app.callback(#callback for the graph3
        Output('graph3', 'figure'),
        Output('tab3', 'label'),
        [Input('fatal-dropdown', 'value')]
    )
    def update_graph3(selected_value):#update function for the graph3
            if selected_value == 'Y':
                label = 'Fatal attack'
            else:
                label = 'Not fatal attack'

            filtered_df = sharks_species[sharks_species['Fatal (Y/N)'] == selected_value]#we make a graph according to the value selected
            species_attack = filtered_df.groupby('Species')['Species'].count().sort_values(ascending=False)[1:15]

            data = go.Bar(x = species_attack.index,y=species_attack.values,text=species_attack.values,textposition='auto', marker_color='rgb(102,197,204)')

            layout = go.Layout(title = 'Shark Attack by Species', 
                        xaxis=dict(title='Species'),
                        yaxis=dict(title='Attack Count',visible=False),
                        paper_bgcolor='cornsilk',
                        plot_bgcolor='rgba(252,248,244,1.00)',
                        font = dict(
                            family = "Montserrat",
                            size = 18,
                            color = 'black'
                            )
                        )

            fig = go.Figure(
                data=data,
                layout=layout
            )   
            fig.update_layout(title=f'Number of {label.lower()} depending on shark\'s species')#changing the title
            return fig, label


    @app.callback(#callback for the graph Age and lethality
            Output('graph7', 'figure'),
            Input('show-details-checkbox', 'value')
    )
    def update_graph7(show_details):
        if 'show-details' in show_details:
                # If 'show-details' is selected, display the detailed graph
                return fig_age
        else:#else display a non detailed graph
                fig = px.histogram(shark_sorted_df, x="Age", title="Age and lethality")
                fig.update_xaxes(title_text="Age")
                fig.update_yaxes(title_text="Number of attacks")
                fig.update_layout(
                        plot_bgcolor='rgba(252,248,244,1.00)',
                        paper_bgcolor='cornsilk',
                        font = dict(
                            family = "Montserrat",
                            size = 18,
                            color = 'black'
                            )
                )
        return fig


    @app.callback(#callback for the graph_maps
            Output('graph_maps', 'figure'),
            Input('shark-attack-details-dropdown', 'value')
        )
    def update_map(selected_option):#according to the selected option, display a different map
            if selected_option == 'usa':
                return fig_usa
            elif selected_option == 'australia':
                return fig_aus
            elif selected_option == 'south-africa':
                return fig_sa
            else:
                return fig_world


    app.run_server(debug=True)