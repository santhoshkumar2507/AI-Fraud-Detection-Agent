# Smart AI Agent to Protect Users from Fraudulent Transactions  
Team Name: sod 001  

## Problem Statement  
Online transactions are increasing rapidly, and so are fraud cases like unauthorized payments, high-value scams, unusual time transactions, and transactions from unknown locations.  
Users often lose money and trust because fraud is detected too late or without clear explanation.

## Proposed Solution  
We built a Smart AI Fraud Detection Agent that analyzes transaction data and classifies each transaction as:  
- NORMAL  
- SUSPICIOUS  
- FRAUD  

The agent uses rule-based intelligence and decision logic to protect users in real-time and suggest actions automatically.

## Agent Workflow  
1. User uploads transaction CSV file  
2. Data preprocessing (cleaning & validation)  
3. Fraud Detection Agent applies rules  
4. Decision Engine classifies transaction  
5. Action module suggests next step  
6. Result shown in Streamlit dashboard  

## Tech Stack  
- Python  
- Streamlit (Frontend Dashboard)  
- Pandas (Data handling)  
- GitHub (Version control)  
- Figma (Prototype / System flow design)

## Fraud Detection Rules  
- Amount greater than ₹80,000 → FRAUD  
- Transaction at unusual time (12 AM – 5 AM) → SUSPICIOUS  
- Transaction from unknown location → SUSPICIOUS  
- Combination of 2 or more → FRAUD  
- Normal behavior → NORMAL  

## Features  
- Detects fraud, suspicious and normal transactions  
- Real-time decision display  
- Explainable AI (shows reason for classification)  
- Action recommendation system  
- CSV based dataset input  
- Agentic behavior implementation  

## Setup & Run  
1. Install dependencies  
```bash
pip install streamlit pandas
