import requests
import time
import csv 
import configparser



def get_config():
    # Lastpass API credentials
    config = configparser.ConfigParser()
    config.sections()
    config.read("config.ini")
    for key in config['LastPass']:  
        print(key)
    global api_key
    api_key = config['LastPass']['api_key']
    print("api_key: " + api_key)
    if(api_key == ""):
        print("no lastpass api key in config file")



# Get Last fm data
def get_song_details(artist, track):
    print("api_key: " + api_key)
    url = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&artist={artist}&track={track}&format=json"

    response = requests.get(url)
    data = response.json()

    if "error" in data:
        print("Error:", data["message"])
        outputdata = [
            [track, artist, 'not found']
        ]
        write_to_csv(outputfile,outputdata)
    else:
        track_info = data["track"]
        try:
            print("Song Details:")
            print(f"Artist: {track_info['artist']['name']}")
            print(f"Track: {track_info['name']}")                
            print(f"Album: {track_info['album']['title']}")
            minutes = (int(track_info['duration'])/1000) // 60
            seconds = (int(track_info['duration'])/1000) % 60

            if(len(str(int(seconds))) == 1):
                track_info['simpleduration'] = "00:0" + str(int(minutes)) + ":0" + str(int(seconds))
            else: 
                track_info['simpleduration'] = "00:0" + str(int(minutes)) + ":" + str(int(seconds))
            
            outputdata = [
                [track_info['name'], track_info['artist']['name'], track_info['album']['title'], track_info['simpleduration']]
            ]
            print(outputdata)
            write_to_csv(outputfile,outputdata)
        except KeyError:    
            print(KeyError)      
            outputdata = [
                [track, artist, KeyError]
            ]
            write_to_csv(outputfile,outputdata)
        
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
        get_song_details(artist.strip(), track.strip())
        print("----------------------")
        time.sleep(0.5)

    