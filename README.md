# Stock Market Knowledge Assistant Frontend
Welcome to Raggy! Want to start investing, but don't know where to begin? Raggy is a stock market knowledge assistant who can help you become familar with foundational stock market terminology and provide investing strategies you can start implementing now!

This repository contains the frontend of Raggy. 
To see Raggy's backend, click [HERE](https://github.com/HaydenK2/stock-market-assistant-backend)
# Components
## 1. React Frontend
Raggy is built ontop of a React frontend for user friendly access. Simply type in what you want to ask Raggy. Within a couple seconds, Raggy will generate an answer to help you out!

## 2. Axios FastAPI
We utilze axios to so Raggy can communicate with its FastAPI. The backend will generate the answer using its RAG system and send the answer to the frontend

#   Getting Started Locally
1. After you clone the repository, create a virtual environment to run the frontend
   
```
python -m venv .venv
```
2. Activate the venv:
```
.\.venv\Scripts\Activate.ps1
```

3. pip install all the packages inside ```requirments.txt```
```
pip install -r requirements.txt
```

4. cd into frontend and then run the frontend code:

```
cd frontend
npm run dev
```
4. Click on the url link to view the frontend
- Make sure the backend is running as well before you ask Raggy!
