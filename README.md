# fitbit-strava-weight-sync

Syncer of weight from Fitbit Aria scale to Strava profile

I created this due to owning the Fitbit Aria scale, which will record your weight automatically into your fitbit profile. The script will automatically copy the recorded weights into your strava profile, which is useful for intervals.icu tracking, which uses that as the source of your weight.

To use it, you will need to set up an API application on both Fitbit and Strava and populate the relevant credentials into python/server_creds.json.  You will also need to configure Fitbit to see the script as a webhook / subscription endpoint and register it to be triggered when body measurements change.
