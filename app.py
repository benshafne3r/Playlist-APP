from flask import Flask, request, jsonify, render_template
import requests
import base64

app = Flask(__name__)

# Spotify API credentials
client_id = "c4c047045f094929a6ab31117bb1c16c"
client_secret = "c4c047045f094929a6ab31117bb1c16c"

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

# Existing search function to find a song in playlists
def search_song_in_playlists(song_name, artist_name):
    token = get_spotify_token()
    if not token:
        return []

    # Your existing code for searching through categories, playlists, and tracks goes here
    # Modify it slightly to return results as a list of dictionaries rather than printing directly
    results = []
    # ... existing code to fetch categories, playlists, and tracks ...
    # If song is found in a playlist, add it to results list
    # Example entry for found song:
    # results.append({"playlistName": playlist_name, "category": category_name})
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search():
    artist = request.args.get('artist')
    track = request.args.get('track')

    if not artist or not track:
        return jsonify({"error": "Both artist and track are required"}), 400

    # Call the function to search for the song in playlists
    results = search_song_in_playlists(track, artist)

    # Return JSON response with search results
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
