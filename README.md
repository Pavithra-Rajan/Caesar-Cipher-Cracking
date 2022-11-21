# Caesar-Cipher-Cracking

## Greedy Method

### To view the help menu
```console
python3 cipher.py -h
```
```console
usage: hill_climb.py [-h] -f F

optional arguments:
  -h, --help  show this help message and exit
  -f F        Name of the file containing the
              ciphertext to be decrypted
```
### Run the file
```console
python3 cipher.py -f messages/message.txt -c 4 -n pavithra
```

### The above script captures these heuristics
- Utilise the frequency distribution of each alphabet in the English language and calculate the score obtained for each alphabet in the ciphertext and each iteration of all possibilities. The iteration with the maximum score is chosen.
- Use the bigram frequency distribution of the English language. A bigram is a pair of letters. ‘Th’ is the most common bigram. Similar to the alphabet frequency heuristic, we can compute the score and choose the iteration with the maximum score.
- As there are only limited alphabets in the English language (26 + 1 for spaces in sentences), we can try out all the possibilities and choose the one that resembles a valid text.

### State-space graphs
- Letter frequency
![frequency](/states/frequency-analysis.png "Letter Frequency")

- Bigram frequency
![bigram](/states/bigram-analysis.png "Bigram Frequency")

- Mono-alphabetic substituition
![mono](/states/mono-sub.png "Mono-alphabetic substituition")

## Hill Climbing Method

### To view the help menu
```console
python3 hill_climb.py -h
```
```console
usage: hill_climb.py [-h] -f F

optional arguments:
  -h, --help  show this help message and exit
  -f F        Name of the file containing the
              ciphertext to be decrypted
```
### Run the file
```console
python3 hill-climb.py -f ciphers/cipher.txt 
```

### Graph
![hill climbing](/states/hillclimbing.png "Hill Climbing") <p></p>
Here the scores for each iteration will be computed till a local maximum is reached and shown to the user. If the text resembles a valid English text, then we can stop.
We can see below that the scores progressively increase (becomes less negative). The graph depicting the scores across each iteration is also generated.
