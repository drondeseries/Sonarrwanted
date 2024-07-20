import requests
import datetime
import pytz
import argparse

# Configuration variables
SONARR_URL = 'http://localhost:8989'
SONARR_API_KEY = 'sonarrapikey'
DEFAULT_HOURS = 48

def get_missing_episodes(hours):
    now = datetime.datetime.now(pytz.utc)
    past_hours = now - datetime.timedelta(hours=hours)

    headers = {
        'X-Api-Key': SONARR_API_KEY
    }

    # Fetch all series monitored by Sonarr
    series_response = requests.get(f'{SONARR_URL}/api/v3/series', headers=headers)
    series_response.raise_for_status()
    series_list = series_response.json()

    missing_episodes = []

    for series in series_list:
        # Fetch the episodes for the series
        episodes_response = requests.get(f'{SONARR_URL}/api/v3/episode?seriesId={series["id"]}', headers=headers)
        episodes_response.raise_for_status()
        episodes_list = episodes_response.json()

        for episode in episodes_list:
            # Check if the episode is monitored, has aired, and is not downloaded
            if episode['monitored'] and not episode['hasFile'] and 'airDate' in episode:
                episode_air_date = datetime.datetime.fromisoformat(episode['airDate']).astimezone(pytz.utc)
                if past_hours <= episode_air_date <= now:
                    missing_episodes.append({
                        'series_id': series['id'],
                        'episode_id': episode['id'],
                        'series_title': series['title'],
                        'season': episode['seasonNumber'],
                        'episode': episode['episodeNumber'],
                        'title': episode['title'],
                        'air_date': episode['airDate']
                    })

    return missing_episodes

def search_missing_episodes(missing_episodes):
    headers = {
        'X-Api-Key': SONARR_API_KEY
    }

    for episode in missing_episodes:
        search_payload = {
            'name': 'EpisodeSearch',
            'episodeIds': [episode['episode_id']]
        }
        search_response = requests.post(f'{SONARR_URL}/api/v3/command', json=search_payload, headers=headers)
        search_response.raise_for_status()
        print(f"Search triggered for {episode['series_title']} - S{episode['season']:02}E{episode['episode']:02} - {episode['title']}")

def main(hours):
    missing_episodes = get_missing_episodes(hours)

    if missing_episodes:
        print(f"Missing episodes from the past {hours} hours:")
        for episode in missing_episodes:
            print(f"{episode['series_title']} - S{episode['season']:02}E{episode['episode']:02} - {episode['title']} (Aired: {episode['air_date']})")
        
        search_missing_episodes(missing_episodes)
    else:
        print(f"No missing episodes from the past {hours} hours.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and search for missing episodes in Sonarr.")
    parser.add_argument('--hours', type=int, default=DEFAULT_HOURS, help="Number of hours to look back for missing episodes")
    args = parser.parse_args()
    main(args.hours)
