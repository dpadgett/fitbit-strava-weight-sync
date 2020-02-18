# fitbit-strava-weight-sync
syncer of weight from fitbit aria scale to strava profile.
i created this due to owning the fitbit aria scale, which will record your weight automatically into your fitbit profile.
the script will automatically copy the recorded weights into your strava profile, which is useful for intervals.icu tracking
which uses that as the source of your weight.  to use it, you will need to set up an api application on both fitbit and strava,
and populate the relevant credentials into python/server_creds.json.  you will also need to configure fitbit to see the script
as a webhook / subscription endpoint, and register it to be triggered when the body measurements change.
