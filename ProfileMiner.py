import instaloader
import json
import os

def extract_profile_data(username):
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    try:
        # Load the profile with the given username
        profile = instaloader.Profile.from_username(loader.context, username)

        # Print some basic profile info
        print(f"Username: {profile.username}")
        print(f"Full Name: {profile.full_name}")
        print(f"Bio: {profile.biography}")
        print(f"Followers: {profile.followers}")
        print(f"Following: {profile.followees}")
        print(f"Number of Posts: {profile.mediacount}")

        # Download profile picture (optional)
        loader.download_profile(profile.username, profile_pic_only=True)

        # Download the most recent posts (optional)
        for post in profile.get_posts():
            loader.download_post(post, target=f"{profile.username}_posts")

        # Download highlights (optional)
        download_highlights(profile)

        # Save profile data to a JSON file (optional)
        save_profile_data(profile)

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile with username '{username}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_highlights(profile):
    try:
        # Create a directory for saving highlights
        highlight_dir = f"{profile.username}_highlights"
        if not os.path.exists(highlight_dir):
            os.makedirs(highlight_dir)

        # Download highlights
        for highlight in profile.get_highlights():
            for item in highlight.get_items():
                loader.download_storyitem(item, target=highlight_dir)

    except Exception as e:
        print(f"Error while downloading highlights: {e}")

def save_profile_data(profile):
    try:
        with open(f"{profile.username}_profile_data.json", "w", encoding="utf-8") as file:
            data = {
                "Username": profile.username,
                "Full Name": profile.full_name,
                "Bio": profile.biography,
                "Followers": profile.followers,
                "Following": profile.followees,
                "Number of Posts": profile.mediacount
            }
            json.dump(data, file, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Error while saving profile data: {e}")

if __name__ == "__main__":
    # Take user input for Instagram username
    username = input("Enter the Instagram username: ")
    extract_profile_data(username)
