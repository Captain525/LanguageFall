# LanguageFall

FILE SUMMARIES: 

textData.py - gets data from list of websites. Puts it into an array then returns the list of file names. copies the html
files into files in the respective language folders. Also does some cutting and editing of thse files. 
Then, converts it into a csv which other functions can read to do the machine learning. 

makeCSV.py - makes the csv from the different folders of data. This gets the data ready for ML. 
manipulateText - cuts things out of text files to make it fit for use. Does this automatically. Called from textData.

manipulateText - edits the text obtained from websites to make it ready for machine learning.  

machineLearningLanguages - does the main machine learning. Uses a deep sequential neural network and splits the data from 
the csv into training, validation and test data, trains the training data on the model, then tests it to see how it works. 

Explanation of how it works: 

1. Once you have the csv, you have a bunch of pairs of text, and their proper classification. First thing you need to do is 
called feature extraction, which means you need to convert the input data into something useful for the computer to understand, 
which will help it be able to properly distinguish the languages. If you give it something like how much punctuation 
is in the line, that may not be as helpful as if we gave it the words in the line or something. 

2. The way I decided to do feature classification is by getting a list of the 200 most common trigrams for each language. 
This means the most common 3 letter(including spaces) combinations in the whole text. Using this, we can decompose each
input line into trigrams, to put it into a "numerical" form.

Another way this could've been done is with teh "bag of words" method, which means the 200 most common WORDS are chosen 
and the text is decomposed this way. however, i didn't choose this way because there could be cases where none of the words
matched exactly yet were very similar. 

for example, the words(not old english french or latin) interest and interesting. 
In the bag of words model, interest and interesting would be two different words, the computer unable to see the lexical 
similarity between the two, because it just knows if they're EXACTLY the same word, or NOT the same word. 

However, doing this in the trigram way, we could decompose them into the trigrams (made up here) int, ter, res, est, and ing. 
This means the computer would see them as:

              int  ter  res est  ing ...
interest        1   1     1   1    0
interesting     1   1     1   1    1 
This communicates the similarities and relation between the two words MUCH more clearly, and i think 
simplifies the language classification process. 

Note that the number for each doesn't have a limit, and a combo could occur many times:

The cat and the dog are the best in the world, but the dog does it better. 
the at_ and _do are est in_ but is_ bet ter
5   1    1    3  1   1  1    1   0   1  1
So, in our case we will have around 400(lets call it t) something unique trigrams(because there is overlap between the three languages)
which means each input is a t-dimensional vector(has t elements), where each element is the amount of times the corresponding
trigram occurs in that given sample of text. 
3. split the data into 3 parts: train, validation, test. 

This is done when we make feature matrices, basically we put
So, once we have this, we then need to normalize this input data. This is because we want to have a bound on what the max number
can be, so we can safely account for ALL possibilities in our neural network. To do this, you take the MAX value in 
the entire training set, so if there's 20 of one trigram in one text input, that would be the max, so we take that as the max, 
and we also get the min(which is almost always 0), and then we scale all elements in the vectors to be in the range 
0 to 1. If you divide everything by the max value, you KNOW that everything will be between 0 and 1. This helps keep the 
numbers at a reasonable size. 

So, now we have 3 parts of data, train validation and test, where each has a vector of trigrams as the input to the neural 
network and the output is again that classification. It's almost time to start the neural network. 

Last thing we must do before we make the neural network is we have to put the output categories into a form the 
computer can understand. To do this, we can use One Hot Encoding. What this is is that it turns categorical variables
into a vector. So, since we have three categories, we make the outputs as a 3d vector - each element corresponds to one category. 
So, to represent old english, we use [1 0 0], for old french we use [0 1 0] and for old latin we use [0 0 1]. If a language
could be multiple categories you could have multiple ones, but that doesn't apply  in our case. 

So, now it's time to talk about neural networks. A neural network is essentially a function, which takes in an input 
and gives an output. In our cas, the input is this t dimensional trigram vector corresponding to one text sample, and 
the output is either [1 0 0], [0 1 0] or [0 0 1], or more specifically, the relative probabilities of each classification, 
and the official classification is the greatest probability. 

The way a neural network works is essentially similar to pavlovlian conditioning: when the neural network guesses correctly, 
you want to reward that behavior, whereas when it guesses incorrectly, we want to discourage that behavior and change it. 

To get the prediction of the neural network is actually just adding and multiplying, which seems counterintuitive but it
works well. The way to visualize a network is as a series of nodes, and lines called weights which connect the nodes to eachother. 
You think of the nodes in layers, and as the neural network runs it sort of goes from one layer to the next calculating until 
it gets an answer. The weights each have a number in some range -r,r , often this range will be from -1 to 1, but it depends on 
the specific algorithm. To get the value of the next layer nodes, you multiply each of the previous layer's node value 
by the weight between that node and the new one, and do this for all the previous nodes and their weights, then add a constant
"bias" to this result ,and you get the value for the next layer. Then, to keep the data in a reasonable range so guesses don't vary
wildly, you normalize this value to be betweeen 0 and 1 or some other small range. You do this for each node at each layer, 
over and over again, and at the end you end with 3 values between 0 and 1, which represent the relative probabilities of each
classification. Then, the algorithm picks the highest value, and then that is the guess. 

The algorithm compares this guess vector to what the actual vector was [1 0 0] or [0 1 0] or [0 0 1]. Then, it gets the
error between the prediction and the result. Then, through each iteration, it adjusts the weights and biases of the network
accordingly to minimize the error of the network, which resultingly increases the accuracy. 

The network runs this same algorithm many many times on the training data, until it gets very good at classifying the 
data. 

Then, once we have this model with set weights and biases, we can test it by using our test set. We run the test set 
inputs through the model, not changing the weights and biases but just getting hte result, then we see how accurate the 
predictions were, which comes out in the accuracy of the model, as a percent correct. 

For this model, our accuracy was somewhere between 97 and 98% which i thought was very good ,considering i wasn't even 
sure this would work before trying it. 


used this article to help guide the ML part of my project:
https://towardsdatascience.com/deep-neural-network-language-identification-ae1c158f6a7d


