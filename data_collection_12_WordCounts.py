"""
data_collection_12_WordCounts.py 

6 - preparation for word frequency analysis
7 - word frequency analysis 
8 - calculations
9 - trying to understand why centrality is related to noun/propernoun use

@author: lizakarmannaya
"""


########################################################################
######## 6 - preparation for word frequency analysis ###################
########################################################################

import pandas as pd
import os 
import glob
import csv
import collections
import matplotlib.pyplot as plt
import re

#import spacy 

#everything below has been repeated for RIGHT too 
os.chdir(os.path.expanduser("~"))
os.chdir('ark-tweet-nlp-0.3.2/outputs_conll/RIGHT') #do this once


errors = []
Propernoun_tags = ['^', 'Z', 'M']
Noun_tags = ['N', 'S', 'L']

Propernouns_LEFT = []
Nouns_LEFT = []

Propernouns_RIGHT = []
Nouns_RIGHT = []


counter = 0
for txt_file in glob.glob("*.txt"): 
    counter+=1

    #extract user_id from file name 
    user_id = txt_file.split("tweets_")[1] 
    user_id = user_id.split(".txt")[0]

    with open(txt_file, 'r') as f:
        try:
            for tweet in f.read().split('\n\n'): #for every tweet from this user
                lines = tweet.split('\n') #create iterable with every triple of tab-separasted tags            
                lines_split = [x.split('\t') for x in lines] #this is now a list of 3 items
                for triple in lines_split:
                    if triple[1] in Propernoun_tags:
                        Propernouns_RIGHT.append(triple[0])
                    elif triple[1] in Noun_tags:
                        Nouns_RIGHT.append(triple[0])
        except IndexError as e:
            errors.append({user_id: {tweet: e}})

    print(f'finished file {counter} out of 17789 LEFT/16496 RIGHT')


len(Propernouns_LEFT) #1,564,753 
len(errors) #17788 - 1 for each tweet - this is the blank line at the end 
len(Nouns_LEFT) #5,669,614
Propernouns_LEFT[0] #print out the first item in Propernouns_LEFT

len(Propernouns_RIGHT) #1,199,460
len(errors) #16496 - 1 for each tweet - this is the blank line at the end 
len(Nouns_RIGHT) #3,787,619

os.chdir(os.path.expanduser("~"))


with open ('RESULTS_LEFT_Propernoun_frequency_list.txt', 'w') as f:
    [f.write(str(val) + '\n') for val in Propernouns_LEFT]
with open ('RESULTS_LEFT_Noun_frequency_list.txt', 'w') as f:
    [f.write(str(val) + '\n') for val in Nouns_LEFT]

with open ('RESULTS_RIGHT_Propernoun_frequency_list.txt', 'w') as f:
    [f.write(str(val) + '\n') for val in Propernouns_RIGHT]
with open ('RESULTS_RIGHT_Noun_frequency_list.txt', 'w') as f:
    [f.write(str(val) + '\n') for val in Nouns_RIGHT]




#with open("RESULTS_LEFT_Noun_frequency_list.txt", "w") as f:
#    for s in score:
#        f.write(str(s) +"\n")
## read files in again 
os.chdir(os.path.expanduser("~"))
Propernouns_LEFT = []
with open("RESULTS_LEFT_Propernoun_frequency_list.txt", "r") as f:
    for line in f:
        Propernouns_LEFT.append(str(line.strip()))

Nouns_LEFT = []
with open("RESULTS_LEFT_Noun_frequency_list.txt", "r") as f:
    for line in f:
        Nouns_LEFT.append(str(line.strip()))

Propernouns_RIGHT = []
with open("RESULTS_RIGHT_Propernoun_frequency_list.txt", "r") as f:
    for line in f:
        Propernouns_RIGHT.append(str(line.strip()))

Nouns_RIGHT = []
with open("RESULTS_RIGHT_Noun_frequency_list.txt", "r") as f:
    for line in f:
        Nouns_RIGHT.append(str(line.strip()))


len(Nouns_LEFT) #e.g. check that they loaded in correctly - 5669614
len(set(Propernouns_LEFT)) #224612
len(set(Nouns_LEFT)) #165551




########################################################################
######## 7 - WORD FREQUENCY ANALYSIS ###################################
########################################################################
#tf-idf - to find words especially important for 
#n-grams - e.g. models like fasttext - will create similar vectors for misspelt words 

#formula from Sylwester & Purver 
    #first lowercase, remove stopwords, lemmatise/extract word stems 

#formula from Bryden et al. (2013) 

#see log odds ratio here https://www.tidytextmining.com/twitter.html 



type(Propernouns_LEFT[0]) #str


#### 7.1 - analyse word frequencies without any cleaning
## ignore #tweets per user or #tags per tweet
## --> put all tags into one list 

Propernouns_LEFT 
Nouns_LEFT 


Propernouns_RIGHT 
Nouns_RIGHT 

#### 1. Propernouns_LEFT ####
counts_Propernouns_LEFT = collections.Counter(Propernouns_LEFT)
counts_Propernouns_LEFT.most_common(30)
#create df 
counts_Propernouns_LEFT_30 = pd.DataFrame(counts_Propernouns_LEFT.most_common(30), columns=['words', 'count'])
counts_Propernouns_LEFT_30.head()
#create graph
fig, ax = plt.subplots(figsize=(8, 8))
# Plot horizontal bar graph
counts_Propernouns_LEFT_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common Propernouns Found in LEFT Tweets (Including All Words)")
plt.savefig('RESULTS/WordCounts/Propernouns_LEFT_mostcommon.png')

