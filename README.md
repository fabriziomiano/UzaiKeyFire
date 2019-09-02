# Vocabulary analyzer
Are you always using the same words in
your scientific papers?
This is a tool to run a text analysis on 
PDF files containing an English corpus.

# What is it?
It's a simple tool to extract keywords and Part-Of-Speech distributions
from a given PDF. It employs a
[spaCy](https://github.com/explosion/spaCy) English model
to perform tokenization and named-entities extraction.
It's pretty much a word counter that employs 
standard NLP pre-processing, plus the NER part performed by spaCy. 
Additionally it produces a word cloud image. 

## How to install
This tool has been developed on Ubuntu 18.04 and macOS High Sierra, but 
has never been seriously tested. 
It requires Python3+ and [`virtualenv`](https://github.com/pypa/virtualenv). 
With these two installed, simply clone the repo and run `source install.sh`

#### Requirements
The file `requirements.txt` contains all the needed python packages.

##### Ubuntu 18.04 
Ubuntu should come with Python3+ installed, so just give 
`source install.sh` and Bob's your uncle.

##### macOS
Follow the following steps: 

* Open a Terminal and run `xcode-select --install`
* log out and back in
* get Homebrew [here](https://brew.sh/): 
copy/paste the link they provide in a terminal. 

At this stage, if you get an error that says

```
git: error: unable to locate xcodebuild, please make sure the path to the Xcode folder is set correctly!
git: error: You can set the path to the Xcode folder using /usr/bin/xcode-select -switch
```

follow what's been said 
[here](https://stackoverflow.com/questions/19647788/git-error-unable-to-locate-xcodebuild-after-a-fresh-os-x-mavericks-upgrade), 
and run the following in a terminal:

* `sudo xcode-select -switch /Library/Developer/CommandLineTools`

Once Homebrew has been downloaded and installed you can install Python3 by:

* `brew install python`

Once Python has been brewed
(a.k.a. Python installation finished successfully), 
you should be able to run `pip install virtualenv` 
and finally `source install.sh`.

##### Windows
Sorry, I have no clue. I don't even care.

## How to run
Once the virtual environment has been created, and activated, simply run 
```
python main.py --filepath /path/to/PDF_file
```
This will assume by default a maximum number of words to plot `nmaxwords = 20`.
To modify this setting, simply specify your preference by add the `--nwords` flag, e.g.
```
python main.py --filepath /path/to/PDF_file --nmaxwords 25
```

### Considerations 
The tool is designed to run only on searchable PDF, namely PDF files
in which the text can be selected and copied. 
That's it!

## Results 
Here there are the sample results obtained by running on a PDF 
of some proceedings I wrote a long time ago, taken from [here](https://pos.sissa.it/282/856/pdf). 

#### Top 20 keywords
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/kwords_count.png)

#### Top 20 nouns
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Nouns.png)

#### Top 20 adjectives
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Adjectives.png)

#### Top 20 adverbs
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Adverbs.png)

#### Top 20 verbs
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Verbs.png)

#### Top 20 entities
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Entities.png)

#### Top 20 entity types
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Entity%20types.png)

#### Word cloud
![alt text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/wordcloud.png)
## Acknowledgements
Thanks to the people at [spaCy](https://github.com/explosion/spaCy)
for the NE part, and to the guys who made 
[word cloud](https://amueller.github.io/word_cloud) for the awesome word-cloud images
that can be produced.
