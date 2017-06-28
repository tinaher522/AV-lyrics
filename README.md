# README #

AVSR-Music
Dissertation project for MSc in Advanced Computer Science of the University of Sheffied.
Author = Xinghui He
Supervisor = Dr. Jon Barker


### What is this repository for? ###

AIM of the project
Conduct a research that analyse the approaches HMM-GMM and HMM-DNN of ASR in music. 
The experiments were implemented using Kaldi tools. The database were constructed using 
acoustic covers of popular music obtained from YouTube. The Language Model were constructed 
using the lyrics of the dicographies of several artist. The Acoustic Model were based in a 
subset of cmudict.

### How do I get set up? ###

annotation = The annotation folder contain the annotation files generated in each stage of the annotation process.
asrmusic = Project's Kaldi recipie.
database = Database files of the waveforms of the project.
docs = Foldes with some documentation and its latex files.
lmodel = Files for language and acoustic model.
tools = Collection of tools separated by stages' subfolders.
wav = Folder with the audios database.
Readme.md = This file.


### Contribution guidelines ###

- annotation
Folder contains the files generated from the annotation process. For description of the content of each subfolder refer to /annotation/readme.md
- asrmusic
This folder have the kaldi recipie with the proper structure for the project. This folder should be copied into /{KALDI_ROOT}/egs/ in order to maintain the kaldi's organization.
- database
Database files are saved in this folder.
- docs
Folder contains some LaTex help info. In general, the information of each readme.md in the project are in the manuals too.
- lmodel
Folder contains the necessary files for the language model and acoustic model.
- tools
The tools necessaries for the construction of the database, the acoustic model and the language model were created using Python. Each tools' subfolder intent to group the required tools for an specific stage in the project.
- wav
All the wav files should be saved into this folder.
Watch  
Recent activity 

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact