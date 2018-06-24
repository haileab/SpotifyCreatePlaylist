import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import string

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class FindSongs():

    def __init__(self):
        #self.string = string
        self.trials = 1
        self.result = []

    def clean_string(self,s):
        '''
        Removes punctuation and lowercases the string.
        '''
        exclude = set(string.punctuation)
        clean = ''.join(ch.lower() for ch in s if ch not in exclude)
        return clean


    def split_search(self, string):

        self.trials += 1
        song_words = [x for x in string.split(" ")]
        for i in reversed(range(len(song_words))):
            input = " ".join(song_words[0:i+1])
            remainder = " ".join(song_words[i+1:])
            print('running loop:', i,"s:", "t:", input)
            print(f"searching res1:{input}")
            search_res = self.search_sub(input)


            if search_res != False:
                print('appending:')
                self.result.append(search_res)
                print('result_dic:',self.result)
                print("-" * 20, i)
                print(remainder == "")

                if remainder == "":
                    print("Done HURRAY!!!!!!!!!")
                    print(self.result)
                    break
                self.split_search(remainder)
                break
            else:
                continue

    def search_sub(self, input):
        '''
        Searches spotify for the "string" returns first result if it exists.
        '''
        input = '"'+input+'"' #adds quotes to string, to search for phrase

        results = sp.search(q='track:' + input , type='track', limit=20)

        try:
            song_0 = results['tracks']['items'][0]['name'] #exits try statement if no result (no first song)
            num_of_songs = len(results['tracks']['items'])
            # iterate through the search results and search for exact match
            if num_of_songs != 0:
                for i in range(num_of_songs):
                    song = results['tracks']['items'][i]['name']
                    clean_song_result = self.clean_string(song)

                    if clean_song_result == input.strip('"'):
                        print('match')
                        d = {'artist': results['tracks']['items'][i]['artists'][0]['name'],
                            'song': results['tracks']['items'][i]['name'],
                            'player_link': results['tracks']['items'][i]['external_urls']['spotify']
                            }
                        return d
                return False

        except:
            #no search results
            return False

#print(results)
if __name__ == '__main__':

    # if len(sys.argv) > 1:
    #     s = sys.argv[1]
    # else:
    #     print ("Missing: %s string_to_search" % (sys.argv[0],))
    #     sys.exit()
    s = "If I can't let it go out of my mind"
    test = FindSongs()
    clean = test.clean_string(s)
    test.split_search(clean)
