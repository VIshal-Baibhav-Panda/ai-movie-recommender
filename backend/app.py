from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="../templates", static_folder="../static")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


# 🧹 CLEAN TITLE
def clean_title(title):
    return title.lower().replace("movie", "").strip()


# 🎯 GET BEST POSTER (PRO LOGIC)
def get_best_poster(title):
    queries = [
        title,
        title + " movie",
        title.split(":")[0],
        clean_title(title)
    ]

    for q in queries:
        try:
            res = requests.get(
                "https://api.themoviedb.org/3/search/movie",
                params={
                    "api_key": TMDB_API_KEY,
                    "query": q,
                    "include_adult": False
                },
                timeout=5
            )

            data = res.json()

            if data.get("results"):
                # 🔥 choose best match by popularity
                best = max(data["results"], key=lambda x: x.get("popularity", 0))

                if best.get("poster_path"):
                    return f"https://image.tmdb.org/t/p/w500{best['poster_path']}"

        except:
            continue

    return ""  # fallback


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/overview")
def overview():
    return render_template("overview.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    movie = data.get("movie")

    try:
        # 🤖 AI CALL
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
Give 5 REAL popular movies similar to '{movie}'.

Format EXACTLY:
Movie Name - short 2 line description

Rules:
- Only real movies
- No random words
- No numbering
- No extra text
"""
                    }
                ]
            },
            timeout=10
        )

        data = response.json()
        raw_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        raw_text = raw_text.replace("\n\n", "\n").strip()
        lines = raw_text.split("\n")

        movies = []

        for line in lines:
            if "-" in line:
                title, desc = line.split("-", 1)

                title = title.strip()
                desc = desc.strip()

                # 🎬 GET POSTER (PRO MATCHING)
                poster = get_best_poster(title)

                movies.append({
                    "title": title,
                    "desc": desc,
                    "poster": poster
                })

        # 🛟 fallback if AI fails
        if len(movies) == 0:
            movies = [
                {
                    "title": "Interstellar",
                    "desc": "A team travels through space to save humanity.",
                    "poster": get_best_poster("Interstellar")
                }
            ]

        return jsonify({"movies": movies})

    except Exception as e:
        print("🔥 ERROR:", e)

        return jsonify({
            "movies": [
                {
                    "title": "Inception",
                    "desc": "A thief enters dreams to steal secrets.",
                    "poster": get_best_poster("Inception")
                }
            ]
        })
    
    


if __name__ == "__main__":
    app.run(debug=True)

    