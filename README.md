# README #

# Lip reading for song transcription

Dissertation project for MSc in Advanced Computer Science of the University of Sheffied.

** Author = Xinghui He **
** Supervisor = Dr. Jon Barker **


## Introduction to the project.

This project is extended by an MSc project that ran last year called ‘Automatic Speech Recognition in Music’.  
Aiming to compare the performance of Audio-only ASR system with visual-only ASR system, this project would focus on the visual front end design to build an visual-only ASR system with the same music database last year.

The experiments are implemented using Kaldi tools with opencv and dlib. The database were constructed using videos of popular music obtained from YouTube. The Language Model were constructed using the lyrics of the dicographies of several artists. The Acoustic Model were based in a subset of cmudict.

## Content of folders
### annotation
containning annotated lyrics in our database.

### avsr-music
containning kaldi's recipe for our systems.

### database
containing the details for songs in database.

### docs
containing the dissertation and poster.

### Lmodel
containing the files for language model.

### tools
containing the tools for generating the prepared data.
like tools for segment wav files and mp4 files into utterances...