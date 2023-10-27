from data_processing import clean_time, categorize_time, px, pd

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
                    )#visual modification : colors, legend,...
    fig.update_traces(
    line_color='rgb(102,197,204)',
    hovertemplate='Year: %{x}<br>Number: %{y}'
    )#visual modification : colors, legend,...
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
                        )#visual modification : colors, legend,...
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


def hoursGraph(df):
    shark_n = df.copy()
    shark_n.dropna(subset=['Time'], inplace=True)

    # Set the accepted time periods
    time_periods = ["evening", "morning", "night", "afternoon"]

    # Apply the clean_time sorting function 
    shark_n['Time'] = shark_n['Time'].apply(clean_time)


    shark_n['Time'] = shark_n['Time'].str.replace(r'^(.*?)(\d{2})$', r'\2', regex=True)  # If there is some text with an hour in it, only keep the hour
    shark_n = shark_n[shark_n['Time'].isin(time_periods) | (shark_n['Time'].str.isdigit() )] # Drop the rows with incorrect data

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
                            )#visual modification : colors, legend,...
    )
    return fig


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