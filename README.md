# strava-exercise-route-visualizer
Visualizes users exercise routes on a map.

## Usage
On first use, create an app to strava ( https://www.strava.com/settings/api ).
When done with that, copy the `.env.example` file and rename the copied file into `.env`. Add your client secret and client id into the `.env` file. Leave redirect_uri as is.

After that, you can get all your exercises by running the `authenticate.py` file, and going to http://localhost:8080/authorize . It redirects you to strava page, where you must accept in order to allow getting your data. After that, you can stop the server.

Then to fetch your activity summaries, run `fetch_activities.py`. It gets all your summaries and saves them. Finally, create and open the visualization by running `plot_routes.py`. When you have new activities, just repeat the fetching and plotting steps again.

