# README.md

This repo controlls a plotly-based dashboard for lab data for the eEDM lab at LBL. 

The dashboard is hosted at:
https://josephmlev.github.io/eedmLabDashboard/

`index.html`:	Dashboard page with Plotly.js charts. Fetches data.json and renders plots with pan/zoom.

`data.json`:	Sensor readings pushed by the Pi (or any test readings)

`pushFakeDataTest.py`:	Example script for pushing data to the repo. Uses fake data for testing. Requires a GitHub token! Currently on JL's labtop for security.

`PiLabDashboardSetupNotes.txt`:	Setup instructions for deploying on the Pi.

For info on deployments see:
https://github.com/josephmlev/eedmLabDashboard/deployments/github-pages