#save df of most common words 
#'RESULTS/WordCounts/Propernouns_LEFT_mostcommon.csv'



#### 2. Propernouns_RIGHT ####
counts_Propernouns_RIGHT = collections.Counter(Propernouns_RIGHT)
counts_Propernouns_RIGHT_30 = pd.DataFrame(counts_Propernouns_RIGHT.most_common(30), columns=['words', 'count'])
counts_Propernouns_RIGHT_30.head()
fig, ax = plt.subplots(figsize=(8, 8))
counts_Propernouns_RIGHT_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="blue")
ax.set_title("Common Propernouns Found in RIGHT Tweets (Including All Words)")
plt.savefig('RESULTS/WordCounts/Propernouns_RIGHT_mostcommon.png')


#### 3. Nouns_LEFT ####
counts_Nouns_LEFT = collections.Counter(Nouns_LEFT)
counts_Nouns_LEFT_30 = pd.DataFrame(counts_Nouns_LEFT.most_common(30), columns=['words', 'count'])
counts_Nouns_LEFT_30.head()
fig, ax = plt.subplots(figsize=(8, 8))
counts_Nouns_LEFT_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common Nouns Found in LEFT Tweets (Including All Words)")
plt.savefig('RESULTS/WordCounts/Nouns_LEFT_mostcommon.png')


#### 4. Nouns_RIGHT ####
counts_Nouns_RIGHT = collections.Counter(Nouns_RIGHT)
counts_Nouns_RIGHT_30 = pd.DataFrame(counts_Nouns_RIGHT.most_common(30), columns=['words', 'count'])
counts_Nouns_RIGHT_30.head()
fig, ax = plt.subplots(figsize=(8, 8))
counts_Nouns_RIGHT_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="blue")
ax.set_title("Common Nouns Found in RIGHT Tweets (Including All Words)")
plt.savefig('RESULTS/WordCounts/Nouns_RIGHT_mostcommon.png')






#### 7.2 all to lowercase  
## remember, RTs have been removed entirely already 

Propernouns_LEFT_lower = [word.lower() for word in Propernouns_LEFT]
Propernouns_RIGHT_lower = [word.lower() for word in Propernouns_RIGHT]
Nouns_LEFT_lower = [word.lower() for word in Nouns_LEFT]
Nouns_RIGHT_lower = [word.lower() for word in Nouns_RIGHT]

#repeat all graphs from above
counts_Propernouns_LEFT_lower = collections.Counter(Propernouns_LEFT_lower)
counts_Propernouns_LEFT_lower_30 = pd.DataFrame(counts_Propernouns_LEFT_lower.most_common(30), columns=['words', 'count'])
counts_Propernouns_LEFT_lower_30.head()
fig, ax = plt.subplots(figsize=(8, 8))
counts_Propernouns_LEFT_lower_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common Propernouns Found in LEFT Tweets (Including All Words lowercased)")
plt.savefig('RESULTS/WordCounts/Propernouns_LEFT_mostcommon_lowercase.png')




#### 7.3 - lemmatise 
#### 7.3.1 - lemmatise using NLTK WordNet 
## NB drop all emojis from tokens 

## NB drop # from tokens 


#example
## Nb need to define POS for which I am lemmatising this
import nltk
#nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

type(Propernouns_LEFT[0])

for word in Propernouns_LEFT:
    word = word.lower()
    print ("{0:20}{1:20}".format(word,wordnet_lemmatizer.lemmatize(word, pos='n')))
#this doesn't drop 's 


for word in Nouns_LEFT:
    print ("{0:20}{1:20}".format(word,wordnet_lemmatizer.lemmatize(word, pos="n")))
#this doesn't drop 's 





#### 7.3.2 - lemmatise using SpaCy
import spacy
# Initialize spacy 'en' model, keeping only tagger component needed for lemmatization
nlp = spacy.load('en', disable=['parser', 'ner'])

sentence = "The striped bats are hanging on their feet for best"

# Parse the sentence using the loaded 'en' model object `nlp`
doc = nlp(sentence)

# Extract the lemma for each token and join
" ".join([token.lemma_ for token in doc])




#### 7.3.3 - clean (pseudo-lemmatise) using RegExpression
## manually drop emojis 
#function to prepare for dropping emojis
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


## manually srop 's, 'll, 'd, 've, 'm, 're - #NB apostrophe has to be both ’ and ' 
## manually lowercase, strip of whitespace, drop '#' (hastags here are used as parts of speech - see POS tagger description)
## manually remove emoji 

Propernouns_LEFT_clean = [string.lower().strip().replace("#", "") for string in Propernouns_LEFT]
Propernouns_LEFT_clean = [re.sub(r"((’|')(s|ll|d|ve|m|re))", "", string) for string in Propernouns_LEFT_clean] 
Propernouns_LEFT_clean = [remove_emoji(string) for string in Propernouns_LEFT_clean]
Propernouns_LEFT_clean = list(filter(None, Propernouns_LEFT_clean)) #drop empty stirng which is the result of dropping emoji
#now plot the most common 30 
counts_Propernouns_LEFT_clean = collections.Counter(Propernouns_LEFT_clean)
len(counts_Propernouns_LEFT_clean) #166338
#counts_Propernouns_LEFT_clean.most_common(30)
#create df 
counts_Propernouns_LEFT_clean_30 = pd.DataFrame(counts_Propernouns_LEFT_clean.most_common(30), columns=['words', 'count'])
counts_Propernouns_LEFT_clean_30.head()
#create graph
fig, ax = plt.subplots(figsize=(8, 8))
# Plot horizontal bar graph
counts_Propernouns_LEFT_clean_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common Propernouns Found in LEFT Tweets (Including All Words without 's|'ll|'d|'ve|'m|'re, '#' & emojis, lowercased, no emoji)")
plt.savefig('RESULTS/WordCounts/Propernouns_LEFT_clean_3_mostcommon.png')


#repeat for Propernouns RIGHT 
Propernouns_RIGHT_clean = [string.lower().strip().replace("#", "") for string in Propernouns_RIGHT]
Propernouns_RIGHT_clean = [re.sub(r"((’|')(s|ll|d|ve|m|re))", "", string) for string in Propernouns_RIGHT_clean]
Propernouns_RIGHT_clean = [remove_emoji(string) for string in Propernouns_RIGHT_clean]
Propernouns_RIGHT_clean = list(filter(None, Propernouns_RIGHT_clean)) #drop empty stirng which is the result of dropping emoji
counts_Propernouns_RIGHT_clean = collections.Counter(Propernouns_RIGHT_clean)
len(counts_Propernouns_RIGHT_clean) #146319
counts_Propernouns_RIGHT_clean_30 = pd.DataFrame(counts_Propernouns_RIGHT_clean.most_common(30), columns=['words', 'count'])
counts_Propernouns_RIGHT_clean_30.head()
fig, ax = plt.subplots(figsize=(8, 8))
counts_Propernouns_RIGHT_clean_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="blue")
ax.set_title("Common Propernouns Found in RIGHT Tweets (Including All Words without 's|'ll|'d|'ve|'m|'re, '#' & emojis, lowercased, no emoji)")
plt.savefig('RESULTS/WordCounts/Propernouns_RIGHT_clean_3_mostcommon.png')


#repeat for Nouns LEFT 
Nouns_LEFT_clean = [string.lower().strip().replace("#", "") for string in Nouns_LEFT]
Nouns_LEFT_clean = [re.sub(r"((’|')(s|ll|d|ve|m|re))", "", string) for string in Nouns_LEFT_clean]
Nouns_LEFT_clean = [remove_emoji(string) for string in Nouns_LEFT_clean]
Nouns_LEFT_clean = list(filter(None, Nouns_LEFT_clean)) #drop empty stirng which is the result of dropping emoji
counts_Nouns_LEFT_clean = collections.Counter(Nouns_LEFT_clean)
len(counts_Nouns_LEFT_clean) #116856
counts_Nouns_LEFT_clean_30 = pd.DataFrame(counts_Nouns_LEFT_clean.most_common(30), columns=['words', 'count'])
counts_Nouns_LEFT_clean_30.head()
fig, ax = plt.subplots(figsize=(8, 8))
counts_Nouns_LEFT_clean_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common Nouns Found in LEFT Tweets (Including All Words without 's|'ll|'d|'ve|'m|'re, '#' & emojis, lowercased)")
plt.savefig('RESULTS/WordCounts/Nouns_LEFT_clean_3_mostcommon.png')


#repeat for Nouns RIGHT
Nouns_RIGHT_clean = [string.lower().strip().replace("#", "") for string in Nouns_RIGHT]
Nouns_RIGHT_clean = [re.sub(r"((’|')(s|ll|d|ve|m|re))", "", string) for string in Nouns_RIGHT_clean]
Nouns_RIGHT_clean = [remove_emoji(string) for string in Nouns_RIGHT_clean]
Nouns_RIGHT_clean = list(filter(None, Nouns_RIGHT_clean)) #drop empty stirng which is the result of dropping emoji
counts_Nouns_RIGHT_clean = collections.Counter(Nouns_RIGHT_clean)
len(counts_Nouns_RIGHT_clean) #93293
counts_Nouns_RIGHT_clean_30 = pd.DataFrame(counts_Nouns_RIGHT_clean.most_common(30), columns=['words', 'count'])
counts_Nouns_RIGHT_clean_30.head()
fig, ax = plt.subplots(figsize=(8, 8))
counts_Nouns_RIGHT_clean_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="blue")
ax.set_title("Common Nouns Found in RIGHT Tweets (Including All Words without 's|'ll|'d|'ve|'m|'re, '#' & emojis, lowecased)")
plt.savefig('RESULTS/WordCounts/Nouns_RIGHT_clean_3_mostcommon.png')





#### 7.4 - stem? - NO, doesn't work 
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
porter = PorterStemmer()
lancaster=LancasterStemmer()

for word in Propernouns_LEFT:
    print ("{0:20}{1:20}".format(word,porter.stem(word)))
#this returns words as lowercase, without 's' at the end, without the 's' after apostrophe, but still including the apostrophe itself 
#'Stalinism' --> 'Stalin' 
#'Christmas' --> 'christma'
#'Coronavirus' --> 'coronaviru' 
for word in Propernouns_LEFT:
    print ("{0:20}{1:20}".format(word,lancaster.stem(word)))
#Energy’s --> energy’s            
#Aluminium --> alumin              
#Australia --> austral             
#Union --> un                  




#### 7.4 - more cleaning?
#### 7.4.1 - do I need to exclude 'coronavirus, covid etc.'? 
len(Propernouns_LEFT) #1564753
len(Propernouns_RIGHT) #1199460
len(Nouns_LEFT) #5669614
len(Nouns_RIGHT) #3787619

coronavirus = ['coronavirus', 'sarscov2', 'covid', 'covid19', 'covid_19', 'covid-19', 'covid2019', 'covid_2019', 'covid-2019', 'cov19', 'cov_19', 'cov-19', 'cov2019', 'cov_2019', 'cov-2019', 'cv19', 'cv_19', 'cv-19', 'cv2019', 'cv_2019', 'cv-2019', 'covid19uk', 'covid2019uk']

#already lowercased
#already dropped hashtags & emojis &'s etc.  
len(Propernouns_LEFT_clean) #1546104
len(Propernouns_RIGHT_clean) #1182685
len(Nouns_LEFT_clean) #5665362
len(Nouns_RIGHT_clean) #3783808

my_collection_Propernouns = Propernouns_LEFT_clean+Propernouns_RIGHT_clean
len(my_collection_Propernouns) #2728789

my_collection_Nouns = Nouns_LEFT_clean + Nouns_RIGHT_clean
len(my_collection_Nouns) #9449170

#now create a list of all words in these 2 collections that match tags in 'coronavirus'
coronavirus_in_my_collection_Nouns = [] 
for word in my_collection_Nouns:
    if word in coronavirus:
        coronavirus_in_my_collection_Nouns.append(word)
len(coronavirus_in_my_collection_Nouns) #13349
len(coronavirus_in_my_collection_Nouns)/len(my_collection_Nouns) #0.0014127166724696456 --> =0.1% --> don't need to multiverse Nouns 


coronavirus_in_my_collection_Propernouns = [] 
for word in my_collection_Propernouns:
    if word in coronavirus:
        coronavirus_in_my_collection_Propernouns.append(word)
len(coronavirus_in_my_collection_Propernouns) #24478
len(coronavirus_in_my_collection_Propernouns)/len(my_collection_Propernouns) #0.008970279490279388 --> don't need to multiverse Propernouns 


########
## now also calcualte proportions 'coronavirus' by side 
coronavirus_in_my_collection_Nouns_Left = [] 
for word in Nouns_LEFT_clean:
    if word in coronavirus:
        coronavirus_in_my_collection_Nouns_Left.append(word)
len(coronavirus_in_my_collection_Nouns_Left)/len(Nouns_LEFT_clean) #0.0012387557935397597

coronavirus_in_my_collection_Nouns_Right = [] 
for word in Nouns_RIGHT_clean:
    if word in coronavirus:
        coronavirus_in_my_collection_Nouns_Right.append(word)
len(coronavirus_in_my_collection_Nouns_Right)/len(Nouns_RIGHT_clean) #0.001673182148777105

coronavirus_in_my_collection_Propernouns_Left = [] 
for word in Propernouns_LEFT_clean:
    if word in coronavirus:
        coronavirus_in_my_collection_Propernouns_Left.append(word)
len(coronavirus_in_my_collection_Propernouns_Left)/len(Propernouns_LEFT_clean) #0.00806220021421586

coronavirus_in_my_collection_Propernouns_Right = [] 
for word in Propernouns_RIGHT_clean:
    if word in coronavirus:
        coronavirus_in_my_collection_Propernouns_Right.append(word)
len(coronavirus_in_my_collection_Propernouns_Right)/len(Propernouns_RIGHT_clean) #0.010157396094479933



#### 7.4.1 - do I need to exclude pronouns from Nouns lists? 
first_pers_pronouns = ['i', 'we', 'me','us','mine','ours','my','our','myself','ourselves'] 
second_pers_pronouns = ['you','yours','your','yourself','yourselves']
third_pers_pronouns = ['he', 'she', 'it', 'they', 'her','him','them','hers','his','its','theirs','his','their','herself','himself','itself','themselves']
other_pronouns = ['all','another','any','anybody','anyone','anything','both','each','either','everybody','everyone','everything','few','many','most','neither','nobody','none','noone','nothing','one','other','others','several','some','somebody','someone','something','such','that','these','this','those','what','whatrever','which','whichever','who','whoever','whom','whomever','whose','as','that','what','whatever','thou','thee','thy','thine','ye','eachother','everybody','naught','nought','somewhat','thyself','whatsoever','whence','where','whereby','wherever']

pronouns = first_pers_pronouns + second_pers_pronouns + third_pers_pronouns + other_pronouns
len(pronouns) #94

#now create a list of all words in these 2 collections that match tags in 'coronavirus'
pronouns_in_my_collection_Nouns = [] 
for word in my_collection_Nouns:
    if word in pronouns:
        pronouns_in_my_collection_Nouns.append(word)
len(pronouns_in_my_collection_Nouns) #929401
len(pronouns_in_my_collection_Nouns)/len(my_collection_Nouns) #0.09835795101580351 --> need to multiverse Nouns?


pronouns_in_my_collection_Propernouns = [] 
for word in my_collection_Propernouns:
    if word in pronouns:
        pronouns_in_my_collection_Propernouns.append(word)
len(pronouns_in_my_collection_Propernouns) #15902
len(pronouns_in_my_collection_Propernouns)/len(my_collection_Propernouns) #0.005827493441229791 --> don't need to multiverse Propernouns 



## --> re-plot Nouns without pronouns: 
def remove_pronouns(wordlist): 
    wordlist_clean = [word for word in wordlist if word not in pronouns]
    return wordlist_clean

len(Nouns_LEFT_clean) #5665362
len(Nouns_RIGHT_clean) #3783808


Nouns_LEFT_clean_nopronouns = remove_pronouns(Nouns_LEFT_clean)
len(Nouns_LEFT_clean_nopronouns) #5074947

Nouns_RIGHT_clean_nopronouns = remove_pronouns(Nouns_RIGHT_clean)
len(Nouns_RIGHT_clean_nopronouns) #3444822

