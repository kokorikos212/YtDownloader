from pytube import Playlist, YouTube
import pytube as yt
import subprocess
import os 
import pandas as pd
import re 
import sqlite3 
import sys

class Downloader:
    def __init__(self, output_directory):
        
        self.output_directory = output_directory 
    
    def __repr__(self):
        print(f"output_directory given = {self.output_directory}")

    
    def sanitize_filename(self, filename):
        # Replace or remove invalid characters
        sanitized_filename = re.sub(r'[\/:*?"<>|]', '', filename)
        
        # Remove leading dots (hidden files)
        sanitized_filename = sanitized_filename.lstrip('.')
        
        # Ensure the resulting filename is not empty
        if not sanitized_filename:
            sanitized_filename = "invalid_filename"
            
        
        # Trim the filename to a maximum length (255 characters)
        if len(sanitized_filename) > 255:
            sanitized_filename = sanitized_filename[:255]
        
        return sanitized_filename
            

    def identify_link_type(self, link):
        # Check if the link is a valid YouTube URL
        try:
            yt = YouTube(link)
            return "Video"  # It's a video URL
        except:
            pass

        # Check if the link is a valid YouTube playlist URL
        try:
            pl = Playlist(link)
            return "Playlist"  # It's a playlist URL
        except:
            pass

        return "unknown"  # It's neither a video nor a playlist URL
    
    def DOWNLOAD_STARTER(self, links): # checks if the link is a video or a playlist or if we have a textfile and starts the downloading prosses 
        for link in links:
            type_of_link = self. identify_link_type(link)
            if type_of_link == 'Video':
                    try:                   
                        self.download_song_and_create_dataframe(link)                    
                    except Exception as e:  
                        print(e)
                
            elif type_of_link == 'Playlist':
                try:                   
                    self.Download_playlist(link)
                except Exception as e:  
                        print(e)


    def download_song_and_create_dataframe(self, link, progres_bar=0): 
        try:
            # Create a YouTube object
            video = YouTube(link)

            # Get the video details
            title = str(video.title)
            author = str(video.author)
            views = int(video.views)
            length = int(video.length)
            publish_date = str(video.publish_date)
            raiting = video.rating
            publish_date = video.publish_date


            # Download the video as an audio stream (webm format)
            audio_stream = video.streams.filter(only_audio=True).first()
            audio_file = audio_stream.download(output_path=self.output_directory)

            # Save the detail-data of the song-vid
            video_data = (title, author, views, length ,publish_date)
            # Connect to the database
            connection = sqlite3.connect("Downloads_Database.db")
            cursor = connection.cursor()
            # Add the details 
            cursor.execute('''
                INSERT INTO mytable (title, author, views, length ,publish_date) VALUES (?,?,?,?,?)''', video_data)
            connection.commit()
            connection.close()

            # Check the validity of the title as a filename
            valid_filname = self.sanitize_filename(title)
            # Convert the downloaded webm file to MP3 using ffmpeg
            mp3_file = os.path.join(self.output_directory, f"{valid_filname}.mp3")
            os.rename(audio_file, mp3_file)

            print('Song downloaded and converted to MP3 successfully!')
            return 

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return None
    
    def Download_playlist(self, link):
        print("__Download_playlist__")
        # URL of the YouTube playlist you want to download
        playlist_url = str(link)

        # Create a Playlist object
        playlist = Playlist(playlist_url)
        valid_filename = self.sanitize_filename(playlist.title)
        playlist_folder = os.path.join(self.output_directory,valid_filename)
        os.makedirs(playlist_folder, exist_ok=True)

        Song_details_df = []
        # Iterate through the videos in the playlist and download and convert each one to MP3
        for video_url in playlist.video_urls:
            try:
                video = YouTube(video_url)
                video_stream = video.streams.get_audio_only()
                video_info = yt.player_response['videoDetails']                

                # Get the video details
                title = video.title
                author = video.author
                views = video.views
                length = video.length
                publish_date = video.publish_date
                raiting = video.rating
                publish_date = video.publish_date

                # Save the detail-data of the song-vid
                video_data = (title, author, views, length ,publish_date)
                # Connect to the databasef
                connection = sqlite3.connect("Downloads_Database.db")
                cursor = connection.cursor()
                # Add the details 
                cursor.execute('''
                    INSERT INTO mytable(title, author, views, length ,publish_date) VALUES (?,?,?,?,?)''', video_data)
                connection.commit()
                connection.close()

            except:
                pass
            
            # Download the video as an audio stream (webm format)
            audio_file = video_stream.download(output_path= playlist_folder)

            # Convert the downloaded webm file to MP3 using ffmpeg
            valid_filename = self.sanitize_filename(title)
            mp3_file = f"{playlist_folder}/{valid_filename}.mp3"
            subprocess.run(['ffmpeg', '-i', audio_file, mp3_file])

            # Remove the original webm file
            os.remove(audio_file)

        print('Playlist downloaded and converted to MP3 successfully!')
        return Song_details_df
    
    def Download_list_of_playlists(self, file):
        with open(file, "r") as f:
            links = f.readlines()
        for link in links:
            self.Download_playlist(link)
