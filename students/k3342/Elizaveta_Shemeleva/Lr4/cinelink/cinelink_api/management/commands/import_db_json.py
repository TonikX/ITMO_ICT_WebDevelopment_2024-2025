import json
from datetime import datetime

from django.core.management.base import BaseCommand

from cinelink_api.models import Movie, User, List, ListMovie, Rating, Friend


def parse_year(year):
    if year and isinstance(year, str) and year.isdigit():
        return int(year)
    return None


def parse_timestamp(timestamp):
    try:
        return datetime.fromisoformat(timestamp)
    except ValueError:
        return None


class Command(BaseCommand):
    help = "Import data from db.json"

    def handle(self, *args, **kwargs):
        with open("db.json", "r") as file:
            data = json.load(file)

        # Import movies
        self.stdout.write("Importing movies...")
        for movie in data["movies"]:
            try:
                if not movie.get("id") or movie.get("rating") is None:
                    self.stdout.write(f"Skipping movie with missing ID or rating: {movie['title']}")
                    continue

                Movie.objects.update_or_create(
                    id=movie["id"],  # IMDb ID as primary key
                    defaults={
                        "title": movie["title"],
                        "poster_url": movie.get("poster"),
                        "year": parse_year(movie.get("year")),
                        "genres": ", ".join(movie.get("genres", [])),
                        "rating": movie["rating"],
                    },
                )
            except Exception as e:
                self.stderr.write(f"Error importing movie {movie.get('title', 'unknown')}: {e}")

        # Import users
        self.stdout.write("Importing users...")
        for user in data["users"]:
            try:
                user_obj, created = User.objects.update_or_create(
                    email=user["email"],
                    defaults={"avatar_url": user.get("avatar")},
                )

                # Create friendships
                for friend_id in user.get("friends", []):
                    friend_user = User.objects.filter(email=friend_id).first()
                    if friend_user:
                        Friend.objects.get_or_create(user=user_obj, friend=friend_user)

                # Add favorite movies to user's "Favorites" list
                for favorite_id in user.get("favorites", []):
                    movie = Movie.objects.filter(id=favorite_id).first()
                    if not movie:
                        self.stdout.write(f"Skipping invalid favorite movie ID: {favorite_id}")
                        continue
                    favorite_list, _ = List.objects.get_or_create(user=user_obj, name="Favorites")
                    ListMovie.objects.get_or_create(list=favorite_list, movie=movie)
            except Exception as e:
                self.stderr.write(f"Error importing user {user.get('email', 'unknown')}: {e}")

        # Import ratings
        self.stdout.write("Importing ratings...")
        for rating in data["ratings"]:
            try:
                user = User.objects.filter(email=rating["userId"]).first()
                movie = Movie.objects.filter(id=rating["movieId"]).first()
                if user and movie:
                    Rating.objects.get_or_create(
                        user=user,
                        movie=movie,
                        defaults={
                            "rating": rating["rate"],
                            "created_at": parse_timestamp(rating["timestamp"]),
                        },
                    )
            except Exception as e:
                self.stderr.write(f"Error importing rating: {e}")

        self.stdout.write("Data import completed successfully!")
