import requests
import time
import csv 
import configparser
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials


def get_config():
    # Spotify API credentials
    config = configparser.ConfigParser()
    config.sections()
    config.read("config.ini")
    for key in config['Spotify']:  
        print(key)
    client_id = config['Spotify']['client_id']
    print("client_id: " + client_id)
    if(client_id == ""):
        print("no spotify client id in config file")
    client_secret = config['Spotify']['client_secret']    
    print("client_secret: " + client_secret)
    if(client_secret == ""):
        print("no spotify client secret in config file")

    # Authenticate with Spotify API
    global sp
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    

def get_track_info(song_name, artist):
    print("client_id " + str(getattr(SpotifyClientCredentials, "client_id")))
    print("client_secret " + str(getattr(SpotifyClientCredentials, "client_secret")))
    SpotifyClientCredentials.client_secret
    # Search for the track
    track_results = sp.search(q=f"track:{song_name} artist:{artist}", limit=1, type='track')
    #print(f"Track results:  {track_results}")

    if track_results['tracks']['items']:
        # Extract track information
        track = track_results['tracks']['items'][0]
        #print(f"Track:  {track}")
        track_info = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'duration': track["duration_ms"],
            'preview_url': track['preview_url']
        }
        #print(f"Track info:  {track_info}")
        try:
            print("Song Details:")
            print(f"Artist: {track_info['artist']}")
            print(f"Track: {track_info['name']}")                
            print(f"Album: {track_info['album']}")
            minutes = (int(track_info['duration'])/1000) // 60
            seconds = (int(track_info['duration'])/1000) % 60

            if(len(str(int(seconds))) == 1):
                track_info['simpleduration'] = "00:0" + str(int(minutes)) + ":0" + str(int(seconds))
            else: 
                track_info['simpleduration'] = "00:0" + str(int(minutes)) + ":" + str(int(seconds))
            
            outputdata = [
                [track_info['name'], track_info['artist'], track_info['album'],  track_info['release_date'], track_info['simpleduration']]
            ]
            print(outputdata)
            write_to_csv(outputfile,outputdata)
        except KeyError:    
            print(KeyError)      
            outputdata = [
                [track, artist, KeyError]
            ]
            write_to_csv(outputfile,outputdata)

    else:
        return None

# Example usage
# Read in the CSV file
def read_csv_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            # Remove newline character
            line = line.strip()
            # Split line by comma
            fields = line.split(',')
            # Add fields to data list
            data.append(fields)
    return data

# Write lastfm data to the CSV file
def write_to_csv(filename, data):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Run the app
if __name__ == "__main__":

    # get config
    get_config()

    # read the file
    # Example usage
    filename = "machiisongs.csv"  # Replace with your CSV file name
    outputfile = "machiisongsspotify.csv"

    # initialise the file
    open(outputfile, 'w', newline='').close

    csv_data = read_csv_file(filename)
    print("CSV Data:")
    for row in csv_data:
        track = row[0]
        artist = row[1] 
        print(f"fetching {track} details")
        get_track_info(track.strip(), artist.strip())
        print("----------------------")
        time.sleep(0.5)





        
        


    