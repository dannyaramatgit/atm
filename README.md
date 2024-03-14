Simple ATM backend

1. please nevigate to the app's main folder and run command:
   **docker-compose up -d**
2. navigate to **http://localhost:8000/docs**

if not loading please run :
**docker-compose down**
and
**docker-compose up -d**
again


available actions:
1. withdrawal
   ex: get request - localhost:8000/atm/withdrawal/?amount=370
   
2. refill
   ex: post request - localhost:8000/atm/refill/
   with request body:
   {
    "money":{
        "0.1": 5,
        "5": 20,
        "20": 15,
        "100": 30
      }
    }