counts_Nouns_LEFT_clean_nopronouns = collections.Counter(Nouns_LEFT_clean_nopronouns)
len(counts_Nouns_LEFT_clean_nopronouns) #116784
counts_Nouns_LEFT_clean_nopronouns_30 = pd.DataFrame(counts_Nouns_LEFT_clean_nopronouns.most_common(30), columns=['words', 'count'])
counts_Nouns_LEFT_clean_nopronouns_30.head()
fig, ax = plt.subplots(figsize=(8, 8))
counts_Nouns_LEFT_clean_nopronouns_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common Nouns Found in LEFT Tweets (Including All non-pronoun Words without 's|'ll|'d|'ve|'m|'re, '#' & emojis, lowecased)")
plt.savefig('RESULTS/WordCounts/Nouns_LEFT_clean_3_mostcommon_nopronouns.png')


counts_Nouns_RIGHT_clean_nopronouns = collections.Counter(Nouns_RIGHT_clean_nopronouns)
len(counts_Nouns_RIGHT_clean_nopronouns) #93220
counts_Nouns_RIGHT_clean_nopronouns_30 = pd.DataFrame(counts_Nouns_RIGHT_clean_nopronouns.most_common(30), columns=['words', 'count'])
counts_Nouns_RIGHT_clean_nopronouns_30.head()
fig, ax = plt.subplots(figsize=(8, 8))
counts_Nouns_RIGHT_clean_nopronouns_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="blue")
ax.set_title("Common Nouns Found in RIGHT Tweets (Including All non-pronoun Words without 's|'ll|'d|'ve|'m|'re, '#' & emojis, lowecased)")
plt.savefig('RESULTS/WordCounts/Nouns_RIGHT_clean_3_mostcommon_nopronouns.png')









#### 7.5 - see how big a proportion of my Propernouns/Nouns emojis constitute

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002500-\U00002BEF"  # chinese char
                           u"\U00002702-\U000027B0"
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001f926-\U0001f937"
                           u"\U00010000-\U0010ffff"
                           u"\u2640-\u2642"
                           u"\u2600-\u2B55"
                           u"\u200d"
                           u"\u23cf"
                           u"\u23e9"
                           u"\u231a"
                           u"\ufe0f"  # dingbats
                           u"\u3030"
                           "]+", flags=re.UNICODE)

my_collection_Propernouns_uncleaned = Propernouns_LEFT + Propernouns_RIGHT
#need to use the uncleaned collection, because in the cleaned version I remove these emojis 
emojis_in_Propernouns = []
for word in my_collection_Propernouns_uncleaned:
    match_tag = emoji_pattern.match(word)
    if match_tag:
        emojis_in_Propernouns.append(word)
len(emojis_in_Propernouns) #46959
len(emojis_in_Propernouns)/len(my_collection_Propernouns_uncleaned) #0.01698819881101782
## --> emojis constitute only 1.7% of this collection  
## --> maybe shouls still try to drop entire tag if it contains emoji - as the words follower by them are rarely propernuons 


my_collection_Nouns_uncleaned = Nouns_LEFT + Nouns_RIGHT_clean
emojis_in_Nouns = []
for word in my_collection_Nouns_uncleaned:
    match_tag = emoji_pattern.match(word)
    if match_tag:
        emojis_in_Nouns.append(word)
len(emojis_in_Nouns) #6229
len(emojis_in_Nouns)/len(my_collection_Nouns_uncleaned) #0.000658914835283985







#######################################################
########### 8 - calculations ##########################
#######################################################

#P(word use | political affiliation) = #times word occurs in tweets of followers of this side / count of all words used in tweets of followers of this side 

df_LEFT = pd.read_csv('RESULTS_LEFT_noun_frequency_2.csv', index_col=0)
df_LEFT.head()
total_tags_LEFT = df_LEFT['total_tags'].sum()
total_tags_LEFT #33017889

df_RIGHT = pd.read_csv('RESULTS_RIGHT_noun_frequency_2.csv', index_col=0)
df_LEFT.head()
total_tags_RIGHT = df_RIGHT['total_tags'].sum()
total_tags_RIGHT #22513236


#Nouns, LEFT 
counts_Nouns_LEFT_clean = collections.Counter(Nouns_LEFT_clean) #dictionary
len(counts_Nouns_LEFT_clean) #116856 - same as len(set(Nouns_LEFT_clean)) 
data=[]
for word in set(Nouns_LEFT_clean): #only loop through each word once - no repetitions
    count = counts_Nouns_LEFT_clean[word]
    proportion = counts_Nouns_LEFT_clean[word]/total_tags_LEFT
    data.append([word, count, proportion])
df_Nouns_proportions_LEFT = pd.DataFrame(columns=['word', 'count', 'proportion'], data=data)
df_Nouns_proportions_LEFT.to_csv('df_Nouns_proportions_LEFT.csv')

#Nouns, RIGHT
counts_Nouns_RIGHT_clean = collections.Counter(Nouns_RIGHT_clean)
len(counts_Nouns_RIGHT_clean) #93293
data=[]
for word in set(Nouns_RIGHT_clean):
    count = counts_Nouns_RIGHT_clean[word]
    proportion = counts_Nouns_RIGHT_clean[word]/total_tags_RIGHT
    data.append([word, count, proportion])
df_Nouns_proportions_RIGHT = pd.DataFrame(columns=['word', 'count', 'proportion'], data=data)
df_Nouns_proportions_RIGHT.to_csv('df_Nouns_proportions_RIGHT.csv')


