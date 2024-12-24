import csv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import time
import logging

api_key='your api key'

youtube=build('youtube','v3',developerKey=api_key)

'''

request=youtube.search().list(part='id,snippet',q='Elon Musk',type='video',maxResults=10,order='rating')

response=request.execute()


for item in response['items']:
    video_id = item['id']['videoId']  # Extract video ID
    title = item['snippet']['title']  # Extract video title
    link = f"https://www.youtube.com/watch?v={video_id}"  # Create full URL
    print(f"Title: {title}\nLink: {link}\n")
    

'''

# Function to get the transcript for a given video ID
def get_video_transcript(video_id):
    try:
        # Fetch transcript using youtube-transcript-api
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        logging.error(f"Error fetching transcript for video {video_id}: {str(e)}")
        return None

# Function to format the transcript as plain text
def format_transcript(transcript):
    formatter = TextFormatter()
    return formatter.format_transcript(transcript)

# Function to search YouTube for videos based on a query
def search_youtube(query, max_results=10):
    try:
        request = youtube.search().list(
            part='id,snippet',
            q=query,  # You can change this query to anything else
            type='video',
            maxResults=max_results,
            order='rating'  # You can change the order as needed
        )
        response = request.execute()
        return response['items']
    except Exception as e:
        logging.error(f"Error searching for videos: {str(e)}")
        return []

# Function to save video details and transcript to CSV
def save_to_csv(video_details):
    # Define the CSV file name
    filename = 'video_transcripts.csv'

    # Open the CSV file in write mode
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(['Video Title', 'Video Link', 'Transcript'])
        
        # Write the video details
        for video in video_details:
            writer.writerow([video['title'], video['link'], video['transcript']])

# Function to process each video and fetch its transcript
def process_video_transcripts(videos):
    video_details = []  # List to store video details and transcripts
    
    for item in videos:
        video_id = item['id']['videoId']  # Extract video ID
        title = item['snippet']['title']  # Extract video title
        link = f"https://www.youtube.com/watch?v={video_id}"  # Create full URL
        
        logging.info(f"Fetching transcript for video: {title}")
        logging.info(f"Video Link: {link}")
        
        # Get the transcript for the video
        transcript = get_video_transcript(video_id)
        
        if transcript:
            formatted_transcript = format_transcript(transcript)
            logging.info(f"Transcript:\n{formatted_transcript}")  # Print the formatted transcript
            video_details.append({'title': title, 'link': link, 'transcript': formatted_transcript})
        else:
            logging.warning(f"Transcript not available for video: {title}")
            video_details.append({'title': title, 'link': link, 'transcript': 'Transcript not available'})
        
        # Optional: Add a small delay to avoid hitting API limits too quickly
        time.sleep(2)

        logging.info("\n" + "="*50 + "\n")
    
    # Save the video details and transcripts to CSV
    save_to_csv(video_details)

# Main Execution Flow
if __name__ == "__main__":
    query = 'Elon Musk'  # Search query, can be changed to anything
    videos = search_youtube(query)  # Fetch videos for the search query
    if videos:
        process_video_transcripts(videos)  # Process each video and fetch its transcript
    else:
        logging.warning("No videos found for the query.")