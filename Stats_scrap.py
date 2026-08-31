import statsapi
import json



games = statsapi.schedule(start_date="2026-06-01", end_date = "2026-06-1")
print(games['venue_id'])