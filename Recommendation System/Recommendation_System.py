movies = [
    {"title": "Avengers", "genre": "Action", "rating": 9},
    {"title": "Iron Man", "genre": "Action", "rating": 8},
    {"title": "John Wick", "genre": "Action", "rating": 9},
    {"title": "Deadpool", "genre": "Comedy", "rating": 8},
    {"title": "The Hangover", "genre": "Comedy", "rating": 7},
    {"title": "Superbad", "genre": "Comedy", "rating": 7},
    {"title": "Titanic", "genre": "Romance", "rating": 9},
    {"title": "The Notebook", "genre": "Romance", "rating": 8}
]

user_input = input("Enter preferred genres (comma separated): ")
preferences = [x.strip().lower() for x in user_input.split(",")]

recommendations = []

for movie in movies:
    if movie["genre"].lower() in preferences:
        recommendations.append(movie)

recommendations.sort(key=lambda x: x["rating"], reverse=True)

print("\nRecommended Movies:")

for movie in recommendations:
    print(f"{movie['title']} (Rating: {movie['rating']})")