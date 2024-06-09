import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Set up your Warpcast API endpoint and authorization token
WARPCAST_API_ENDPOINT = "https://api.warpcast.com"  # Replace with the actual Warpcast API endpoint
WARPCAST_API_TOKEN = os.getenv('WARPCAST_API_TOKEN')  # Ensure you have this environment variable set

# Function to get likes, comments, and recasts for a specific cast
def get_cast_interactions(cast_id):
    headers = {
        'Authorization': f'Bearer {WARPCAST_API_TOKEN}'
    }
    
    # Replace the URLs with the actual API endpoints for likes, comments, and recasts
    likes_url = f"{WARPCAST_API_ENDPOINT}/casts/{cast_id}/likes"
    comments_url = f"{WARPCAST_API_ENDPOINT}/casts/{cast_id}/comments"
    recasts_url = f"{WARPCAST_API_ENDPOINT}/casts/{cast_id}/recasts"

    likes_response = requests.get(likes_url, headers=headers)
    comments_response = requests.get(comments_url, headers=headers)
    recasts_response = requests.get(recasts_url, headers=headers)

    likes = likes_response.json().get('data', [])
    comments = comments_response.json().get('data', [])
    recasts = recasts_response.json().get('data', [])

    return likes, comments, recasts

# Function to save the interactions data to an Excel file
def save_to_excel(cast_id, likes, comments, recasts):
    likes_df = pd.DataFrame(likes, columns=['user_id', 'username'])
    comments_df = pd.DataFrame(comments, columns=['user_id', 'username', 'comment'])
    recasts_df = pd.DataFrame(recasts, columns=['user_id', 'username'])

    with pd.ExcelWriter(f'cast_{cast_id}_interactions.xlsx') as writer:
        likes_df.to_excel(writer, sheet_name='Likes', index=False)
        comments_df.to_excel(writer, sheet_name='Comments', index=False)
        recasts_df.to_excel(writer, sheet_name='Recasts', index=False)

    print(f"Data saved to cast_{cast_id}_interactions.xlsx")

if __name__ == '__main__':
    cast_id = input("Enter the cast ID: ")
    likes, comments, recasts = get_cast_interactions(cast_id)
    save_to_excel(cast_id, likes, comments, recasts)
