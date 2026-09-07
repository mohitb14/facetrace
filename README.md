# FaceTrace

## Face Identification & Blockchain Verification

FaceTrace is a prototype that combines face detection, live visual search,
face matching, cryptographic hashing and blockchain-based evidence verification.

## Pipeline

Input Face Image
↓
Face Detection & Embedding
↓
Live Yandex Visual Search
↓
Candidate Images
↓
Face Similarity Matching
↓
Best Match + Source URL
↓
SHA-256 Fingerprint
↓
Ethereum Smart Contract
↓
On-chain Verification
↓
Tamper Detection

## Features

- Face detection and face embeddings using InsightFace
- Live visual search using Yandex Images
- Automatic candidate image discovery
- Face similarity matching using cosine similarity
- SHA-256 evidence fingerprinting
- Ethereum smart contract evidence registry
- On-chain hash verification
- Tamper detection

## Tech Stack

- Python
- OpenCV
- InsightFace
- Playwright
- BeautifulSoup
- Web3.py
- Solidity
- Ethereum Tester

## How to Run

Clone the repository and create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate