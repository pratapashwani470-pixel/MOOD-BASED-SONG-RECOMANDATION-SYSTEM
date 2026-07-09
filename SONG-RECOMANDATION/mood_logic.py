import random
import pylast

#  apna Last.fm API key/secret yahan daalo
API_KEY = "0eb25d61da4ca4c80ab82274372c9a99"
API_SECRET = "2ed4159bc29bab3fb9e4759656dde27b"

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

last_recommended = {}

def detect_mood(text):
    text = text.lower()
    if "happy" in text or "joy" in text:
        return "happy"
    elif "sad" in text or "cry" in text:
        return "sad"
    elif "love" in text or "romantic" in text:
        return "romantic"
    elif "party" in text or "dance" in text:
        return "party"
    elif "gym" in text or "workout" in text:
        return "workout"
    else:
        return "neutral"

def recommend_songs(mood, language_choice):
    artist_map = {
        "happy": {
            "english": "Ed Sheeran", "hindi": "Arijit Singh",
            "punjabi": "Diljit Dosanjh", "tamil": "Anirudh Ravichander", "bhojpuri": "Khesari Lal Yadav"
        },
        "sad": {
            "english": "Adele", "hindi": "Arijit Singh",
            "punjabi": "Amrinder Gill", "tamil": "Sid Sriram", "bhojpuri": "Pawan Singh"
        },
        "romantic": {
            "english": "Taylor Swift", "hindi": "Arijit Singh",
            "punjabi": "Jass Manak", "tamil": "Haricharan", "bhojpuri": "Ritesh Pandey"
        },
        "party": {
            "english": "Bruno Mars", "hindi": "Badshah",
            "punjabi": "AP Dhillon", "tamil": "Yuvan Shankar Raja", "bhojpuri": "Neelkamal Singh"
        },
        "workout": {
            "english": "Imagine Dragons", "hindi": "Sukhwinder Singh",
            "punjabi": "Sidhu Moosewala", "tamil": "Anirudh Ravichander", "bhojpuri": "Khesari Lal Yadav"
        },
        "neutral": {
            "english": "Coldplay", "hindi": "Pritam",
            "punjabi": "Ammy Virk", "tamil": "Ilaiyaraaja", "bhojpuri": "Ritesh Pandey"
        }
    }

    artist_name = artist_map.get(mood, {}).get(language_choice, "Coldplay")
    print(f"DEBUG: Mood={mood}, Language={language_choice}, Artist={artist_name}")

    artist = network.get_artist(artist_name)
    top_songs = artist.get_top_tracks(limit=20)

    all_songs = [song.item.title for song in top_songs]
    random.seed()  # ensure randomness each call
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
