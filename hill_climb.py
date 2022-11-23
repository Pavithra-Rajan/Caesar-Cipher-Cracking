from random import shuffle, randint
from math import log10
import sys
import argparse
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import string
import matplotlib.pyplot as plt
import networkx as nx

def frequency_csv_read():
    '''
    This function reads the CSV file to get the frequency of each alphabet.
    '''
    file = 'frequencies/letter_frequencies.csv'
    f = open(file, "r+")
    freq_dict = {}
    for line in f:
        line = line.lower().replace("\n", "")
        k, v = line.split(",")
        freq_dict[k] = float(v)

    f.close()
    return freq_dict

def create_labels(score_list, edge):
    '''
    This function creates the labels for the networkx graph edges.
    Args:
        score_list (list): List of the scores obtained via letter frequency/bigram frequency
        edge (list[list]): A list containing pair list of each edge
    Return:
        labels which is a dict{tuple: value}
    '''
    labels = {}
    count = 0
    for i in edge:
        test = (i[0], i[1])
        labels[test] = score_list[count]
        count = count + 1
    #print(labels)
    return labels

def create_straight_graph(selected, root, labels):
    '''
    This function creates a straight graph with no edge labels
    Args:
        selected (int): The 'n' caesar rotation value chosen
        root (str): The root of the graph
        labels (list): A list of labels for the edges
    '''

    edge = [[root, 1]]
    for i in range(1,selected[-1]):
        edge.append([i, i+1])
    #print(edge)
    G = nx.Graph()
    G.add_edges_from(edge)
    pos = nx.spring_layout(G, scale=5)
    plt.figure()

    #color_map = ['yellow' if node in selected else 'pink' for node in G]  
    color_map =[]
    for node in G:
        if node == selected[-1]:
            color_map.append('green')

        elif node in selected:
            color_map.append('yellow')
        
        else:
            color_map.append('pink')
         
    #graph = nx.draw_networkx(G,pos, node_color=color_map) # node lables

    nx.draw(
        G, pos, edge_color='black', width=1, linewidths=1,
        node_size=400, node_color=color_map, alpha=0.9,
        labels={node: node for node in G.nodes()}
    )
    nx.draw_networkx_edge_labels(G, pos, 
    edge_labels = create_labels(labels, edge), font_color='red', font_size=8,
    rotate=False)

    plt.savefig("states/" + "soln" + ".png")

def swap_chars(key):
    '''
    This function swaps the letters present in a key of two randomly selected indices.
    Args:
        key (str): The key used for decryption
    Return:
        The modified key
    '''
    i = randint(0, 25)
    j = randint(0, 25)
    key[i], key[j] = key[j], key[i]
    return key

def decrypt(cipher, key):
    '''
    This function takes in the ciphertext and the decyphering key to return the plaintext.
    Args:
        cipher (str): The ciphertext
        key (str): The key used for decryption
    '''
    #print(''.join(frequency_csv_read().keys()))
    letter_freq = ''.join(frequency_csv_read().keys())[:26].upper()
    plaintext = ''

    for c in cipher:
        plaintext += letter_freq[key.index(c)]

    return plaintext

def plot_hill_graph(iters, fitness_values):
    '''
    This function plots a graph of the fitness score values obtained across iterations.
    Args:
        iters (list): A list of all the iteration values
        fitness_values (list): A list of all the fitness score values
    '''
    x = np.array(iters)
    y = np.array(fitness_values)

    cubic_interpolation_model = interp1d(x, y, kind = "cubic")
    X_=np.linspace(x.min(), x.max(), 500)
    Y_= cubic_interpolation_model(X_)

    plt.plot(X_, Y_)
    plt.title("Decrypted Ciphertext across iterations")
    plt.xlabel("Iterations")
    plt.ylabel("Decryption score")
    plt.savefig("states/hillclimbing.png")

def crack_caesar_quad(cipher, name_length, enc_name, max_iter = 1000):
    '''
    This is an auxiliary function to crack the ciphertext.
    Args:
        cipher (str): The ciphertext
        max_iter (int): default 1000, the maximum iterations for which the cryptanalysis is to be performed
    '''
    cipher_obj = HillClimbing('frequencies/english_quadgrams.txt')
    bestkey = None
    bestfit = -1 * float('inf')

    fitness_values = []
    iters = []

    itr = 0
    name_crack = []
    local_max = []

    while True:
        try: 
            node = list(string.ascii_uppercase)
            shuffle(node)
            node_score = cipher_obj.score(decrypt(cipher, node))
            
            itr = itr + 1
            for i in range(max_iter):
                child = node.copy()
                child = swap_chars(child)
                child_score = cipher_obj.score(decrypt(cipher, child))

                if child_score > node_score:
                    #swap parent node and child if child score is better
                    node = child
                    node_score = child_score

            if node_score > bestfit:
                bestfit = node_score
                bestkey = node
                print('Iteration: ', itr)
                print('Best score so far:', node_score)
                cracked = decrypt(cipher, node).lower()
                print('Cracked Cipher Text:', cracked, '\n')
                print('Cracked Name Text:', cracked[-1 * name_length:], '\n')
                local_max.append(itr)

            name_crack.append(cracked[-1 * name_length:]) 
            fitness_values.append(node_score)
            iters.append(itr)
            
        except KeyboardInterrupt:
            print('End of decryption')
            print(f"The rotation factor is {abs(ord(enc_name[0])-ord(name_crack[-1][0]))}")
            plot_hill_graph(iters, fitness_values)
            create_straight_graph(local_max, "root", name_crack)
            #print(name_crack)
            #print(local_max)
                      
            sys.exit()

class HillClimbing:
    
    def __init__(self, file_name):
        '''
        This is the initialising constructor.
        Args:
            file_name (str): The file to obtain the quadgram frequencies.
        '''
        self.quadgram = {}

        for line in open(file_name).readlines():
            key,count = line.split(' ') 
            self.quadgram[key] = int(count) # explicitely convert to int to take sum

        self.length = len(key) # it is 4 because quadgrams are used
        #print(self.length)
        self.total_frequency = sum(self.quadgram.values())

        #compute log of frequency %
        for key in self.quadgram.keys():
            self.quadgram[key] = log10(float(self.quadgram[key])/self.total_frequency)
        self.floor = log10(0.01/self.total_frequency)
        #print(self.floor)

    def score(self, text):
        '''
        This function computes the score of the cracked text based on the quadgram frequency.
        Args:
            text (str): The potential cracked ciphertext
        '''
        score = 0
        quadgram = self.quadgram.__getitem__ 

        for i in range(len(text)-self.length+1):
            # add corresponding score if in quadgram else add the small negative factor
            if text[i:i+self.length] in self.quadgram: 
                score += quadgram(text[i:i+self.length])
            else: 
                score += self.floor          
        return score


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help="Name of the file containing the ciphertext to be decrypted")
    parser.add_argument('-n', type=str, help="Encrypted Name to be decrypted")
    args = parser.parse_args()
    name = args.n
    f = open(args.f, 'r')
    cipher = f.read()
    crack_caesar_quad(cipher.upper() + name.upper(), len(name), name.lower())