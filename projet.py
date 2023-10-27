import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import json

def filtration_df():
    df = pd.read_csv('attacks.csv', encoding='latin1') #latin1, utf8 does not work
    df = df.rename(columns={'Species ':'Species'}) #take off the space after the column Species
    df = df.rename(columns={'Sex ':'Sex'}) #take off the space after the column Sex
    df = df.drop(['Unnamed: 22', 'Unnamed: 23'], axis=1) #columns with only NA values
    df = df.dropna(how='all') #drop lines where there are only Nan values
    df = df[df['Year'] >= 1800] #few data before 1800
    # Modifying the value in Sex column
    # Fill NaN value first with Unknown
    df['Sex'] = df['Sex'].fillna("Unknown")
    # Male
    df.loc[df['Sex'].str.contains("M|M "), 'Sex'] = "Male"
    # Female
    df.loc[df['Sex'].str.contains("F|F "), 'Sex'] = "Female"
    # Value other than Female and Male becomes Unspecified
    df.loc[~df['Sex'].str.contains("Male|Female"), 'Sex'] = "Unknown"


    df_Activity = df.copy()
    df_Activity = df_Activity.dropna(subset=['Activity'])#drop the na because we can't change names if not
    df_Activity.loc[df_Activity['Activity'].str.contains('fishing|Fishing', case=False), 'Activity'] = 'Fishing'#so we have all type of fishing
    df_Activity.loc[df_Activity['Activity'].str.contains('diving|Diving', case=False), 'Activity'] = 'Diving'#so we have all type of diving

    df_Year = df.groupby('Year')['Date'].count().reset_index() #attack numbers by years

    df_Species = df.copy()
    df_Species = df_Species.dropna(subset=['Species'])#drop the na because we can't change names if not
    df_Species.loc[df_Species['Species'].str.contains('white shark|White shark', case=False), 'Species'] = 'White shark'
    df_Species.loc[df_Species['Species'].str.contains('tiger shark|Tiger shark', case=False), 'Species'] = 'Tiger shark'
    df_Species.loc[df_Species['Species'].str.contains('6\'|1.8 m', case=False), 'Species'] = '1.8m shark'
    df_Species.loc[df_Species['Species'].str.contains('Zambesi|zambesi', case=False), 'Species'] = 'Zambesi shark'
    df_Species.loc[df_Species['Species'].str.contains('bronze|Bronze', case=False), 'Species'] = 'Bronze whaler shark'
    df_Species.loc[df_Species['Species'].str.contains('5\'|1.5 m', case=False), 'Species'] = '1.5m shark'
    df_Species.loc[df_Species['Species'].str.contains('4\'|1.2 m', case=False), 'Species'] = '1.2m shark'
    df_Species.loc[df_Species['Species'].str.contains('12\'|3.7 m', case=False), 'Species'] = '3.7m shark'
    df_Species.loc[df_Species['Species'].str.contains('3\'|0.9 m', case=False), 'Species'] = '0.9m shark'
    df_Species.loc[df_Species['Species'].str.contains('8\'|2.4 m', case=False), 'Species'] = '2.4m shark'
    df_Species.loc[df_Species['Species'].str.contains('10\'|3 m', case=False), 'Species'] = '3m shark'
    df_Species.loc[df_Species['Species'].str.contains('2 m', case=False), 'Species'] = '2m shark'
    df_Species.loc[df_Species['Species'].str.contains('not confirmed|unconfirmed', case=False), 'Species'] = None
    return df, df_Activity, df_Year, df_Species

def byYearGraph(df): 
    fig = px.line(df,x='Year', y='Date', title='Shark Attack by Year')#a line
    fig.update_layout(
                        yaxis_title='Attacks',
                        plot_bgcolor='rgba(252,248,244,1.00)',
                        paper_bgcolor='cornsilk',
                        font = dict(
                        family = "Montserrat",
                        size = 18,
                        color = 'black'
                        )
                    )#visual modification : coulors, legend,...
    fig.update_traces(
    line_color='rgb(102,197,204)',
    hovertemplate='Year: %{x}<br>Number: %{y}'
    )#visual modification : coulors, legend,...
    return fig

