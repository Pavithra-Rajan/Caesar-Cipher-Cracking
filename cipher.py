from collections import Counter
import argparse

def char_replace_lower(line, to_be_replaced, to_be_replaced_with = ''):
    '''
    This function will replace a character with another character ('' by default) and convert
    to lower case.
    Args:
        line (str): A string
        to_be_replaced (str): The character to be replaced
        to_be_replaced_with (str): The new character that should be in place of the above character
    Return:
        A string with the required character replaced
    '''
    return line.replace(to_be_replaced, to_be_replaced_with).lower()

def read_message(file_name):
    '''
    This function will read the message from a given text file.
    Assumption: No other special characters apart from '.' and ',' which will be replaced.
    Args:
        file_name (str): The file from which the message is to be read
    Return:
        The message read from the txt file and pre-processed
    '''
    message = ''
    f = open(file_name, 'r')
    for line in f:
        line = char_replace_lower(line, '.')
        line = char_replace_lower(line, ',')
        message += char_replace_lower(line, '\n', ' ')
    return message

def print_stdout(text):
    '''
    This function is just used for stdout printing to separate each section.
    Args:
        text (str): The text to be printed into stdout console.
    '''
    line = 25 * "-"
    print(line + text + line)

class CaesarCipher:

    def __init__(self):
        '''
        This is the initialising constructor.
        self.alpha_dict (dictionary): A dictionary of all the alphabets mappet to corresponding indices. Space is given an index too.
        self.alpha_dict_complement (dictionary): Index to alphabet mapping dictionary.
        self.freq_dict (dictionary): An empty dictionary initialised to store the computed frequency distribution of english alphabets.
        self.frequency_csv_read (function): To read the alphabet frequency CSV file.
        '''
        self.alpha_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
        'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14,'p': 15, 'q': 16, 'r': 17, 
        's': 18, 't': 19, 'u': 20,'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, ' ': 26}
        self.alpha_dict_complement = {v: k for k, v in self.alpha_dict.items()}
        self.freq_dict = {}
        self.bigram_dict = {}
        self.frequency_csv_read()
        self.bigram_csv_read()

    def monoalpha_shift(self, letter, n):
        '''
        This function shifts a letter by 'n' and returns the new letter.
        As space is there, z will shift to space if n = 1.
        Args:
            letter (str): The letter to be shifted
            n (int): The rotation factor
        Return:
            A letter after rotating by a factor of n.
        Mod 27 is taken because 26 alphabets  + space
        '''
        position = self.alpha_dict[letter] 
        return self.alpha_dict_complement[(position + n) % 27]  

    def encode_caesar(self, message, n):
        '''
        This function encodes a message by monoalphabetic shift of each character of it.
        Args:
            message (str): The message to be encoded
            n (int): The rotation factor
        Return:
            The cipher text
        '''
        cipher = ""

        for m in message:
            c = self.monoalpha_shift(m, n)
            cipher += c
        return cipher

    def decode_caesar(self, cipher_text, n):
        '''
        This function decodes a message by monoalphabetic shift of each character of it.
        Args:
            cipher_text (str): The cipher text to be decoded
            n (int): The rotation factor
        Return:
            The plain text
        '''
        plain_text = ""
        for c in cipher_text:
            p = self.monoalpha_shift(c, n * -1)
            plain_text += p
        return plain_text

    def frequency_csv_read(self):
        '''
        This function reads the CSV file to get the frequency of each alphabet.
        '''
        file = 'letter_frequencies.csv'
        f = open(file, "r+")

        for line in f:
            line = line.lower().replace("\n", "")
            k, v = line.split(",")
            self.freq_dict[k] = float(v)

        f.close()
        #print(self.freq_dict)

    def score_string(self, string):
        '''
        This function computes the frequency distribution value of the string.
        Args:
            string (str): The message to be evaluated
        Return:
            The frequency score
        '''
        score = 0.0
        for ch in string:
            score += self.freq_dict[ch]

        return score

    def crack_caesar_frequency(self, cipher_text):
        '''
        This function attempts to crack the caesar cipher using the frequency distribution.
        The outcome which gives the maximum score when evaluated is accepted.
        Args:
            cipher_text (str): The cipher text
        Return:
            The cracked plain text and 'n' rotation factor
        '''
        #List to store each decode possibility
        decode_list = []
        #List to store the frequency score of each decode
        decode_scores = []

        for i in range(len(self.alpha_dict)):
            plain = ""
            for c in cipher_text:
                p = self.monoalpha_shift(c, i * -1)
                plain += p

            decode_list.append(plain)
            decode_scores.append(self.score_string(plain))
    
        max_score = 0
        max_score_index = -1
        for i in range(len(self.alpha_dict)):
            if decode_scores[i] > max_score:
                max_score = decode_scores[i]
                max_score_index = i

        return decode_list[max_score_index], max_score_index
    
    def crack_caesar_27n(self, cipher_text, i):
        '''
        This function tries to crack the Caesar cipher by trying all 27 possibilities.
        Args:
            cipher_text (str): The cipher text to be decoded
            i: The rotation factor
        Return:
            The shifted cipher text.
        '''
        plain_text = ""

        for c in cipher_text:
            p = self.monoalpha_shift(c, i * -1)
            plain_text += p
        return plain_text
 
    def bigram_csv_read(self):
        '''
        This function reads the CSV file to get the bigram frequency.
        '''
        file = 'bigram_frequency.csv'
        f = open(file, "r+")

        for line in f:
            line = line.lower().replace("\n", "")
            k, v = line.split(",")
            self.bigram_dict[k] = float(v)
        #print(self.bigram_dict)
        f.close()
    
    def bigram_score(self, cipher):
        '''
        This function computes the bigram frequency distribution value of the string.
        Args:
            string (str): The message to be evaluated
        Return:
            The bigram frequency score
        '''
        score = 0.0
        # create a bigram frequency dictionary of the ciphertext
        bigram_freq = Counter(cipher[idx : idx + 2] for idx in range(len(cipher) - 1))
        sorted_bigram ={k: v for k, v in sorted(dict(bigram_freq).items(), key=lambda item: item[1])}
        
        for k in sorted_bigram.keys():
            try:
                #possible that not all bigrams in the dictionary so escape those
                score += self.bigram_dict[k]
            except:
                pass

        return score
        #bigram_freq = Counter(cipher[idx : idx + 2] for idx in range(len(cipher) - 1))
        #return {k: v for k, v in sorted(dict(bigram_freq).items(), key=lambda item: item[1])}

    def crack_caesar_bigram(self, cipher_text):
        '''
        This function attempts to crack the caesar cipher using the bigram frequency distribution.
        The outcome which gives the maximum score when evaluated is accepted.
        Args:
            cipher_text (str): The cipher text
        Return:
            The cracked plain text and 'n' rotation factor
        '''
        #List to store each decode possibility
        decode_list = []
        #List to store the frequency score of each decode
        decode_scores = []

        for i in range(len(self.alpha_dict)):
            plain = ""
            for c in cipher_text:
                p = self.monoalpha_shift(c, i * -1)
                plain += p

            decode_list.append(plain)
            decode_scores.append(self.bigram_score(plain))

        max_score = 0
        max_score_index = -1
        for i in range(len(self.alpha_dict)):
            if decode_scores[i] > max_score:
                max_score = decode_scores[i]
                max_score_index = i

        return decode_list[max_score_index], max_score_index


parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, required=True, help="Name of the file containing the plaintext to be encrypted")
parser.add_argument('-c', type=int, required=True, help="The Caesar rotation factor")
parser.add_argument('-n', type=str, help="Name to be encoded")
args = parser.parse_args()
message_file = args.f
#print(args.n)
n = args.c
name = args.n
cipher_obj = CaesarCipher()
print_stdout("Read Plain Text")
message = read_message(message_file)
message = message + " " + name

cipher_text = cipher_obj.encode_caesar(message, n)
print('Encrypted Cipher Text:', cipher_text[:-1 * len(name)])

decoded_message = cipher_obj.decode_caesar(cipher_text[:-1 * len(name)], n)
print('Decoded Message:', decoded_message)

print_stdout("Encoding name")
print(f'Ciphertext corresponsding to {name}: {cipher_text[-1 * len(name):]}')

print_stdout("Cracking using frequency analysis")
cracked, n = cipher_obj.crack_caesar_frequency(cipher_text)
print('Cracked Cipher Text:', cracked[:-1 * len(name)])
print('Cracked name:', cracked[-1 * len(name):])
print(f"The value of n is: {n}")

print_stdout("Cracking using bigram analysis")
cracked, n = cipher_obj.crack_caesar_bigram(cipher_text)
print('Cracked Cipher Text:', cracked[:-1 * len(name)])
print('Cracked name:', cracked[-1 * len(name):])
print(f"The value of n is: {n}")

print_stdout("Cracking using mono-alphabetic substitution")
op = 'n'

for i in range(1,27):
    print(f"Iteration number: {i}")
    cracked = cipher_obj.crack_caesar_27n(cipher_text, i)
    print('Cracked Cipher Text:', cracked[:-1 * len(name)])
    print_stdout(30 * "-")
    op = input("Type 'y' if it seems valid, else 'n': ")

    if op == 'y':
        print('Cracked name:', cracked[-1 * len(name):])
        break