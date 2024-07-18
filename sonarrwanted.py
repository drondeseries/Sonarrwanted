import requests
import logging
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# Sonarr API configuration
SONARR_URL = 'http://localhost:8989'
SONARR_API_KEY = '.........'

# Configure logging
logging.basicConfig(filename='sonarr_recent_episodes.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize colorama
init(autoreset=True)

timeframes = [15, 30, 45, 60, 90, 120, 150, 200, 260]

def trigger_search_for_episode(episode_id):
    try:
        response = requests.post(f'{SONARR_URL}/api/v3/command',
                                 headers={'X-Api-Key': SONARR_API_KEY},
                                 json={"name": "EpisodeSearch", "episodeIds": [episode_id]})
        response.raise_for_status()
        logging.info(f"Triggered search for episode ID: {episode_id}")
    except Exception as e:
        logging.error(f"Error triggering search for episode ID {episode_id}: {e}")

def get_recent_episodes(timeframe_minutes):
    try:
        timeframe = datetime.utcnow() - timedelta(minutes=timeframe_minutes)
        timeframe_str = timeframe.isoformat() + 'Z'

        series_response = requests.get(f'{SONARR_URL}/api/v3/series',
                                       headers={'X-Api-Key': SONARR_API_KEY})
        series_response.raise_for_status()
        series_list = series_response.json()

        recent_episodes = []

        for series in series_list:
            series_id = series['id']
            episodes_response = requests.get(f'{SONARR_URL}/api/v3/episode',
                                             headers={'X-Api-Key': SONARR_API_KEY},
                                             params={'seriesId': series_id})
            episodes_response.raise_for_status()
            episodes = episodes_response.json()

            for episode in episodes:
                air_date_utc = episode.get('airDateUtc')
                if air_date_utc and timeframe_str <= air_date_utc <= datetime.utcnow().isoformat() + 'Z':
                    recent_episodes.append(episode)

        if not recent_episodes:
            logging.info(f'No episodes found in the last {timeframe_minutes} minutes.')
            return

        for episode in recent_episodes:
            series_id = episode['seriesId']
            series_response = requests.get(f'{SONARR_URL}/api/v3/series/{series_id}',
                                           headers={'X-Api-Key': SONARR_API_KEY})
            series_response.raise_for_status()
            series = series_response.json()

            series_title = series['title']
            episode_title = episode['title']
            season_number = episode['seasonNumber']
            episode_number = episode['episodeNumber']
            air_date = episode['airDate']
            episode_id = episode['id']

            # Colorize the output
            colored_series_title = f"{Fore.CYAN}{series_title}{Style.RESET_ALL}"
            colored_episode_title = f"{Fore.MAGENTA}{episode_title}{Style.RESET_ALL}"
            colored_season_number = f"{Fore.YELLOW}Season: {season_number}{Style.RESET_ALL}"
            colored_episode_number = f"{Fore.GREEN}Episode: {episode_number}{Style.RESET_ALL}"

            logging.info(f"Series: {colored_series_title}, Episode: {colored_episode_title}, {colored_season_number}, {colored_episode_number}, Air Date: {air_date}")

            trigger_search_for_episode(episode_id)

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    for minutes in timeframes:
        get_recent_episodes(minutes)
