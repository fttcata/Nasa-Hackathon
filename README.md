# Nasa-Hackathon

## We are going to win this

Website: https://weatherwary-earth.l.ink/
- interactive map --> Google earth/maps API --> pin-point location input for research
- search tool for location
- search tool for time windows 

DataFlow 
- website/Google maps API - user uses maps to put pin - coordinates sent as request to Meomatics API
- Mateomatics - responds with data about query
- if date is outside of meomatics limits(15 days in advance) - then we use our own algorithm to predict weather

- we will have a python file that the data is passed into and it outputs the weather prediction for the website to display

