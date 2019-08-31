# Paper analysis
Paper keywords extraction 

## What is it?
A simple tool to run a basic, very simple, 
topic analysis on facebook posts. Additionally, it uses
[spaCy](https://github.com/explosion/spaCy) default models 
to extract named-entities from comments. 
It's pretty much a word counter that employs 
standard NLP pre-processing, plus the NER part performed by spaCy. 

#### How does it do it?
It gets the data of given posts by calling
the [Facebook GraphAPI](https://developers.facebook.com/tools/explorer/). 
It performs text preprocessing
(tokenization, stopwords filtering, stemming) and makes plots:
a word cloud plot - using this awesome library 
[`word_Cloud`](https://github.com/amueller/word_cloud) -
and a bar plot - using [`seaborn`](https://github.com/mwaskom/seaborn) - 
of the N most important words.
The tool can be configured in page id, single post id, number of
posts, etc. 
It can be run on the last n plots, or on a given post id.

## How to install

This tool has been developed on Ubuntu 18.04 and macOS High Sierra, but 
has never been seriously tested. 
It requires Python3+ and [`virtualenv`](https://github.com/pypa/virtualenv). 
With these two installed, simply clone the repo
and run `source install.sh`

#### Requirements

A Facebook API token associated to an active app is an essential requirement.
(See [Facebook for developers documentation](https://developers.facebook.com/docs/facebook-login/access-tokens/))
The file `requirements.txt` contains all the needed python packages and spaCy models.

##### Ubuntu 18.04 
It should come with Python3+ installed, so just give 
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

The file `settings.conf` contains a number of parameters, 
among which, access token and facebook profile/page id, 
that have to be edited in order for the tool to run.

### Fancy word count
Two modes are allowed: 
(**remember to edit settings.conf**): 
##### Single-post using post ID
* `source wc_by_id.sh settings.conf` 
##### Latest N posts
* `source wc_latest.sh settings.conf`

### Named-Entity Recognition using spaCy
Additionally, it is possible to run Named-Entity Recognition using 
default spaCy models (supported: en, it). 
No Word Cloud will be produced in this case.

##### Single-post using post ID
* `source ner_by_id.sh settings.conf` 
##### Latest N posts
* `source ner_latest.sh settings.conf`


### Considerations 
The tool is designed to run until the conditionds on the variables 
in `settings.conf` are met or, shouldn't this happen, 
up until the max request rate, that Facebook do apply, is reached.

That's it!

## Results 
Here there are two images of the plots that are produced 
by running the tool on this post:
https://www.facebook.com/GiveToTheNext/posts/477277113022512

#### Bar plot using the top 20 words

![alt_text](https://raw.githubusercontent.com/fabriziomiano/fb-comments-simple-analysis/master/sample_img/barplot_445363319547225_477277113022512.png)

#### Word cloud with no stemming 

![alt text](https://raw.githubusercontent.com/fabriziomiano/fb-comments-simple-analysis/master/sample_img/wc_477277113022512.png)

#### Bar plot using the top 12 entities

![alt_text](https://raw.githubusercontent.com/fabriziomiano/fb-comments-simple-analysis/master/sample_img/barplot_477277113022512_ner.png)

## Acknowledgements
Thanks to the people at [spaCy](https://github.com/explosion/spaCy)
for the NE part,to the people who produced 
[facebook-sdk](https://github.com/mobolic/facebook-sdk)
for the ease of access to the data, and finally to the guys who made 
[word_cloud](https://amueller.github.io/word_cloud) for the awesome word-cloud images
that can be produced.