#Propernouns, LEFT 
counts_Propernouns_LEFT_clean = collections.Counter(Propernouns_LEFT_clean) #dictionary
len(counts_Propernouns_LEFT_clean) #166338 - same as len(set(Propernouns_LEFT_clean)) 
data=[]
for word in set(Propernouns_LEFT_clean):
    count = counts_Propernouns_LEFT_clean[word]
    proportion = counts_Propernouns_LEFT_clean[word]/total_tags_LEFT
    data.append([word, count, proportion])
df_Propernouns_proportions_LEFT = pd.DataFrame(columns=['word', 'count', 'proportion'], data=data)
df_Propernouns_proportions_LEFT.shape
df_Propernouns_proportions_LEFT.to_csv('df_Propernouns_proportions_LEFT.csv')

#Propernouns, RIGHT 
counts_Propernouns_RIGHT_clean = collections.Counter(Propernouns_RIGHT_clean) #dictionary
len(counts_Propernouns_RIGHT_clean) #146319
data=[]
for word in set(Propernouns_RIGHT_clean):
    count = counts_Propernouns_RIGHT_clean[word]
    proportion = counts_Propernouns_RIGHT_clean[word]/total_tags_RIGHT
    data.append([word, count, proportion])
df_Propernouns_proportions_RIGHT = pd.DataFrame(columns=['word', 'count', 'proportion'], data=data)
df_Propernouns_proportions_RIGHT.to_csv('df_Propernouns_proportions_RIGHT.csv')


#### re-import data 
df_Propernouns_proportions_LEFT = pd.read_csv('df_Propernouns_proportions_LEFT.csv', index_col=0)
df_Propernouns_proportions_RIGHT = pd.read_csv('df_Propernouns_proportions_RIGHT.csv', index_col=0)
df_Nouns_proportions_LEFT = pd.read_csv('df_Nouns_proportions_LEFT.csv', index_col=0)
df_Nouns_proportions_RIGHT = pd.read_csv('df_Nouns_proportions_RIGHT.csv', index_col=0)

df_Propernouns_proportions_LEFT.shape #(166338, 3)
df_Propernouns_proportions_RIGHT.shape #(146319, 3)
df_Nouns_proportions_LEFT.shape #(116856, 3)
df_Nouns_proportions_RIGHT.shape #(93293, 3)


#drop words with counts<20 from each df 
df_Propernouns_proportions_LEFT = df_Propernouns_proportions_LEFT[df_Propernouns_proportions_LEFT['count']>10]
df_Propernouns_proportions_LEFT.shape #(13378, 3)

df_Propernouns_proportions_RIGHT = df_Propernouns_proportions_RIGHT[df_Propernouns_proportions_RIGHT['count']>10]
df_Propernouns_proportions_RIGHT.shape #(10943, 3)

df_Nouns_proportions_LEFT = df_Nouns_proportions_LEFT[df_Nouns_proportions_LEFT['count']>10]
df_Nouns_proportions_LEFT.shape #(17368, 3)

df_Nouns_proportions_RIGHT = df_Nouns_proportions_RIGHT[df_Nouns_proportions_RIGHT['count']>10]
df_Nouns_proportions_RIGHT.shape #(14468, 3)




#### NOW display them by highest proportion first 
df_Propernouns_proportions_LEFT.head()
df_Propernouns_proportions_LEFT_sorted = df_Propernouns_proportions_LEFT.sort_values(by = 'count', ascending=False)
df_Propernouns_proportions_LEFT_sorted.head()

df_Propernouns_proportions_RIGHT.head()
df_Propernouns_proportions_RIGHT_sorted = df_Propernouns_proportions_RIGHT.sort_values(by = 'count', ascending=False)
df_Propernouns_proportions_LEFT_sorted.head()


df_Propernouns_LEFT-RIGHT = pd.DataFrame()

#re-set index as 'word' so I can loop over specific words? 
for index in df_Propernouns_proportions_LEFT.index:
    df_Propernouns_LEFT['word'].values[index] = df_Propernouns_proportions_LEFT['word'].values[index]
    #df_Propernouns_proportions_LEFT.at

    df_Propernouns_LEFT-RIGHT['LEFT-RIGHT'].values[index] = df_Propernouns_proportions_LEFT['proportion'].values[index]








################################################################################
#### 9 - trying to understand why centrality is related to noun/propernoun use :
################################################################################
## --> analyse words used by 10 MOST hubs-central users 

#find 10 most hubs-central users in df 
df = pd.read_csv('RESULTS_df_multiverse_DIRECTED.csv', index_col=0)
df.head()
df.shape
df_LEFT = df[df['side']=='LEFT']
df_LEFT.shape
df_LEFT.head()
df_RIGHT = df[df['side']=='RIGHT']
df_RIGHT.shape


df_LEFT_sorted = df_LEFT.sort_values(by='hubs', ascending=False) #most central at the top
df_LEFT_sorted = df_LEFT_sorted.head(10)
LEFT_central_ids = list(df_LEFT_sorted['user_id_str'])
LEFT_central_ids
#now manualy save these ids into 'ark-tweet-nlp-0.3.2/outputs_conll/LEFT/most_central'

df_RIGHT_sorted = df_RIGHT.sort_values(by='hubs', ascending=False) #most central at the top
df_RIGHT_sorted = df_RIGHT_sorted.head(10)
RIGHT_central_ids = list(df_RIGHT_sorted['user_id_str'])
RIGHT_central_ids
#now manualy save these ids into 'ark-tweet-nlp-0.3.2/outputs_conll/LEFT/most_central'


## 1. LEFT 
os.chdir(os.path.expanduser("~"))
os.chdir('ark-tweet-nlp-0.3.2/outputs_conll/LEFT/most_central') #do this once


