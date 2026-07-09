from flask import Flask, request, jsonify, render_template
import random
import pylast

app = Flask(__name__)

# Last.fm API credentials
API_KEY = "0eb25d61da4ca4c80ab82274372c9a99"
API_SECRET = "2ed4159bc29bab3fb9e4759656dde27b"
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

last_recommended = {}

# Mood detection logic
def detect_mood(text):
    text = text.lower()
    if any(word in text for word in ["happy", "joy", "excited", "awesome", "great", "fun", "cheerful"]):
        return "happy"
    elif any(word in text for word in ["sad", "cry", "depressed", "lonely", "broken", "upset", "hurt"]):
        return "sad"
    elif any(word in text for word in ["love", "romantic", "affection", "crush", "sweetheart", "heart"]):
        return "romantic"
    elif any(word in text for word in ["party", "dance", "club", "celebration", "dj", "festival"]):
        return "party"
    elif any(word in text for word in ["gym", "workout", "exercise", "training", "fitness", "running"]):
        return "workout"
    else:
        return "neutral"

# Hybrid tag-based recommendation
def recommend_songs(mood, language_choice):
    try:
        # 1. Mood + language tag
        combined_tag = f"{mood} {language_choice}"
        tag = network.get_tag(combined_tag)
        top_tracks = tag.get_top_tracks(limit=20)

        # 2. Fallback to language tag
        if not top_tracks:
            tag = network.get_tag(language_choice)
            top_tracks = tag.get_top_tracks(limit=20)

        # 3. Fallback to mood tag
        if not top_tracks:
            tag = network.get_tag(mood)
            top_tracks = tag.get_top_tracks(limit=20)

        all_songs = [track.item.title for track in top_tracks]
        random.shuffle(all_songs)

        key = f"{mood}_{language_choice}"
        prev_songs = last_recommended.get(key, [])
        new_songs = [s for s in all_songs if s not in prev_songs]

        if len(new_songs) < 5:
            prev_songs = []
            new_songs = all_songs

        final_songs = new_songs[:5]
        last_recommended[key] = prev_songs + final_songs

        return final_songs
    except Exception as e:
        print("Error fetching songs:", e)
        return ["No songs found"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    language = data.get('language')
    text = data.get('text')
    mood = detect_mood(text)
    songs = recommend_songs(mood, language)
    return jsonify({"mood": mood, "songs": songs})

if __name__ == '__main__':
    app.run(debug=True)
