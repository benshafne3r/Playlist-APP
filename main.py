import requests
import json
import streamlit as st
import base64

st.write("hello")

# Spotify API credentials
CLIENT_ID = 'c4c047045f094929a6ab31117bb1c16c'
CLIENT_SECRET = 'ec3dca0513a3447b91964b6fc57c13a4'

# Encode client credentials
client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

# Get Spotify API token
def get_spotify_token():
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {client_creds_b64}"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(token_url, headers=headers, data=data)
    response_json = response.json()
    return response_json.get("access_token")

# Get Spotify categories
def get_spotify_categories():
    token = get_spotify_token()
    if not token:
        print("Failed to retrieve token.")
        return []

    categories_url = "https://api.spotify.com/v1/browse/categories"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "country": "US",  # Change to desired country code
        "limit": 20       # Set limit of categories to retrieve
    }
    response = requests.get(categories_url, headers=headers, params=params)

    if response.status_code == 200:
        categories_data = response.json().get("categories", {}).get("items", [])
        return [(category['id'], category['name']) for category in categories_data]
    else:
        print(f"Failed to retrieve categories: {response.status_code}")
        return []

# Get playlists for each category with names
def get_playlists_for_category(category_id, token):
    playlists_url = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "country": "US",
        "limit": 10  # Adjust this to the desired number of playlists per category
    }
    response = requests.get(playlists_url, headers=headers, params=params)

    if response.status_code == 200:
        playlists = response.json().get("playlists", {}).get("items", [])
        return [{"id": playlist['id'], "name": playlist['name']} for playlist in playlists]
    else:
        print(f"Failed to retrieve playlists for category {category_id}: {response.status_code}")
        return []

# Get all tracks from a playlist
def get_tracks_from_playlist(playlist_id, token):
    tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "limit": 100  # Adjust to retrieve more or fewer tracks per playlist
    }
    response = requests.get(tracks_url, headers=headers, params=params)

    if response.status_code == 200:
        tracks = response.json().get("items", [])
        return [
            {
                "track_id": track['track']['id'],
                "track_name": track['track']['name'],
                "artist_name": track['track']['artists'][0]['name']
            }
            for track in tracks if track['track']
        ]
    else:
        print(f"Failed to retrieve tracks for playlist {playlist_id}: {response.status_code}")
        return []

# Search for a song by name and artist across playlists, displaying playlist names
def search_song_in_playlists(song_name, artist_name):
    token = get_spotify_token()
    if not token:
        print("Failed to retrieve token.")
        return

    categories = get_spotify_categories()
    if not categories:
        print("No categories found.")
        return

    song_found = False
    for category_id, category_name in categories:
        print(f"\nSearching in category: {category_name}")

        playlists = get_playlists_for_category(category_id, token)
        for playlist in playlists:
            playlist_id = playlist["id"]
            playlist_name = playlist["name"]
            tracks = get_tracks_from_playlist(playlist_id, token)
            for track in tracks:
                # Check if the track name and artist match the search criteria
                if song_name.lower() == track["track_name"].lower() and artist_name.lower() == track["artist_name"].lower():
                    print(f"Found '{song_name}' by {artist_name} in playlist '{playlist_name}' (ID: {playlist_id})")
                    song_found = True

    if not song_found:
        print(f"'{song_name}' by {artist_name} not found in any playlist.")

# Run the function to search for a specific song
search_song_in_playlists("HOT TO GO!", "Chappell Roan")