errors = []
Propernoun_tags = ['^', 'Z', 'M']
Noun_tags = ['N', 'S', 'L']

Propernouns_LEFT_central = [] #skip this at the second run 
Nouns_LEFT_central = [] #skip this at the second run 

Propernouns_RIGHT_central = []
Nouns_RIGHT_central = []


counter = 0
for txt_file in glob.glob("*.txt"): 
    counter+=1

    #extract user_id from file name 
    user_id = txt_file.split("tweets_")[1] 
    user_id = user_id.split(".txt")[0]

    with open(txt_file, 'r') as f:
        try:
            for tweet in f.read().split('\n\n'): #for every tweet from this user
                lines = tweet.split('\n') #create iterable with every triple of tab-separasted tags            
                lines_split = [x.split('\t') for x in lines] #this is now a list of 3 items
                for triple in lines_split:
                    if triple[1] in Propernoun_tags:
                        Propernouns_LEFT_central.append(triple[0]) #CHANGE to LEFT/RIGHT
                    elif triple[1] in Noun_tags: 
                        Nouns_LEFT_central.append(triple[0]) #CHANGE to LEFT/RIGHT
        except IndexError as e:
            errors.append({user_id: {tweet: e}})

    print(f'finished file {counter}')


len(Propernouns_LEFT_central) #363
len(errors) #10 - 1 for each tweet - this is the blank line at the end 
len(Nouns_LEFT_central) #1668
Propernouns_LEFT_central[0] 

##NOW re-run this with RIGHT 
len(Propernouns_RIGHT_central) #431
len(errors) #10 - 1 for each tweet - this is the blank line at the end 
len(Nouns_RIGHT_central) #1546
Nouns_RIGHT_central[0]

#now clean these 
def clean_wordlist(wordlist):
    wordlist_clean = [string.lower().strip().replace("#", "") for string in wordlist]
    wordlist_clean = [re.sub(r"((’|')(s|ll|d|ve|m|re))", "", string) for string in wordlist_clean] 
    wordlist_clean = [remove_emoji(string) for string in wordlist_clean] ##NB define this function earlier
    wordlist_clean = list(filter(None, wordlist_clean)) #drop empty stirng which is the result of dropping emoji
    return wordlist_clean

Propernouns_LEFT_central_clean = clean_wordlist(Propernouns_LEFT_central)
Nouns_LEFT_central_clean = clean_wordlist(Nouns_LEFT_central)
Propernouns_RIGHT_central_clean = clean_wordlist(Propernouns_RIGHT_central)
Nouns_RIGHT_central_clean = clean_wordlist(Nouns_RIGHT_central)


len(Propernouns_LEFT_central_clean) #363 --> 362
len(Nouns_LEFT_central) #1668 --> 1668
len(Propernouns_RIGHT_central) #431 --> 431
len(Nouns_RIGHT_central) #1546 --> 1546




###visualise & save most common words for these 10 users
os.chdir(os.path.expanduser("~"))

#Propernouns
counts_Propernouns_LEFT_c = collections.Counter(Propernouns_LEFT_central_clean)
counts_Propernouns_LEFT_c_30 = pd.DataFrame(counts_Propernouns_LEFT_c.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(8, 8))
counts_Propernouns_LEFT_c_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common Propernouns Found in Tweets of 10 most LEFT-central users (Including All Words cleaned)")
plt.savefig('RESULTS/WordCounts/Propernouns_LEFT_10mostcentral_mostcommon_clean.png')

counts_Propernouns_RIGHT_c = collections.Counter(Propernouns_RIGHT_central_clean)
counts_Propernouns_RIGHT_c_30 = pd.DataFrame(counts_Propernouns_RIGHT_c.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(8, 8))
counts_Propernouns_RIGHT_c_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="blue")
ax.set_title("Common Propernouns Found in Tweets of 10 most RIGHT-central users (Including All Words cleaned)")
plt.savefig('RESULTS/WordCounts/Propernouns_RIGHT_10mostcentral_mostcommon_clean.png')

#Nouns
counts_Nouns_LEFT_c = collections.Counter(Nouns_LEFT_central_clean)
counts_Nouns_LEFT_c_30 = pd.DataFrame(counts_Nouns_LEFT_c.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(8, 8))
counts_Nouns_LEFT_c_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common Nouns Found in Tweets of 10 most LEFT-central users (Including All Words cleaned)")
plt.savefig('RESULTS/WordCounts/Nouns_LEFT_10mostcentral_mostcommon_clean.png')

counts_Nouns_RIGHT_c = collections.Counter(Nouns_RIGHT_central_clean)
counts_Nouns_RIGHT_c_30 = pd.DataFrame(counts_Nouns_RIGHT_c.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(8, 8))
counts_Nouns_RIGHT_c_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="blue")
ax.set_title("Common Nouns Found in Tweets of 10 most RIGHT-central users (Including All Words cleaned)")
plt.savefig('RESULTS/WordCounts/Nouns_RIGHT_10mostcentral_mostcommon_clean.png')




## --> analyse words used by 10 LEAST hubs-central users 
#find 10 most hubs-central users in df 
#1. re-import df 
df = pd.read_csv('RESULTS_df_multiverse_DIRECTED.csv', index_col=0)
df.shape
df_LEFT = df[df['side']=='LEFT']
df_RIGHT = df[df['side']=='RIGHT']
df_LEFT_sorted = df_LEFT.sort_values(by='hubs', ascending=False) #most central at the top
df_RIGHT_sorted = df_RIGHT.sort_values(by='hubs', ascending=False) #most central at the top

