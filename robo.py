# use natural language toolkit
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
# word stemmer
stemmer = LancasterStemmer()



# 3 classes of training data
training_data = []
training_data.append({"class":"order", "sentence":"i'll have a salad please"})
training_data.append({"class":"order", "sentence":"i'll take the salad"})
training_data.append({"class":"order", "sentence":"can I have the roasted chicken?"})
training_data.append({"class":"order", "sentence":"can I get the roasted chicken?"})
training_data.append({"class":"order", "sentence":"i'll take spaghetti and meetballs"})
training_data.append({"class":"order", "sentence":"i'll have the spaghetti and meetballs"})
training_data.append({"class":"order", "sentence":"I'll have a pizza pie"})
training_data.append({"class":"order", "sentence":"I'll take a slice of pizza"})
training_data.append({"class":"order", "sentence":"I'll have the carbonara"})
training_data.append({"class":"order", "sentence":"Can I get the carbonara"})

training_data.append({"class":"intermediary", "sentence":"Can I get a few more moments?"})
training_data.append({"class":"intermediary", "sentence":"I am still deciding."})
training_data.append({"class":"intermediary", "sentence":"Give me a minute."})
training_data.append({"class":"intermediary", "sentence":"Sorry, can I have a few more moments."})
training_data.append({"class":"intermediary", "sentence":"Could you come back in a few minutes"})
training_data.append({"class":"intermediary", "sentence":"I don't know"})
training_data.append({"class":"intermediary", "sentence":"What is good here?"})

training_data.append({"class":"drink", "sentence":"I'll have water please"})
training_data.append({"class":"drink", "sentence":"Water will be just fine"})
training_data.append({"class":"drink", "sentence":"lemonade"})
training_data.append({"class":"drink", "sentence":"I'll have a glass of wine"})
training_data.append({"class":"drink", "sentence":"beer world be good"})
training_data.append({"class":"drink", "sentence":"I'm good"})
training_data.append({"class":"drink", "sentence":"tea"})
training_data.append({"class":"drink", "sentence":"coffee"})

training_data.append({"class":"update", "sentence":"yes, everything is fine"})
training_data.append({"class":"update", "sentence":"yes, the food is great"})
training_data.append({"class":"update", "sentence":"the food was excellent"})
training_data.append({"class":"update", "sentence":"the food is good"})
training_data.append({"class":"update", "sentence":"can i have some more water please"})
training_data.append({"class":"update", "sentence":"can i have some more napkins please"})

training_data.append({"class":"readyToGo", "sentence":"check please"})
training_data.append({"class":"readyToGo", "sentence":"can i have the check?"})
training_data.append({"class":"readyToGo", "sentence":"excuse me, can we have the check?"})
training_data.append({"class":"readyToGo", "sentence":"bill please"})
training_data.append({"class":"readyToGo", "sentence":"can I get the bill please"})
training_data.append({"class":"readyToGo", "sentence":"excuse me, can we get the bill?"})

training_data.append({"class":"myself", "sentence":"What are you?"})
training_data.append({"class":"myself", "sentence":"Who are you?"})
training_data.append({"class":"myself", "sentence":"What do you do?"})
training_data.append({"class":"myself", "sentence":"I'm curious. What are you?"})
training_data.append({"class":"myself", "sentence":"Are you related to siri?"})

training_data.append({"class":"goodbye", "sentence":"Goodbye"})
training_data.append({"class":"goodbye", "sentence":"Goodday"})
training_data.append({"class":"goodbye", "sentence":"Thanks for the service"})

corpus_words = {}
class_words = {}
response_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []
    response_words[c] = []

# loop through each sentence in our training data to add to our bag
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1          #1 occurence of word
            else:
                corpus_words[stemmed_word] += 1         #more than 1 occurence, increase counter

            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])

# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
#print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class

# calculate a score for a given class taking into account word commonality
def calculate_class_score_commonality(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):                           #parse sentence into words and loop through each word
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score



# return the class with highest score for sentence
def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():                    #go trough class words dictionary
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    decision(high_class, sentence)
    return



def decision(high_class, sentence):
    #based on intent we make decisions
    if high_class == "order":
        print("Coming right up")  # select random response from list
        print("Would that be all?")
        classify(input()) #after input, set drink to true
    elif high_class == "drink":
        print("Sure, I'll be right back with your drink")
        print("Here you go, will that be all?")
        classify(input())
    elif high_class == "intermediary":
        print("Alright, Just tell me when your ready")
        classify(input())
    elif high_class == "readyToGo":
        print("I'll be right back with the check")
        print("Here you are")
        classify(input()) #acknowledge
    elif high_class == "myself":
        print("I Robo the chatbot. I am designed to be your waiter for this establishment so that there is no need to speak upfront. ")
        print("This inspiriation came from the store ichiran where you do not have to speak to anyone at all.")
        classify(input())
    elif high_class == "update":
        if sentence.find("great") != -1:
            print("That is great to hear")
            classify(input())
        elif sentence.find("good") != -1:
            print("That is great to hear")
            classify(input())
        elif sentence.find("excellent") != -1:
            print("That is great to hear")
            classify(input())
        elif sentence.find("water") != -1:
            print("Of course, I'll be right back with more water.")
            print("Will that be all?")
            classify(input())
        elif sentence.find("napkins") != -1:
            print("Of course, I'll be right back with your napkins.")
            print("Is that all?")
            classify(input())
        else:
            print("Alright.")
            classify(input())
    elif high_class == "goodbye":
        print("Thank you for eating at our establishment tonight.")
        print("Have a wonderful evening.")
    return


#based on classification we want a response
#see how well user input matches with response
#if no appropriate response is found, say "soory, i do not understand"

#rate each sentence and high class is picked, then pick best one
#create a list of high class sentences
#see how well user input matches

flag=True
while flag==True:
    print("Hello, my name is robo. I'll be your waiter tonight. How can I help you?")
    user_response = input()
    print(classify(user_response))
#flag = False
