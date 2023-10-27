import pandas as pd
import plotly.express as px

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