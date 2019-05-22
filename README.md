# Lyrics Generation: NLP Project for ENSF 519 (Winter 2019)

By: Jenard Cabia, Shuyi Jin, Nathan Schuetz, Quan Sun

This repository contains our research papers as well as our attempt to train and optimize Artificial Intelligence to generate sequences of meaningful song lyrics for various song genres and moods (happy, neutral, and sad).

## Research

One vastly
popular approach of sequence generation we found in our
study which we will utilize in this experiment is an Artificial
Neural Network (ANN) which will be trained through
supervised learning using song lyrics labeled per genre and
mood. Since lyrics are sequential data and we want the
network to remember parts of the sequences from previous
iterations, we will also implement a deep learning model
Long short-term memory (LSTM) to satisfy our
requirements for sequence generation.

For more information about ANN and LSTM, you can read more about them in: https://en.wikipedia.org/wiki/Artificial_neural_network

### Phase I Deliverable

Our main approach was to divide the project into two
phases, Phase 1 & 2. Phase 1 will focus on collecting the
information and data required for lyrics generation through
scraping of multiple sites including allmusic.com and
lyrics.com. Each song collected will be cleaned, integrated
and labeled before it enters the preprocessing stage where a
text-normalizer is used to remove html tags, accented
characters, special characters, and stop words.
Stemming/Lemmatization will also be performed to the full
set of lyrics which will be our corpus, making a document to
be the lyrics of a single song. Songs will be labeled as either
positive or negative by performing Sentiment Analysis on
each document using VADER Lexicon. Once labeled, the
data will be stored in a Pandas DataFrame where it can be
classified and grouped by genre, by artist, and by album.
Lastly, the sentiment results, as well as common word
occurrences for each grouping will be visualized using
MatPlotLib.

### Phase II Deliverable

Phase 2 will focus mainly on designing the ANN and
LSTM models required for lyrics generation, reporting and
analyzing the newly generated song lyrics, and lastly
performing an evaluation of the results to see whether the
phrases used and the emotions of the generated lyrics reflect
that of the training set. The data gathered from Phase 1 will
be used as training data for the models as well as the
expected outcome for the algorithm.

## Lyrics samples Generated for experimental alternative model:

“(...) Well, I just a little bit of time I need you to feel
alright And the still love her mind I love I just the She with
all my You can do it if you don't know why It's hard to will
be a will you ever said oh So what love should if They won't
come the back with you goes Don't the one more What a to
get to love you feel this And I don't know the And I can't see
me I need you to feel When I know you're gonna say ”
