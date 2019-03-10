# Fake News Detection Application
This is a part of the final semester engineering project at PES University.

## Abstract
Given news content in the form of text, image or url, the project aims to verify the credibility of the information through the use of different metrics like:

1. Fake Image Detection
2. Fake Website Detection
3. Comparing with Credible Sources
4. Stance Detection
5. Community Detection

## Deliverables
The project aims to deliver a web application to interact with users. Along with this, the features of the project will also be exposed in the form of a REST API for developers to leverage the metrics and help fight against the spread of fake news

## Setup Instructions
```bash
cd code
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python -m spacy download en

```

## Dependencies
1. [Event Registry API](http://eventregistry.org/)
2. [PyTextRank](https://medium.com/@aneesha/beyond-bag-of-words-using-pytextrank-to-find-phrases-and-summarize-text-f736fa3773c5)

## Library Bug Fixes
To ensure PyTextrank works as expected, follow [this link](https://github.com/DerwenAI/pytextrank/issues/15) to make necessary changes in your installation or use the virtualenv in this repository

## Team Details
1. Akhilesh Nirna
2. Aviral Joshi
3. Hardik Mahipal Surana

## Acknowledgement
We would like to thank our guide, Dr. S Natarajan, for his support. We would also like to thank the teachers and administration of PES University.