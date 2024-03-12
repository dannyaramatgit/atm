Simple ATM backend

1. please install dependencies by running this from main folder:
   pip install -r requirements.txt

3. choose db engine
   if sqlite, no changes needed
   if postgress, change connection string to postgres data in database.py switch SQLALCHEMY_DATABASE_URL parameter

4. run the app by running from main folder:
   uvicorn main:app --reload

available actions:
1. withdrawal
   ex: get request - localhost:8000/atm/withdrawal/?amount=370
3. refill
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
