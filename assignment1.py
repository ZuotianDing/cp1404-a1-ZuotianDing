"""
CP1404/CP5632 Assignment 1 – Albums Archive 1.0
Name: Ding Zuotian
Date: 20/7/2026
"""

import csv
import random

FILE_NAME = "albums.csv"


def main():
    """Main program loop for the Albums Archive tracker."""
    print("Albums Archive 1.0 - by Your Name")

    # Load albums from file
    albums = load_albums(FILE_NAME)

    # Menu loop
    choice = ""
    while choice != "Q":
        print("\nMenu:")
        print("D - Display all albums")
        print("R - Recommend a random album")
        print("A - Add a new album")
        print("M - Mark an album as completed")
        print("Q - Quit")
        choice = input(">>> ").strip().upper()

        if choice == "D":
            display_albums(albums)
        elif choice == "R":
            recommend_album(albums)
        elif choice == "A":
            add_album(albums)
        elif choice == "M":
            mark_album_completed(albums)
        elif choice == "Q":
            save_albums(FILE_NAME, albums)
            print(f"{len(albums)} albums saved to {FILE_NAME}")
            print("Have a nice day :)")
        else:
            print("Invalid menu choice")


def load_albums(file_name):
    """Load albums from a CSV file into a list of lists. Handles missing file error."""
    albums = []
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Skip empty lines
                    row[2] = int(row[2])  # Convert year to integer
                    albums.append(row)
        print(f"{len(albums)} albums loaded from {file_name}")
    except FileNotFoundError:
        print(f"Error, {file_name} not found!")
        print(f"0 albums loaded from {file_name}")
    return albums


def save_albums(file_name, albums):
    """Save the list of albums back to the CSV file, sorted by status, artist, then title."""
    # Matches the exact save behavior shown in the last screenshot
    albums.sort(key=lambda x: (x[3], x[1], x[0]))
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(albums)


def display_albums(albums):
    """Sort and neatly display the list of all albums."""
    if not albums:
        print("No albums!")
        return

    # Sort primarily by artist, then break ties by album title
    albums.sort(key=lambda x: (x[1], x[0]))

    # Dynamic column widths calculation for clean formatting alignment
    max_title_len = max(len(album[0]) for album in albums)
    max_artist_len = max(len(album[1]) for album in albums)

    required_count = 0
    for i, album in enumerate(albums, 1):  # Indexes start from 1
        title, artist, year, status = album
        if status == "r":
            marker = "*"
            required_count += 1
        else:
            marker = " "
        print(f"{marker}{i}. {title:<{max_title_len}} by {artist:<{max_artist_len}} {year}")

    print(f"{len(albums)} albums in archive. You still want to listen to {required_count} albums.")


def recommend_album(albums):
    """Recommend a random uncompleted (required) album."""
    required_albums = [album for album in albums if album[3] == "r"]
    if not required_albums:
        print("No albums left to listen to!")
        return

    print("Not sure what to listen to next?")
    chosen = random.choice(required_albums)
    print(f"How about... {chosen[0]} by {chosen[1]}?")


def add_album(albums):
    """Prompt user for details and add a new uncompleted album with robust error checking."""
    title = input_non_empty("Title: ")
    artist = input_non_empty("Artist: ")

    while True:
        try:
            year = int(input("Year: "))
            if year > 0:
                break
            print("Number must be > 0")
        except ValueError:
            print("Invalid input; enter a valid number")

    albums.append([title, artist, year, "r"])
    print(f"{title} by {artist} ({year}) added to Albums Archive.")


def mark_album_completed(albums):
    """Prompt user to select a required album and mark it as completed."""
    required_albums = [album for album in albums if album[3] == "r"]
    if not required_albums:
        print("No required albums.")
        return

    display_albums(albums)
    print("Enter the number of an album to mark as completed")

    while True:
        try:
            choice = int(input(">>> "))
            if choice <= 0:
                print("Number must be > 0")
            elif choice > len(albums):
                print("Invalid album number")
            elif albums[choice - 1][3] == "c":
                print(f"You have already completed {albums[choice - 1][0]}")
                break
            else:
                albums[choice - 1][3] = "c"
                print(f"{albums[choice - 1][0]} by {albums[choice - 1][1]} completed!")
                break
        except ValueError:
            print("Invalid input; enter a valid number")


def input_non_empty(prompt):
    """Prompt user until a non-empty string is provided."""
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("Input cannot be blank")


if __name__ == "__main__":
    main()