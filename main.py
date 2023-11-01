from data_processing import *
from graphs import *
from maps import *
from dashboard import *
from callbacks import *
import dash

def main():
    app = dash.Dash(__name__)                  #create the dash
    shark_data = get_data()
    if shark_data is None: return              #the data has not been downloaded
    
    sharks_df, sharks_activity, sharks_year, sharks_species = filtration_df( shark_data )
    fig_year = byYearGraph(sharks_year)
    fig_activity = byActivityGraph(sharks_activity)
    fig_sx = bySexGraph(sharks_df)
    fig_world = worlGraph(sharks_df)
    fig_hours = hoursGraph(sharks_df)
    fig_time_periods = periodGraph(sharks_df)
    fig_age, shark_sorted_df = ageGraph(sharks_df)
    fig_usa = usaGraph(sharks_df)
    fig_aus = australiaGraph(sharks_df)
    fig_sa = africaGraph(sharks_df)
    
    create_dashboard(app, fig_year, fig_sx, fig_activity, fig_world, fig_hours, fig_time_periods, fig_age)        #setup the dash
    get_callbacks(app, shark_sorted_df, sharks_species, fig_age, fig_usa, fig_aus, fig_sa, fig_world)             #get the callbacks for the dashboard
    
    app.run_server(debug=True) #run the server


if __name__ == "__main__":
    main()