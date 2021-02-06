import pandas as pd
import json
from pandas.io.json import json_normalize
with open('watson.json') as f:
    data = json.load(f)

# df = pd.json_normalize(data)

# json_fixed = json_normalize(watson.json)

# jsonconvo = pd.read_json(json_fixed)

speakers=pd.DataFrame(data['speaker_labels']).loc[:,['from','speaker','to']]
convo=pd.DataFrame(data['results'][0]['alternatives'][0]['timestamps'])
speakers=speakers.join(convo)

ChangeSpeaker = speakers.loc[speakers['speaker'].shift() != speakers['speaker']].index

Transcript = pd.DataFrame(columns=['from', 'to', 'speaker', 'transcript'])

for counter in range(0,len(ChangeSpeaker)):
    print(counter)
    currentindex = ChangeSpeaker[counter]
    try:
        nextIndex=ChangeSpeaker[counter+1]-1
        temp = speakers.loc[currentindex:nextIndex,:]
    except:
        temp = speakers.loc[currentindex:,:]
    Transcript = Transcript.append(pd.DataFrame([[temp.head(1)['from'].values[0],temp.tail(1)['to'].values[0],temp.head(1)['speaker'].values[0],temp[0].tolist()]],columns=['from','to','speaker','transcript']))

Transcript.to_csv(r'transcript.txt', header=None, index=None, sep='\t', mode='a')
