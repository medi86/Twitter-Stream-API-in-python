#importing libararies
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pprint import pprint
import pdb
import json
import re
from string import punctuation
import time
from collections import Counter

#twitter api user credentials
CONSUMER_KEY = 'key'
CONSUMER_SECRET = 'secret'
ACCESS_TOKEN_KEY = 'token-key'
ACCESS_TOKEN_SECRET = 'token-secret'

#starting the timer
start_time = time.time()

class apiListener(StreamListener):

    #initiates with timer and empty array
    def __init__(self, start_time, time_limit=0):

        self.time = start_time
        self.limit = time_limit
        self.arr = []

    def on_data(self, data):

        #recevies tweets until it hits the time limit
        while (time.time() - self.time) < self.limit:

            #turn the tweet object(json) into mutable unicode
            parse_data = json.loads(data)

            #checks if a tweet object is encodeable otherwise it will get error on non-tweet object
            if hasattr(parse_data.get('text'), 'encode'):
                #saves every tweet's text data into a variable then saves into the array 
                tweetText = parse_data.get('text').encode(encoding='UTF-8',errors='ignore')
                self.arr.append(tweetText)
            return True

        #turns array into a giant single string then lowercase everywords    
        self.arr = ' '.join(self.arr).lower()

        #using regex to split everywords(any char follows by space) in the string and saves into array, word by word.
        self.arr = re.split(r'[^0-9A-Za-z]+', self.arr)

        #list of stopwords in array
        blacklist = "t https rt co i a able about above abst accordance according accordingly across act actually added adj affected affecting affects after afterwards again against ah all almost alone along already also although always am among amongst an and announce another any anybody anyhow anymore anyone anything anyway anyways anywhere apparently approximately are aren arent arise around as aside ask asking at auth available away awfully b back be became because become becomes becoming been before beforehand begin beginning beginnings begins behind being believe below beside besides between beyond biol both brief briefly but by c ca came can cannot can't cause causes certain certainly co com come comes contain containing contains could couldnt d date did didn't different do does doesn't doing done don't down downwards due during e each ed edu effect eg eight eighty either else elsewhere end ending enough especially et et-al etc even ever every everybody everyone everything everywhere ex except f far few ff fifth first five fix followed following follows for former formerly forth found four from further furthermore g gave get gets getting give given gives giving go goes gone got gotten h had happens hardly has hasn't have haven't having he hed hence her here hereafter hereby herein heres hereupon hers herself hes hi hid him himself his hither home how howbeit however hundred i id ie if i'll im immediate immediately importance important in inc indeed index information instead into invention inward is isn't it itd it'll its itself i've j just k keep  keeps kept kg km know known knows l largely last lately later latter latterly least less lest let lets like liked likely line little 'll look looking looks ltd m made mainly make makes many may maybe me mean means meantime meanwhile merely mg might million miss ml more moreover most mostly mr mrs much mug must my myself n na name namely nay nd near nearly necessarily necessary need needs neither never nevertheless new next nine ninety no nobody non none nonetheless noone nor normally nos not noted nothing now nowhere o obtain obtained obviously of off often oh ok okay old omitted on once one ones only onto or ord other others otherwise ought our ours ourselves out outside over overall owing own p page pages part particular particularly past per perhaps placed please plus poorly possible possibly potentially pp predominantly present previously primarily probably promptly proud provides put q que quickly quite qv r ran rather rd re readily really recent recently ref refs regarding regardless regards related relatively research respectively resulted resulting results right run s said same saw say saying says sec section see seeing seem seemed seeming seems seen self selves sent seven several shall she shed she'll shes should shouldn't show showed shown showns shows significant significantly similar similarly since six slightly so some somebody somehow someone somethan something sometime sometimes somewhat somewhere soon sorry specifically specified specify specifying still stop strongly sub substantially successfully such sufficiently suggest sup sure  t take taken taking tell tends th than thank thanks thanx that that'll thats that've the their theirs them themselves then thence there thereafter thereby thered therefore therein there'll thereof therere theres thereto thereupon there've these they theyd they'll theyre they've think this those thou though thoughh thousand throug through throughout thru thus til tip to together too took toward towards tried tries truly try trying ts twice two u un under unfortunately unless unlike unlikely until unto up upon ups us use used useful usefully usefulness uses using usually v value various 've very via viz vol vols vs w want wants was wasnt way we wed welcome we'll went were werent we've what whatever what'll whats when whence whenever where whereafter whereas whereby wherein wheres whereupon wherever whether which while whim whither who whod whoever whole who'll whom whomever whos whose why widely willing wish with within without wont words world would wouldnt www x y yes yet you youd you'll your youre yours yourself yourselves you've z zero 1 2 3 4 5 6 7 8 9 0".split()

        #Display total word count before filter blacklist
        print "total Wordcount: " + str(len(self.arr))

        #count each words' occurance 
        topten = Counter(self.arr)
        
        #take out blacklist words in lists
        for word in blacklist:
            topten.pop(word, None)

        #Display TOPTEN words!    
        for key, value in topten.most_common(10):
            print "%s: %i" % (key, value)

        #After it prints out total word count and topten words exit out the app.    
        exit()

    #when error occurs print error status code
    def on_error(self, status):
        print status


if __name__ == '__main__':

    #adds credentials to oauth variable
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    streamserver = Stream(auth, apiListener(start_time, time_limit=10))

    #starts the server and receives tweets from Twitter Streming API
    streamserver.sample(languages=['en'])

