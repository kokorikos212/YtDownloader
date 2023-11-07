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

    # def Save_video_data(self, video_data): # The apropriate data format: video_data = (title, author, views, length ,publish_date, link)
    #             """Save the detail-data of the song-vid."""
    #             connection = sqlite3.connect("YT_database.db")
    #             cursor = connection.cursor()
    #             # Append the name of the author into the Artists table 
    #             author = video_data[1] 
    #             cursor.execute('''
    #                 INSERT INTO Artists (name) VALUES (?)''', (author,)) 
    #             # Add the details of the video-song into the Songs table
    #             cursor.execute('''
    #                 INSERT INTO Songs (title, author,views, length ,publish_date, link) VALUES (?,?,?,?,?,?)''', video_data)
    #             connection.commit()
    #             connection.close()


    import sqlite3

    def Save_video_data(self, video_data):
        """Save the detail-data of the song-vid."""
        connection = sqlite3.connect("YT_database.db")
        cursor = connection.cursor()
        
        # Extract the artist's name from video_data
        author = video_data[1]

        # Check if the artist already exists in the Artists table
        cursor.execute("SELECT artist_id FROM Artists WHERE name = ?", (author,))
        existing_artist = cursor.fetchone()

        if existing_artist:
            # Artist already exists, retrieve their ID
            artist_id = existing_artist[0]
        else:
            # Artist doesn't exist, insert their name and get the newly generated ID
            cursor.execute("INSERT INTO Artists (name) VALUES (?)", (author,))
            connection.commit()
            artist_id = cursor.lastrowid

        # Adjust the video_data tuple to match the number of placeholders
        adjusted_video_data = (video_data[0], artist_id, video_data[2], video_data[3], video_data[4], video_data[5])

        # Add the details of the video-song into the Songs table
        cursor.execute('''
            INSERT INTO Songs (title, author, views, length, publish_date, link) VALUES (?,?,?,?,?,?)''', adjusted_video_data)
        connection.commit()
        connection.close()


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

            # Save the detail-data of the song-vid.
            video_data = (title, author, views, length ,publish_date, link)
            self.Save_video_data(video_data)

            # Download the video as an audio stream (webm format)
            audio_stream = video.streams.filter(only_audio=True).first()
            audio_file = audio_stream.download(output_path=self.output_directory)

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
        playlist_title = playlist.title
        valid_filename = self.sanitize_filename(playlist_title)
        playlist_folder = os.path.join(self.output_directory,valid_filename)
        os.makedirs(playlist_folder, exist_ok=True)

        Song_details_df = []
        # Iterate through the videos in the playlist and download and convert each one to MP3
        for video_url in playlist.video_urls:
            try:
                video = YouTube(video_url)
                video_stream = video.streams.get_audio_only()
                # video_info = yt.player_response['videoDetails']                

                # Get the video details
                title = video.title
                author = video.author
                views = video.views
                length = video.length
                publish_date = video.publish_date
                raiting = video.rating
                publish_date = video.publish_date

                video_data = (title, author, views, length ,publish_date, link)
                # SAve the video-song details in the database
                self.Save_video_data(video_data ) 

            except Exception as e:
                print(e)
                return 
            
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