df_LEFT_sorted = df_LEFT_sorted.tail(10)
LEFT_leastcentral_ids = list(df_LEFT_sorted['user_id_str'])
LEFT_leastcentral_ids
#now manualy save these ids into 'ark-tweet-nlp-0.3.2/outputs_conll/LEFT/least_central'

df_RIGHT_sorted = df_RIGHT_sorted.tail(10)
RIGHT_leastcentral_ids = list(df_RIGHT_sorted['user_id_str'])
RIGHT_leastcentral_ids
#now manualy save these ids into 'ark-tweet-nlp-0.3.2/outputs_conll/LEFT/least_central'


## 1. LEFT; 2. RIGHT
os.chdir(os.path.expanduser("~"))
os.chdir('ark-tweet-nlp-0.3.2/outputs_conll/LEFT/least_central') #do this once

errors = []
Propernoun_tags = ['^', 'Z', 'M']
Noun_tags = ['N', 'S', 'L']

Propernouns_LEFT_leastcentral = []
Nouns_LEFT_leastcentral = []

Propernouns_RIGHT_leastcentral = []
Nouns_RIGHT_leastcentral = []

counter = 0
for txt_file in glob.glob("*.txt"): 
    counter+=1

    #extract user_id from file name 
    user_id = txt_file.split("tweets_")[1] 
    user_id = user_id.split(".txt")[0]

    with open(txt_file, 'r') as f:
        try:
            for tweet in f.read().split('\n\n'): #for every tweet from this user
                lines = tweet.split('\n') #create iterable with every triple of tab-separasted tags            
                lines_split = [x.split('\t') for x in lines] #this is now a list of 3 items
                for triple in lines_split:
                    if triple[1] in Propernoun_tags:
                        Propernouns_LEFT_leastcentral.append(triple[0])#CHANGE to LEFT/RIGHT
                    elif triple[1] in Noun_tags:
                        Nouns_LEFT_leastcentral.append(triple[0]) #CHANGE to LEFT/RIGHT
        except IndexError as e:
            errors.append({user_id: {tweet: e}})

    print(f'finished file {counter}')


len(Propernouns_LEFT_leastcentral) #1139
len(errors) #10 - 1 for each tweet - this is the blank line at the end 
len(Nouns_LEFT_leastcentral) #3375
Propernouns_LEFT_leastcentral[0] #'Newhaven'

len(Propernouns_RIGHT_leastcentral) #894
len(errors) #10 - 1 for each tweet - this is the blank line at the end 
len(Nouns_RIGHT_leastcentral) #3424

#now clean these using functions defined above 
Propernouns_LEFT_leastcentral_clean = clean_wordlist(Propernouns_LEFT_leastcentral)
Nouns_LEFT_leastcentral_clean = clean_wordlist(Nouns_LEFT_leastcentral)
Propernouns_RIGHT_leastcentral_clean = clean_wordlist(Propernouns_RIGHT_leastcentral)
Nouns_RIGHT_leastcentral_clean = clean_wordlist(Nouns_RIGHT_leastcentral)


len(Propernouns_LEFT_leastcentral_clean) #1139 --> 1112
len(Nouns_LEFT_leastcentral_clean) #3375 --> 3370
len(Propernouns_RIGHT_leastcentral_clean) # 894 --> 683
len(Nouns_RIGHT_leastcentral_clean) #3424 --> 3090



###visualise & save most common words for these 10 users
os.chdir(os.path.expanduser("~"))

#Propernouns
counts_Propernouns_LEFT_lc = collections.Counter(Propernouns_LEFT_leastcentral_clean)
counts_Propernouns_LEFT_lc_30 = pd.DataFrame(counts_Propernouns_LEFT_lc.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(8, 8))
counts_Propernouns_LEFT_lc_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common Propernouns Found in Tweets of 10 least LEFT-central users (Including All Words cleaned)")
plt.savefig('RESULTS/WordCounts/Propernouns_LEFT_10leasttcentral_mostcommon_clean.png')

counts_Propernouns_RIGHT_lc = collections.Counter(Propernouns_RIGHT_leastcentral_clean)
counts_Propernouns_RIGHT_lc_30 = pd.DataFrame(counts_Propernouns_RIGHT_lc.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(8, 8))
counts_Propernouns_RIGHT_lc_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="blue")
ax.set_title("Common Propernouns Found in Tweets of 10 least RIGHT-central users (Including All Words)")
plt.savefig('RESULTS/WordCounts/Propernouns_RIGHT_10leastcentral_mostcommon_clean.png')

#Nouns
counts_Nouns_LEFT_lc = collections.Counter(Nouns_LEFT_leastcentral_clean)
counts_Nouns_LEFT_lc_30 = pd.DataFrame(counts_Nouns_LEFT_lc.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(8, 8))
counts_Nouns_LEFT_lc_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common Nouns Found in Tweets of 10 least LEFT-central users (Including All Words cleaned)")
plt.savefig('RESULTS/WordCounts/Nouns_LEFT_10leastcentral_mostcommon.png')

counts_Nouns_RIGHT_lc = collections.Counter(Nouns_RIGHT_leastcentral_clean)
counts_Nouns_RIGHT_lc_30 = pd.DataFrame(counts_Nouns_RIGHT_lc.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(8, 8))
counts_Nouns_RIGHT_lc_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="blue")
ax.set_title("Common Nouns Found in Tweets of 10 least RIGHT-central users (Including All Words cleaned)")
plt.savefig('RESULTS/WordCounts/Nouns_RIGHT_10leastcentral_mostcommon.png')







