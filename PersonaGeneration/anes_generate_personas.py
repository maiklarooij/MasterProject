import pandas as pd

#Functions for generating GPT strings from ANES 
def format_list(words):
    if len(words) == 0:
        return ""
    elif len(words) == 1:
        return words[0]
    else:
        formatted_words = ", ".join(words[:-1])
        return f"{formatted_words}, and {words[-1]}"
    
# This code fetches lines from the ANES, and returns as readable dict
def get_anes_rows(number_rows):

    df = pd.read_csv('anes_timeseries_2020_csv_20220210.csv', low_memory=False)

    df1 = df
    # V202545 how often post polituical content on twitter?
    # V202544 how often do you use twitter? 

    ##  Rename columns
    col_recode = {'V201600':'gender',
    'V203000': 'state',
    'V201511x': 'education',
    'V201534x':'employed',
    'V201549x':'race',
    'V201601':'sexOrientation',
    'V201602':'justifiedViolence',
    'V201617x': 'income',
    'V201627': 'selfCensor',
    'V201628':'gunsOwned',
    'V201005':'attentionPolitics',
    'V202073':'vote2020',
    'V201103':'vote2016',
    'V201105':'vote2012',
    'V201116':'afraid',
    'V201117':'outraged',
    'V201118': 'angry',
    'V201119':'happy',
    'V201120':'worried',
    'V201121':'proud',
    'V201122':'irritated',
    'V201123':'nervous',
    'V201201':'liberalOrConservative',
    'V201228':'partyIdentif',
    'V201231x':'strongIdentif',
    'V201232':'partyIdentity',
    'V201156':'feelingDemocratic',
    'V201157':'feelingRepublican',
    'V202544':'howOftenUseTwitter'}

    df1 = df1.rename(columns=col_recode)

    #Copy for use later
    df1['V201231x'] = df1['strongIdentif'] 

    ## Recode values
    dic = {-9: None,
           1: 'male',
           2:'female'}

    df1 = df1.replace({'gender': dic})


    dic = {1: 'Alabama',
    2: 'Alaska',
    4: 'Arizona',   
    5: 'Arkansas',
    6: 'California',
    8: 'Colorado',
    9: 'Connecticut',
    10: 'Delaware',
    11: 'Washington DC',
    12: 'Florida',
    13: 'Georgia',
    15: 'Hawaii',
    16: 'Idaho',
    17: 'Illinois',
    18: 'Indiana',
    19: 'Iowa',
    20: 'Kansas',
    21: 'Kentucky',
    22: 'Louisiana',
    23: 'Maine',
    24: 'Maryland',
    25: 'Massachusetts',
    26: 'Michigan',
    27: 'Minnesota',
    28: 'Mississippi',
    29: 'Missouri',
    30: 'Montana',
    31: 'Nebraska',
    32: 'Nevada',
    33: 'New Hampshire',
    34: 'New Jersey',
    35: 'New Mexico',
    36: 'New York',
    37: 'North Carolina',
    38: 'North Dakota',
    39: 'Ohio',
    40: 'Oklahoma',
    41: 'Oregon',
    42: 'Pennsylvania',
    44: 'Rhode Island',
    45: 'South Carolina',
    46: 'South Dakota',
    47: 'Tennessee',
    48: 'Texas',
    49: 'Utah',
    50: 'Vermont',
    51: 'Virginia',
    53: 'Washington',
    54: 'West Virginia',
    55: 'Wisconsin',
    56: 'Wyoming'}

    df1 = df1.replace({'state': dic})


    dic = {-9: None,
           -8: None,
           -2: None,
          1: "Less than high school",
          2: "High school",
          3: "High school",
          4: "Bachelor’s degree",
          5: "Graduate degree"}

    df1 = df1.replace({'education': dic})


    dic = {-2: None,
           1: 'employed',
           2: 'unemployed',
           4: 'unemployed',
           5: 'unemployed',
           6: 'unemployed',
           7: 'unemployed',
           8: 'unemployed'} 

    df1 = df1.replace({'employed': dic})

    dic = {1: 'White',
           2: 'Black',
           3: 'Hispanic',
           4: 'Asian',
           5: 'Native American',
           6: 'Multiple races',
          -9: None,
           -8: None} 

    df1 = df1.replace({'race': dic})

    dic = {1: 'heterosexual',
           2: 'homosexual',
           3: 'bisexual',
           4: None,
          -9: None,
           -5: None} 

    df1 = df1.replace({'sexOrientation': dic})


