
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
    features
from watson_developer_cloud.watson_developer_cloud_service import WatsonException
from pip._vendor.requests.exceptions import ConnectionError
from pip._vendor.requests.packages.urllib3.exceptions import NewConnectionError
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

while True:
    print "Make sure you are connected to internet\n"
    print "Enter watson login details:\n"
    print "Username:"
    input_username=raw_input()
    print "Password:"
    input_passsword=raw_input()
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username=input_username,
    password=input_passsword)
    ## test trial to confirm valid login credentials
    try:
        response = natural_language_understanding.analyze(text='Bruce Banner is the Hulk and Bruce Wayne is BATMAN! ''Superman fears not Banner, but Wayne.',
        features=[features.Emotion()])
        print "YOU ARE NOW TALKING TO KARRMA BOT\n\n"
        break
    except WatsonException:
        print "Username or password invalid, try again\n"
    except ConnectionError:
        print "Check your internet connection"
    except NewConnectionError:
        print "Check your internet connection"

######################################## TRAINING THE BOT #####################################

## angry bot
hitler_file= open("hitler.txt", 'r')
conversation_hitler= hitler_file.readlines
conversation_hitler=[x[1:-3] for x in conversation_hitler]
angry_bot = ChatBot("Hitler", read_only =True, filters=["chatterbot.filters.RepetitiveResponseFilter"],
    logic_adapters=[
        "chatterbot.logic.BestMatch"]) 

angry_bot.set_trainer(ListTrainer)
angry_bot.train(conversation_hitler)

##joy bot
teresa_file= open("mother_teresa.txt", 'r')
conversation_teresa= teresa_file.readlines
conversation_teresa=[x[1:-3] for x in conversation_teresa]
joy_bot = ChatBot("Joy bot", read_only =True, filters=["chatterbot.filters.RepetitiveResponseFilter"],
    logic_adapters=[
        "chatterbot.logic.BestMatch"])

joy_bot.set_trainer(ListTrainer)
joy_bot.train(conversation_teresa)

### fear bot
depressed_file= open("depressed_maria.txt", 'r')
conversation_depressed = depressed_file.readlines
conversation_depressed =[x[1:-3] for x in conversation_hitler]
fear_bot = ChatBot("Depressed Maria", read_only =True, filters=["chatterbot.filters.RepetitiveResponseFilter"],
    logic_adapters=[
        "chatterbot.logic.BestMatch"])

fear_bot.set_trainer(ListTrainer)
fear_bot.train(conversation_depressed)

## Disgust bot
disgust_bot = ChatBot("Disgust bot", read_only =True, filters=["chatterbot.filters.RepetitiveResponseFilter"],
    logic_adapters=[
        "chatterbot.logic.BestMatch"])
conversation_disgust=[
    ]

disgust_bot.set_trainer(ListTrainer)
disgust_bot.train(conversation_disgust)

##sadness bot
sad_bot = ChatBot("Sadness Bot", read_only =True, filters=["chatterbot.filters.RepetitiveResponseFilter"],
    logic_adapters=[
        "chatterbot.logic.BestMatch"])
conversation_sad=[
    ]

sad_bot.set_trainer(ListTrainer)
sad_bot.train(conversation_sad)
######## Analyzing text emotions and giving accordingly same response

while True:
    
    input_text= raw_input()
    try:
        response = natural_language_understanding.analyze(text= input_text,features=[features.Emotion()], language= "en")
    except ConnectionError:
        print "Check your internet connection and then try again"
        continue
    except NewConnectionError:
        print "Check your internet connection"
        continue
    OutputStr=(json.dumps(response, indent=2))
    OutputStr= OutputStr.split(' ')
    ## storing values in different variable for use
    max_emotion=""                              ##stores the emotion which is maximum in input sentence
    max_emotion_value=0.0
    for index, word in enumerate(OutputStr):
        if '"anger":' == word:
            anger = OutputStr[index+1]
            if anger>max_emotion_value:
                max_emotion_value = anger
                max_emotion = "anger"
                
        if '"joy":' == word:
            joy = OutputStr[index+1]
            if joy>max_emotion_value:
                max_emotion_value = joy
                max_emotion = "joy"
        if '"fear":' == word:
            fear = OutputStr[index+1]
            if fear>max_emotion_value:
                max_emotion_value = fear
                max_emotion = "fear"
        if '"disgust":' == word:
            disgust = OutputStr[index+1]
            if disgust>max_emotion_value:
                max_emotion_value = disgust
                max_emotion = "disgust"
        if '"sadness":' == word:
            sadness = OutputStr[index+1]
            if sadness>max_emotion_value:
                max_emotion_value = sadness
                max_emotion = "sadness"
    print max_emotion
    if max_emotion=="anger":
        print "Hitler triggered"
        print angry_bot.get_response(input_text)
    elif max_emotion == "joy":
        print "Mother Teresa triggered"
        print joy_bot.get_response(input_text)
    elif max_emotion == "fear":
        print "Maria, depressed girl triggered"
        print fear_bot.get_response(input_text)
    elif max_emotion == "disgust":
        print "Disgust bot trigerred"
        print disgust_bot.get_response(input_text)
    elif max_emotion == "sadness":
        print "Sad bot trigerred"
        print sad_bot.get_response(input_text)
      
    ##print "Immediate Emotions: \n" + "anger: " + anger + "\njoy: " + joy + "\nfear: " + fear + "\ndisgust: " + disgust + "\nsadness: " + sadness
    ##print "\nMax: "+ max_emotion + max_emotion_value
    
    
    