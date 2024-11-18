import requests
import base64

# Your Spotify API credentials
CLIENT_ID = 'c4c047045f094929a6ab31117bb1c16c'
CLIENT_SECRET = 'ec3dca0513a3447b91964b6fc57c13a4'

# Base URL for Spotify API
API_URL = 'https://api.spotify.com/v1/'

# Step 1: Get Access Token using Client Credentials Flow
def get_access_token():
    client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_credentials_b64 = base64.b64encode(client_credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {client_credentials_b64}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        raise Exception(f"Error retrieving access token: {response.status_code} - {response.text}")

# Step 2: Search for items (tracks, albums, artists, playlists, etc.)
def search_items(query, access_token, search_type="track"):
    search_url = f"{API_URL}search?q={query}&type={search_type}&limit=5"
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        search_results = response.json()
        return search_results
    else:
        raise Exception(f"Error searching for items: {response.status_code} - {response.text}")

# Step 3: Search for playlists containing the track by name, filter for editorial playlists excluding Radio
def get_editorial_playlists_for_track(track_name, access_token):
    playlists_url = f"{API_URL}search?q={track_name}&type=playlist&limit=5"
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(playlists_url, headers=headers)

    if response.status_code == 200:
        playlists = response.json()
        editorial_playlists = [
            playlist for playlist in playlists['playlists']['items'] 
            if playlist['owner']['id'] == 'spotify' and 'radio' not in playlist['id']
        ]
        return editorial_playlists
    else:
        raise Exception(f"Error retrieving playlists for track: {response.status_code} - {response.text}")

# Main function to execute the workflow
def main():
    search_query = input("Enter the search query (song, album, artist, etc.): ")
    search_type = input("Enter the search type (track, album, artist, playlist, show, episode): ").lower()  # Specify the type

    try:
        access_token = get_access_token()

        # Search for items (tracks, albums, artists, playlists, etc.)
        search_results = search_items(search_query, access_token, search_type)

        if search_type == 'track':
            # If the type is track, display track details and get editorial playlists excluding Radio
            tracks = search_results.get('tracks', {}).get('items', [])
            if tracks:
                print(f"Found tracks matching '{search_query}':")
                for track in tracks:
                    track_name = track['name']
                    track_artist = track['artists'][0]['name']
                    print(f"Track: {track_name} by {track_artist}")

                    # Get Spotify editorial playlists (excluding Radio playlists) the track is in
                    editorial_playlists = get_editorial_playlists_for_track(track_name, access_token)
                    if editorial_playlists:
                        print(f"Spotify Editorial Playlists (excluding Radio) the track is in:")
                        for playlist in editorial_playlists:
                            print(f"- {playlist['name']} (ID: {playlist['id']})")
                    else:
                        print("This track is not in any Spotify editorial playlists.")
            else:
                print("No tracks found for the given search.")
        
        elif search_type == 'album':
            albums = search_results.get('albums', {}).get('items', [])
            if albums:
                print(f"Found albums matching '{search_query}':")
                for album in albums:
                    album_name = album['name']
                    album_artist = album['artists'][0]['name']
                    print(f"Album: {album_name} by {album_artist}")
            else:
                print("No albums found for the given search.")

        elif search_type == 'artist':
            artists = search_results.get('artists', {}).get('items', [])
            if artists:
                print(f"Found artists matching '{search_query}':")
                for artist in artists:
                    artist_name = artist['name']
                    print(f"Artist: {artist_name}")
            else:
                print("No artists found for the given search.")

        elif search_type == 'playlist':
            playlists = search_results.get('playlists', {}).get('items', [])
            if playlists:
                print(f"Found playlists matching '{search_query}':")
                for playlist in playlists:
                    playlist_name = playlist['name']
                    print(f"Playlist: {playlist_name}")
            else:
                print("No playlists found for the given search.")

        elif search_type == 'show':
            shows = search_results.get('shows', {}).get('items', [])
            if shows:
                print(f"Found shows matching '{search_query}':")
                for show in shows:
                    show_name = show['name']
                    print(f"Show: {show_name}")
            else:
                print("No shows found for the given search.")
        
        elif search_type == 'episode':
            episodes = search_results.get('episodes', {}).get('items', [])
            if episodes:
                print(f"Found episodes matching '{search_query}':")
                for episode in episodes:
                    episode_name = episode['name']
                    print(f"Episode: {episode_name}")
            else:
                print("No episodes found for the given search.")
        
        else:
            print(f"Search type '{search_type}' is not supported. Try: track, album, artist, playlist, show, episode.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
