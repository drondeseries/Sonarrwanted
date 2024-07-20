# Sonarr Missing Episodes Checker

This script checks for missing episodes in Sonarr for the past specified number of hours and triggers an automatic search for those episodes.

## Prerequisites

- Python 3.x
- `requests` library
- `pytz` library

You can install the required libraries using:

```bash
pip install requests pytz
```

## Configuration
Update the following configuration variables in the script with your Sonarr URL and API key:

# Configuration variables
```
SONARR_URL = 'http://localhost:8989'
SONARR_API_KEY = 'your_sonarr_api_key'
DEFAULT_HOURS = 48  # Default number of hours to look back
```

## Usage
Run the script using Python, specifying the number of hours to look back. If no hours are specified, the script will default to 48 hours.
```bash
python check_missing_episodes.py --hours <number_of_hours>
```

Example: 
```
python check_missing_episodes.py --hours 24
```

This will check for missing episodes in the past 24 hours and trigger a search for those episodes in Sonarr.

### Script Details
The script fetches all monitored series and their episodes from Sonarr.
It checks if each episode has aired in the specified time frame and whether it is missing (not downloaded).
If an episode is missing, it triggers an automatic search for the episode in Sonarr using the Episode Search command.

Example Output
```
Missing episodes from the past 24 hours:
Series Title - S01E01 - Episode Title (Aired: 2024-07-19)
Search triggered for Series Title - S01E01 - Episode Title
```
If there are no missing episodes in the specified time frame, the script will output:
```
No missing episodes from the past 24 hours.
```
### License
This project is licensed under the MIT License.