def byActivityGraph(df):
    prov_activity = df[df.Type == 'Provoked'].groupby('Activity')['Activity'].count().sort_values(ascending=False)[:10]#The 10 activities most common
    fig = px.bar(prov_activity, x=prov_activity.values, y=prov_activity.index, orientation='h', labels={'index':'','x':'Attack Count'},
                title = 'Provoked Attacks by Activity')#barplot
    fig.update_layout(
                        plot_bgcolor='rgba(252,248,244,1.00)',
                        paper_bgcolor='cornsilk',
                        font = dict(
                        family = "Montserrat",
                        size = 18,
                        color = 'black'
                        )#visual modification : coulors, legend,...
                    )
    fig.update_traces(marker_color='rgb(102, 197, 204)')#bar colors
    return fig

def bySexGraph(df):
    # Count by gender
    bySex_count = df['Sex'].value_counts().reset_index().rename(columns={'index':'Gender','Sex':'Count'})

    fig = px.pie(data_frame = bySex_count,
             values = 'Count',
             names = 'Gender',
             title = 'Shark Attack by Gender',
             color_discrete_sequence=px.colors.qualitative.Pastel
             )#a pie

    fig.update_traces(textposition ='outside',
                    textinfo = 'label+percent')#informative text modification
    fig.update_layout(paper_bgcolor='cornsilk',
                    legend_title = 'Gender',
                    font = dict(
                        family = "Montserrat",
                        size = 18,
                        color = 'black'
                    ))#visual modification : colors, legend,...
    
    return fig

def worlGraph(df):
    byCountry_count = df['Country'].value_counts().reset_index().rename(columns={'Country':'Count','index':'Country'})#count by countries
    fig = px.choropleth(data_frame = byCountry_count,
                        locations = 'Country',
                        color='Count',
                        color_continuous_scale="Viridis",
                        locationmode = 'country names',
                        scope = 'world',
                        title = 'Shark Attack around the World')#a map of every country 

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

def usaGraph(df):
    # Take the data from the USA in the dataframe
    byAreaUS_count = df[df['Country'] == "USA"]['Area'].value_counts().reset_index().rename(columns={'Area':'Count','index':'Area'})

    # Create a dictionnary to match the locationmode='USA-states' in the graph
    states_code = {'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA',
                'Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC',
                'Florida': 'FL','Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN',
                'Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD',
                'Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO',
                'Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ',
                'New Mexico': 'NM','New York': 'NY','North Carolina': 'NC','North Dakota': 'ND','Ohio': 'OH',
                'Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Rhode Island': 'RI','South Carolina': 'SC',
                'South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virginia': 'VA',
                'Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}

    byAreaUS_count['State Code'] = byAreaUS_count['Area'].map(states_code)

    fig = px.choropleth(data_frame = byAreaUS_count,
                        locations = 'State Code',
                        color='Count',#color scale depending on the number of attacks
                        color_continuous_scale="Viridis",#type of color
                        locationmode = 'USA-states', #map by states of USA
                        scope = 'usa',#USA map
                        title = 'Shark Attacks in the USA',#title
                        hover_name = 'Area')# Display region names when hovering

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

def australiaGraph(df):
    with open('states_australia.geojson', 'r') as file:  # source : https://github.com/rowanhogan/australian-states/blob/master/states.geojson
        aus_map = json.load(file)
    byAreaAUS_count = df[df['Country'] == "AUSTRALIA"]['Area'].value_counts().reset_index().rename(columns={'Area':'Count','index':'Area'})

    fig = px.choropleth(byAreaAUS_count,
                        geojson=aus_map,#a json map already done
                        locations='Area', #column of the dataset
                        color='Count',#color scale depending on the number of attacks
                        color_continuous_scale="Viridis",#type of color
                        featureidkey="properties.STATE_NAME",
                        title = 'Shark Attack in Australia',#title
                        )


    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":10})
    fig.update_geos(fitbounds="locations", visible=False)  # Fit the map to the regions in the dataset
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

def africaGraph(df):
    with open('states_south_africa.json', 'r') as file:      # source : https://github.com/fletchjeff/ZA-Census-Data-Explorer/blob/main/assets/za-provinces.topojson converted to geojson
        sa_map = json.load(file)
    
    byAreaSA_count = df[df['Country'] == "SOUTH AFRICA"]['Area'].value_counts().reset_index().rename(columns={'Area':'Count','index':'Area'})

    # Creation of a dictionnary to rename the states to match the names in the states_south_africa file
    mapping = {
        'Western Cape Province': 'Western Cape',
        'Eastern Cape Province': 'Eastern Cape',
        'Western Province': 'Western Cape',
        'Eastern Province': 'Eastern Cape',
        'KwaZulu-Natal between Port Edward and Port St': 'KwaZulu-Natal',
    }

    # Manually adding the regions where the count is 0 for them to appear on the map and be colorized
    other_regions = [
        {'Area': 'Free State', 'Count': 0},
        {'Area': 'Gauteng', 'Count': 0},
        {'Area': 'Limpopo', 'Count': 0},
        {'Area': 'Mpumalanga', 'Count': 0},
        {'Area': 'North West', 'Count': 0},
        {'Area': 'Northern Cape', 'Count': 0},
    ]

    other_regions_df = pd.DataFrame(other_regions)
    byAreaSA_count = pd.concat([byAreaSA_count, other_regions_df], ignore_index=True) # Concatenation of the two dataframes

    byAreaSA_count['Area'] = byAreaSA_count['Area'].apply(lambda x: mapping.get(x, x)) # Use of the dictionnary already created to rename the states
    byAreaSA_count = byAreaSA_count.groupby('Area', as_index=False)['Count'].sum() # Some rows are divided in subrows, we merge them
    fig = px.choropleth(byAreaSA_count,
                    geojson=sa_map, 
                    locations='Area', 
                    color='Count',
                    color_continuous_scale="Viridis",
                    featureidkey="properties.PROVINCE",
                    hover_name='Area',  # Display region names when hovering
                    )
    fig.update_geos(fitbounds="locations", visible=False)  # Only the regions in our dataset will appear
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":10}) # Setting the plot to occupy all available space without any margin around it
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

def clean_time(time_str):
    time_str = str(time_str).lower()
    if 'h' in time_str:                           # Only keeping the hour and dropping the minutes
        time_str = time_str.split('h')[0]
    if time_str.isdigit() and len(time_str) == 1: # Padding singlee-digit time
        time_str = time_str.zfill(2)
    if 'midday' in time_str:
        time_str = '12'
    if 'noon' in time_str:
        time_str = 'afternoon'
    if 'morning' in time_str:
        time_str = 'morning'
    if len(time_str) == 4 and time_str.isdigit(): # Some rows are still represented by the format "HHmm", we keep the hour
        time_str = time_str[:2]

    return time_str

def hoursGraph(df):
    shark_n = df.copy()
    shark_n.dropna(subset=['Time'], inplace=True)

    # Set the accepted time periods
    time_periods = ["evening", "morning", "night", "afternoon"]

    # Apply the clean_time sorting function 
    shark_n['Time'] = shark_n['Time'].apply(clean_time)


    shark_n['Time'] = shark_n['Time'].str.replace(r'^(.*?)(\d{2})$', r'\2', regex=True)  # If there is some text with an hour in it, only keep the hour
    shark_n = shark_n[shark_n['Time'].isin(time_periods) | (shark_n['Time'].str.isdigit() )] # Drop the rows with incorrect data


    fig = px.histogram(shark_n, x="Time")

    #Select only the numeric time values
    numeric_time_values = shark_n[shark_n['Time'].str.isdigit()]['Time'].astype(int)
    numeric_time_values = numeric_time_values[numeric_time_values <= 24]

    #Creating a histogram with only the numeric values
    fig = px.histogram(numeric_time_values, 
                        x="Time",
                        title="Hour of the attack",
                        )

    fig.update_xaxes(title_text="Time (hours)")
    fig.update_yaxes(title_text="Number of attacks")

    fig.update_traces(marker_color="rgb(102, 197, 204)", marker_line_color="black", marker_line_width=1, opacity=1)#changes the histogram visual
    fig.update_layout(plot_bgcolor='rgba(252,248,244,1.00)',
                            paper_bgcolor='cornsilk',
                            barmode="overlay",
                            bargap=0.1,
                            font = dict(
                                family = "Montserrat",
                                size = 18,
                                color = 'black'
                            )#visual modification : coulors, legend,...
    )
    return fig
# Creation of sorting function
def categorize_time(time_str):
    if time_str.isdigit():
        hour = int(time_str)
        if 0 <= hour < 6:
            return "night"
        elif 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 24:
            return "evening"
    else:
        return time_str

def periodGraph(df):
    shark_n = df.copy()
    shark_n.dropna(subset=['Time'], inplace=True)

    # Set the accepted time periods
    time_periods = ["evening", "morning", "night", "afternoon"]

    # Apply the clean_time sorting function 
    shark_n['Time'] = shark_n['Time'].apply(clean_time)
    shark_n['Time'] = shark_n['Time'].str.replace(r'^(.*?)(\d{2})$', r'\2', regex=True)  # If there is some text with an hour in it, only keep the hour
    shark_n = shark_n[shark_n['Time'].isin(time_periods) | (shark_n['Time'].str.isdigit() )] # Drop the rows with incorrect data

    # Copy of the cleaned data
    shark_f = shark_n.copy()     
    # Apply the sorting function
    shark_f['Time'] = shark_f['Time'].apply(categorize_time)

    time_count = shark_f['Time'].value_counts().reset_index().rename(columns={'index':'Time','Time':'Count'})

    fig = px.pie(data_frame = time_count,
             values = 'Count',
             names = 'Time',
             title = 'Time of the attack',
             color_discrete_sequence=px.colors.qualitative.Pastel
             )#create a pie with its details

    fig.update_traces(textposition ='outside',
                    textinfo = 'label+percent')#information text 

    fig.update_layout(paper_bgcolor='cornsilk',
                    legend_title = 'Time',
                    font = dict(
                        family = "Montserrat",
                        size = 18,
                        color = 'black'
                    ))#visual modification : colors, legend,...
    return fig

def ageGraph(df):
    shark_a = df.copy()
    shark_a.dropna(subset=['Age'], inplace=True)                                # Drop rows with Na values 
    shark_a = shark_a[shark_a['Age'].str.match(r'^\d+(\.\d+)?$')]               # If there is an age and some text in it, only keep the age
    shark_a['Fatal (Y/N)'] = shark_a['Fatal (Y/N)'].str.upper()
    shark_a = shark_a[shark_a['Fatal (Y/N)'].isin(['Y', 'N', 'UNKNOWN'])]       # Define the valid categories
    shark_a['Age'] = pd.to_numeric(shark_a['Age'])
    shark_sorted = shark_a.sort_values(by='Age', ascending=True)                # Sort the values 

    fig = px.histogram(shark_sorted, x="Age", color="Fatal (Y/N)", title="Age and lethality")#histogram of the attacks depending on the age og the person
    fig.update_xaxes(title_text="Age")
    fig.update_yaxes(title_text="Number of attacks")
    fig.update_layout(
        plot_bgcolor='rgba(252,248,244,1.00)',
        paper_bgcolor='cornsilk',
        legend_title = 'Fatal',
        font = dict(
            family = "Montserrat",
            size = 18,
            color = 'black'
            ),
            legend=dict(
                font=dict(size=14)  
            )#visual modification : colors, legend,...
        )
    fig.update_traces(
        selector=dict(name='Y'),
        name='YES'
    )#legend changes

    fig.update_traces(
        selector=dict(name='N'),
        name='NO'
    )#legend changes
    return fig, shark_sorted


df, df_Activity, df_Year, df_Species = filtration_df()

fig_year = byYearGraph(df_Year)
fig_activity = byActivityGraph(df_Activity)
fig_sx = bySexGraph(df)
fig_world = worlGraph(df)
fig_hours = hoursGraph(df)
fig_time_periods = periodGraph(df)
fig_age, shark_sorted_df = ageGraph(df)
fig_usa = usaGraph(df)
fig_aus = australiaGraph(df)
fig_sa = africaGraph(df)


app = dash.Dash(__name__)#create the dash


app.layout = html.Div(style={'backgroundColor': 'cornsilk'}, children=[
        dcc.Tabs([#different tabs, each tab is for a graph
            dcc.Tab(id = 'tab1',label='Years', children=[#first graph : number of attacks according to the age
                dcc.Tab(label='tab1', children=[
                    html.Div([
                        dcc.Graph(id='graph1', figure=fig_year),#we reload the fig
                        html.Div(
                            id = 'description1', 
                            children = "the number of shark attacks by years",#description on the dashboard for this tab
                            style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}#description visual
                            )
                    ])
                ])
            ]),
            dcc.Tab(id= 'tab2',label='Gender', children=[
                html.Div([#first graph : number of attacks according to the gender
                    dcc.Graph(id='graph2', figure=fig_sx),#we reload the fig
                    html.Div(
                        id = 'description2',
                        children = "the proportion of shark attack by genders since 1800",#description on the dashboard for this tab
                        style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}#description visual
                        )
                ])
            ]),
            dcc.Tab(id= 'tab3', label='Fatal or not', children=[
                html.Div([
                    dcc.Dropdown(
                        id='fatal-dropdown', 
                        options=[#dropdown options
                            {'label' : 'fatal attack', 'value' : 'Y'},
                            {'label' : 'not fatal attack', 'value' : 'N'}
                        ],
                        value = 'Y',#value at the beginning
                        style={'width': '50%'}#size
                    ),
                    dcc.Graph(id='graph3'),
                    html.Div(
                        id = 'description3',
                        children = "the number of fatal or not attacks by known shark species since 1800",#description on the dashboard for this tab
                        style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}#description visual
                        )  
                ])
            ]),

            dcc.Tab(id= 'tab4', label='Activity', children=[
                html.Div([
                    dcc.Graph(id='graph4', figure=fig_activity),#we reload the fig
                    html.Div(
                        id = 'description4',
                        children = "the number of shark attack by human activity since 1800",#description on the dashboard for this tab
                        style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}#description visual
                        )
                ])
            ]),
            dcc.Tab(label='Shark Attack Map', children=[
            html.Div([
                html.Div(
                        id = 'text_dropdown',
                        children = "Map :",
                        style={'text-align': 'left', 'font-size': '18px', 'margin-top': '10px'}#description visual
                        ),
                dcc.Dropdown(
                    id='shark-attack-details-dropdown',
                    options=[
                        {'label': 'World', 'value': 'World'},
                        {'label': 'USA', 'value': 'usa'},
                        {'label': 'Australia', 'value': 'australia'},
                        {'label': 'South Africa', 'value': 'south-africa'},
                    ],#dropdown options
                    value='World'#value at the beginning
                ),
                dcc.Graph(id='graph_maps', figure=fig_world),#we reload the fig
            ])
        ]),
            dcc.Tab(id= 'tab5',label='Time', children=[
                html.Div([
                    dcc.Graph(id='graph5', figure=fig_hours),#we reload the fig1
                    dcc.Graph(id='graph6', figure=fig_time_periods),#we reload the fig2
                ]),
            ]),
            dcc.Tab(id= 'tab6',label='Attacks by age', children=[
                html.Div([
                    dcc.Checklist(
                        id='show-details-checkbox',
                        options=[
                            {'label': 'Show Details', 'value': 'show-details'}#chekclist options
                        ],
                        value=['show-details'],#value at the beginning
                        style={'font-size': '20px'}#size
                        ),
                    dcc.Graph(id='graph7', figure=fig_age),#we reload the fig
                    
                ]),
                
            ]),

        ])
    ])

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

        filtered_df = df_Species[df_Species['Fatal (Y/N)'] == selected_value]#we make a graph according to the value selected
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


@app.callback(#callback for the graph7
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
