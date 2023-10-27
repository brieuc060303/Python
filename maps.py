import plotly.express as px
import json
import pandas as pd

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
    with open('./ressources/states_australia.geojson', 'r') as file:  # source : https://github.com/rowanhogan/australian-states/blob/master/states.geojson
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
    with open('./ressources/states_south_africa.json', 'r') as file:      # source : https://github.com/fletchjeff/ZA-Census-Data-Explorer/blob/main/assets/za-provinces.topojson converted to geojson
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