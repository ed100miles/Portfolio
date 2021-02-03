import datetime as datetime

def initialise_board():
    board = []
    for x_coord in range(15):
        for y_coord in range(15):
            board.append([x_coord, y_coord, ""])    
    return board

def get_move():
    played_word = input("what word did you play?: ")
    word_start_x = int((input("for your first letter played, what was your X co-ordinate?: ")))
    word_start_y = int((input("for your first letter played, what was your Y co-ordinate?: ")))
    down_or_across = input("did you play down or across? (d/a): ")
    return played_word, word_start_x, word_start_y, down_or_across
    # played_word, word_start_x, word_start_y, down_or_across = get_move()

def is_there_room(board, played_word, word_start_x, word_start_y, down_or_across):
    played_word_length = len(played_word)
    if down_or_across == "a":
        space = (14 - word_start_y)
        if space < played_word_length:
            print("that word's too long...")
            enough_room = False
        else:
            enough_room = True

    if down_or_across == "d":
        space = (14 - word_start_x)
        if space < played_word_length:
            print("that word's too long...")
            enough_room = False
        else:
            enough_room = True
    return enough_room
    # enough_room = is_there_room(board, played_word, word_start_x, word_start_y, down_or_across)

def play_move(enough_room, board, played_word, word_start_x, word_start_y, down_or_across):
    if enough_room == True:
        if down_or_across == "d":
            x = int(word_start_x)
            y = int(word_start_y)
            for char in played_word:
                for element in board:
                    if (element[0] == x) and (element[1] == y):
                        element[2] = char.upper()
                x += 1

        if down_or_across == "a":
            x = int(word_start_x)
            y = int(word_start_y)
            for char in played_word:
                for element in board:
                    if (element[0] == x) and (element[1] == y):
                        element[2] = char.upper()
                y += 1

    return board

def wordDefiner(wordsToDefine):

    wordsList = list((open("/home/ed/Documents/VSCode/scrabbler/ScrabbleCheater1.0/scrabbleWordsAndDef.txt")).read())

    word = ""
    listOfWords = []

    for char in wordsList:
        if char != "\n":
            word = str(word) + str(char)
        else:
            listOfWords.append(str(word.lower()))
            word = ""

    wordAndDefList = []

    for wordAndDef in listOfWords:
        wordAndDefList += [wordAndDef.split("\t")]

    definitions = []

    for index_word in wordsToDefine:
        for index_word_def in wordAndDefList:
            if index_word.lower() == index_word_def[0]:
                definitions.append(index_word_def)
    
    return definitions

def wordScorer(results):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    scores_dict = {'a':1, 'e':1, 'i':1, 'o':1, 'u':1, 'l':1, 'n':1, 's':1, 't':1, 'r':1, 'd':2, 'g':2, 'b':3, 'c':3, 'm':3, 'p':3, 'f':4, 'h':4, 'v':4, 'w':4, 'y':4, 'k':5, 'j':8, 'x':8, 'q':10, 'z':10}
    word_score = []

    for word in results:
        score = 0
        word_letters = dict.fromkeys(list(alphabet), 0)
        for letter in word:
            word_letters[letter] += 1
        
        for key in word_letters:
            score += (scores_dict[key])*(word_letters[key])

        word_score.append([word, score])

    return(word_score) 

def wordRanker(words_with_scores):
    results = []
    def takeSecond(elem):
        return elem[1]
    words_with_scores.sort(key=takeSecond, reverse=True)
    for x in words_with_scores:
        wordScore = [x[0], x[1]]
        results += [wordScore]       
    return results

def wordFinder(user_input, board):
    valid_words = set()
    wordsList = list((open("/home/ed/Documents/VSCode/scrabbler/ScrabbleCheater1.0/scrabbleWords.txt")).read())
    word = ""
    listOfWords = []
    board_letters = set()

    for char in wordsList:
        if char != "\n":
            word = str(word) + str(char)
        else:
            listOfWords.append(str(word.lower()))
            word = ""

    for element in board:
        board_letters.add(element[2])

    for board_letter in board_letters:
        user_input_and_board_letter = user_input + board_letter.lower()
        for theWord in listOfWords:
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            user_letters_dict = dict.fromkeys(list(alphabet), 0)
            listOfWords_dict = dict.fromkeys(list(alphabet), 0)

            for i in range(len(user_input_and_board_letter)):
                user_letters_dict[user_input_and_board_letter[i]] += 1

            for i in range(len(theWord)):
                listOfWords_dict[theWord[i]] += 1

            missing_letters = 0

            for x in user_letters_dict:
            
                if user_letters_dict[x] < listOfWords_dict[x]:
                    missing_letters += 1
                    break

            if missing_letters == 0:
                valid_words.add(theWord)

    return valid_words

#board = initialise_board()
#
#user_input = ""
#
#while user_input != "0":
#
#    user_input = input("What now? \n 1) Find a word \n 2) Define a word \n 3) Play a word \n 4) Show the board \n 5) Reset the board \n 0) Quit \n ---------> ")
#
#    if user_input == "0":
#        user_input = input("Are you sure you want to quit? (yes/no) :")
#        if user_input.lower() in ("yes", "y"):
#            break
#
#    if user_input == "1":
#        user_input = input("what are your letters?: ")
#        found_words = wordFinder(user_input, board)
#        words_with_scores = wordScorer(found_words)
#        print(wordRanker(words_with_scores))
#
#    if user_input == "2":
#        user_input = input("what word do you want defined?")
#        print(wordDefiner([user_input]))
#
#    if user_input == "3":
#        played_word, word_start_x, word_start_y, down_or_across = get_move()
#        enough_room = is_there_room(board, played_word, word_start_x, word_start_y, down_or_across)
#        board = play_move(enough_room, board, played_word, word_start_x, word_start_y, down_or_across)
#    
#    if user_input == "4":
#        print(board)
#    
#    if user_input == "5":
#        board = initialise_board()
#
#print("See ya!")