#     dic = {1: 'Family income below 30k',
#            2: 'Family income below 30k',
#            3: 'Family income below 30k',
#            4: 'Family income below 30k',
#            5: 'Family income below 30k',
#            6: 'Family income 30-60k',
#            7: 'Family income 30-60k',
#            8: 'Family income 30-60k',
#            9: 'Family income 30-60k',
#            10: 'Family income 30-60k',
#            11: 'Family income 60-90k',
#            12: 'Family income 60-90k',
#            13: 'Family income 60-90k',
#            14: 'Family income 60-90k',
#            15: 'Family income 60-90k',
#            16: 'Family income more 90-175k',
#            17: 'Family income more 90-175k',
#            18: 'Family income more 90-175k',
#            19: 'Family income more 90-175k',
#            20: 'Family income more 90-175k',
#            21: 'Family income more 175k',
#            22: 'Family income more 175k',
#            -9: None,
#            -5: None} 
    
#     df1 = df1.replace({'income': dic})

    dic = {-9: None,
           -5: None,
          1:'I never or rarely stop myself from saying something because I think someone might call me a racist, a sexist, or otherwise a bad person',
          2: 'I never or rarely stop myself from saying something because I think someone might call me a racist, a sexist, or otherwise a bad person',
           3: 'I occasionally stop myself from saying something because I think someone might call me a racist, a sexist, or otherwise a bad person',
           4: 'I often stop myself from saying something because I think someone might call me a racist, a sexist, or otherwise a bad person',
           5: 'I often stop myself from saying something because I think someone might call me a racist, a sexist, or otherwise a bad person'} 

    df1 = df1.replace({'selfCensor': dic})


    dic = {-9: None,-5: None}

    df1 = df1.replace({'gunsOwned': dic})

    dic = {-9: None,
           1: "I always or most of the time pay attention to what's going on in government and politics",
           2: "I always or most of the time pay attention to what's going on in government and politics",
           3: "I pay attention to what's going on in government and politics about half the time",
           4: "I pay attention to what's going on in government and politics never or some of the time",
           5: "I pay attention to what's going on in government and politics never or some of the time"}

    df1 = df1.replace({'attentionPolitics': dic})


    dic = {-9: None,
           -8: None,
           -7: None,
           -1: "Didn't vote",
           1: 'Joe Biden',
           2: 'Donald Trump',
           3: None,
           4: None,
           5: None,
           -6: None,
           7: 'Donald Trump',
           8: None,
           11: None,
           12: None,}

    df1 = df1.replace({'vote2020': dic})


    dic = {-9: None,
           -8:None,
           -1:'Didn\t vote',
           1: 'Hillary Clinton',
           2: 'Donald Trump',
           5:  None}

    df1 = df1.replace({'vote2016': dic})

    dic = {-9: None,
           -8:None,
           -1:'Didn\t vote',
           1: 'Barack Obama',
           2: 'Mitt Romney',
           5:  None}

    df1 = df1.replace({'vote2012': dic})


    dic = {-9: None,
           -8: None,
           -4: None,
           -1: None,
           1: 'I consider myself a liberal',
           2: 'I consider myself a conservative',
           3: None}

    df1 = df1.replace({'liberalOrConservative': dic})

    df1['party'] = df1['partyIdentif']
    dic = {-9: 'Not sure',
           -8: 'Not sure',
           -4: 'Not sure',
           0: 'Not sure',
           1: 'Democrat',
           2: 'Republican',
           3: 'Independent',
          5: 'Not sure'}

    df1 = df1.replace({'party': dic})

    dic = {-9: None,
           -8: None,
           -4: None,
           0: None,
           1: 'Democrat',
           2: 'Republican',
           3: 'Independent',
          5: None}

    df1 = df1.replace({'partyIdentif': dic})

    dic = {-9: None,
           -8: None,
           1: 'Strong Democrat',
           2: 'Democrat',
           3: 'Independent who leans Democrat',
           4: 'Independent',
          5: 'Independent who leans Republican',
          6: 'Republican',
          7: 'Strong Republican'}

    df1 = df1.replace({'strongIdentif': dic})

    dic = {-9: None,
           -8: None,
           -1: None,
           1: 'My party is very important to my identity',
           2: 'My party is very important to my identity',
           3: 'My party is moderately important to my identity',
           4: 'My party is not important to my identity',
           5: 'My party is not important to my identity'}

    df1 = df1.replace({'partyIdentity': dic})


    # We select only people who ever use twitter
    df1 = df1.loc[df1['howOftenUseTwitter'].isin((1,2,3,4,5,6))]
    
    #Remove the very small nr of people who did not answer to political affiliation
    # df1 = df1.loc[df1['V201231x']>0]
    
    #Calculate partisanship    
    # Remove the small number of individuals who did not respond to partisan feeling temp
    df1 = df1.loc[(df1['feelingDemocratic']>=0) & (df1['feelingDemocratic']<=100) ]
    df1 = df1.loc[(df1['feelingRepublican']>=0) & (df1['feelingRepublican']<=100) ] 
    # We use the temperature responses for party, to focus on identity and get a -1,1 value for every individual
    df1['partisan'] = (df1['feelingRepublican'] - df1['feelingDemocratic'])/100
    
    ## Function that generates N random people, with WEIGHTING based on the ANES weighting    
    # Note that replacement is key here!
    random_rows = df1.sample(n=number_rows,weights = df1['V200010b'], replace=True) if number_rows is not None else df1
    
    random_dicts = random_rows.to_dict(orient="records")

    #These are the codes for media channels
    # V201634a yahoo.com
    # V201634b cnn.com
    # V201634c huffingpost.com 
    # V201634d nytimes.com
    # V201634e breitbart.com
    # V201634f foxnews.com
    # V201634g washingtonpost.com
    # V201634h theguardian.com
    # V201634i usatoday.com 
    # V201634j bbc.com 
    # V201634k npr.org
    # V201634m dailycaller.com
    # V201634n bloomberg.com
    # V201634p buzzfeed.com
    # V201634q nbcnews.com

    #Here we produce the persona description
    
    res = []
    for d in random_dicts:
        l = {}
        #media sources
        media = ['V201634a','V201634b','V201634c','V201634d','V201634e','V201634f','V201634g','V201634h','V201634i','V201634j','V201634k','V201634m','V201634n','V201634p']
        l['media'] = [m for m in media if d[m]==1]
        
        l['feelingDemocratic'] = d['feelingDemocratic']
        l['feelingRepublican'] = d['feelingRepublican']
        # Normalize the twitter use variable: 
        #NormalizeL: How many times per every second week?
        # 1. Many times every day: 50
        # 2. A few times every day: 30
        # 3. About once a day: 14
        # 4. A few times each week: 5
        # 5. About once a week: 2
        # 6. Once or twice a month: 1
        l['howOftenUseTwitter'] = {1:50, 2:30, 3:14, 4: 5, 5:2, 6:1}[d['howOftenUseTwitter']]
        
        # In your spare time, you like to watch
        hobbies = {'V201631a':'American Idol','V201630r':'NCIS','V201631i':'Good Morning America','V201631r':'Saturday Night Live','V201632c':'Amor Eterno','V201633e':'The Dave Ramsey Show'}
        hobbies_liked = [v for k,v in hobbies.items() if d[k]==1]

        # V201631a PRE: MENTION: TV PROG - AMERICAN IDOL (ABC)
        # V201630r PRE: MENTION: TV PROG - NCIS (CBS)
        # V201631i PRE: MENTION: TV PROG - GOOD MORNING AMERICA (ABC)
        # V201631r PRE: MENTION: TV PROG - SATURDAY NIGHT LIVE (NBC)
        # V201632c PRE: MENTION: TV PROG - AMOR ETERNO
        # V201633e PRE: MENTION: RADIO PROG - THE DAVE RAMSEY SHOW


        l['partisan'] = d['partisan']
        
        # 4 or 5
        feelings = [k for k in ['afraid','outraged','angry','happy','worried','proud','irritated','nervous'] if d[k]==3 or d[k]==4 or d[k]==5]
        
        # ['V201151']
        
        
        
#     dic = {1: 'Family income below 30k',
#            2: 'Family income below 30k',
#            3: 'Family income below 30k',
#            4: 'Family income below 30k',
#            5: 'Family income below 30k',
#            6: 'Family income 30-60k',
#            7: 'Family income 30-60k',
#            8: 'Family income 30-60k',
#            9: 'Family income 30-60k',
#            10: 'Family income 30-60k',
#            11: 'Family income 60-90k',
#            12: 'Family income 60-90k',
#            13: 'Family income 60-90k',
#            14: 'Family income 60-90k',
#            15: 'Family income 60-90k',
#            16: 'Family income more 90-175k',
#            17: 'Family income more 90-175k',
#            18: 'Family income more 90-175k',
#            19: 'Family income more 90-175k',
#            20: 'Family income more 90-175k',
#            21: 'Family income more 175k',
#            22: 'Family income more 175k',
#            -9: None,
#            -5: None} 
        
        
        temps = {
            'feelingDemocratic':'Democrats',
            'feelingRepublican':'Republicans',
            'V201151': 'Joe Biden',
            'V201152': 'Donald Trump',
            'V202168': 'Muslims',
            'V202169': 'Christians',
            'V202170': 'Jews',
            'V202171': 'Police',
            'V202172': 'transgender people',
            'V202173': 'scientists',
            'V202174': 'Black Lives Matter',
            'V202175': 'journalists',
            'V202178': 'NRA',
            'V202184': 'rural Americans',        
            'V202158': 'Anthony Fauci',
            'V202159': 'Christian Fundamentalists',
            'V202160': 'feminists',
            'V202161': 'liberals',
            'V202164': 'conservatives',
            'V202166': 'homosexuals'}
        
        lovelist = []
        hatelist = []
        for k,v in temps.items():
            if d[k] >= 0 and d[k] <= 10:
                hatelist.append(v)
            if d[k] <= 100 and d[k] >= 90:
                lovelist.append(v)
        
        #Create persona string
        l['persona'] = "Here is a description of your persona: \n"

        if d['gender'] is not None:
            l['persona'] += f"You are {d['gender']}.\n"
            
            
        if d['income'] is not None and d['income']>0:
            if d['income'] >= 1 and d['income'] <= 10:
                incomeclass = 'low income'
            elif d['income'] >= 11 and d['income'] <= 20:
                incomeclass = 'middle income'
            else:
                incomeclass = 'high income'
            l['persona'] += f"You are {incomeclass}.\n"
        
            
        if d['V201507x'] is not None:
            l['persona'] += f"Age: {d['V201507x']}.\n" 
        
        religions = {1: 'Protestant', 2: 'Evangelical Protestant', 3: 'Black Protestant', 4: 'Protestant',  5: 'Catholic', 6: 'Christian', 7: 'Jewish', 9: 'not religious'}
        l['V201458x'] = d['V201458x']
        if d['V201458x'] in list(religions.keys()):
            l['persona'] += f"You are {religions[d['V201458x']]}.\n"
        
        if d['state'] is not None:
            l['persona'] += f"You are from {d['state']}.\n"
        if d['education'] is not None: 
            l['persona'] += f"Education: {d['education']}.\n"
        # if d['employed'] is not None: 
            # l['persona'] += f"You are {d['employed']}.\n"
        if d['race'] is not None: 
            l['persona'] += f"You are {d['race']}.\n"
        if d['sexOrientation'] is not None: 
            l['persona'] += f"You are {d['sexOrientation']}.\n"

        l['race'] = d['race'] 
        
        l['party'] = 'Democrat' if l['partisan'] < 0 else 'Republican' if l['partisan'] > 0 else 'Non-partisan'        
        
        #People who never talk about politics: we add other preferences
        if d['V202545'] == 5: # V202023
            l['persona'] += "You never talk about politics.\n" #
            l['never_talk_politics'] = True
            
            l['party'] = 'Non-partisan'
            l['partisan'] = 0
            
            #Fishing
            if d['V202567'] == 1:
                l['persona'] += "You like to go fishing or hunting.\n" #
                               
        #They do talk about politics 
        else:
            l['never_talk_politics'] = False
            
            if d['vote2020'] in ['Donald Trump','Joe Biden']:
                l['persona'] += f"You voted for {d['vote2020']} in 2020.\n"
            else:
                l['persona'] += "You didn't vote in 2020.\n"
                
                
            # OLD WAY OF ASSIGNING PARTY
            # l['party'] = 'Democrat' if d['V201231x'] in [1,2,3] else 'Republican' if d['V201231x'] in [5,6,7] else 'Independent' if d['V201231x'] == 4 else 'None'
            
            
            # if d['strongIdentif'] is not None: 
            #     l['persona'] += f"You are a {d['strongIdentif']}.\n"
        
            #This worked poorly
            # l['persona'] += f"On a scale from -100 to 100, where -100 is extremely Democratic and 100 is extremely Republican, you are: {d['partisan']}.\n"
        
            
            #Generate party affiliation
            if l['partisan'] == 0:
                l['persona'] += 'You prefer neither political party.\n'
            if l['partisan'] < 0 and l['partisan'] > -0.2:
                l['persona'] += 'You prefer the Democrats.\n'
            if l['partisan'] > 0 and l['partisan'] < 0.2:
                l['persona'] += 'You prefer the Republicans.\n'
            if l['partisan'] <= -0.2 and l['partisan'] > -0.5:
                l['persona'] += 'You are a Democrat.\n'
            if l['partisan'] >= 0.2 and l['partisan'] < 0.5:
                l['persona'] += 'You are a Republican.\n'
            if l['partisan'] <= -0.5:
                l['persona'] += 'You are a strong Democrat.\n'
            if l['partisan'] >= 0.5:
                l['persona'] += 'You are a strong Republican.\n'           
            
            if d['justifiedViolence'] in [3,4,5]:
                l['persona'] += "You think political violence is justified.\n"

            if len(lovelist)>0:
                l['persona'] += f'You love {format_list(lovelist)}.\n'

            if len(hatelist)>0:
                l['persona'] += f'You hate {format_list(hatelist)}.\n'            

        #You post online a lot or always about politics, or you get into political argument in the last 12 months
        if d['V202545']== 1 or d['V202545']== 2: #d['V202024']== 1 or 
            l['persona'] += "You like to argue about politics.\n"
            
        
        if len(feelings)>0:
            l['persona'] += f"You feel {format_list(feelings)} about your country.\n"

        if len(hobbies_liked)>0:
            l['persona'] += f'You like to watch {format_list(hobbies_liked)} on TV.\n'

        l['attribs'] = {key: d[key] for key in ['gender','state','education','feelingDemocratic','feelingRepublican','V202023','race','strongIdentif']}
        l['attribs']['hobbies_liked'] = hobbies_liked
        l['attribs']['media'] = l['media']
        
        res.append(l)


    return res

if __name__ == "__main__":
    
    #Example usage
    personas = get_anes_rows(2)
    print(personas[1]['persona'])
