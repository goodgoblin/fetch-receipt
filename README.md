# Hi Fetch!  
to run it first build and tag it
`docker build . -t hi-fetch-from-alex`

then start it up
`docker run -p 8000:8000 hi-fetch-from-alex`


# Running it locally
this will activate a virtual environment
`source .venv/bin/activate`

This will install the libs
`pip install --no-cache-dir -r requirements.txt`

This will run it
`uvicorn app.main:app --host 0.0.0.0 --port 8000`

This will run it in development mode
`fastapi dev app/main.py`

# Run the tests
Install the test libs
`pip install pytest httpx`

Run pytest
`pytest tests/test_receipts.py`

# Solution guidance
I tried to keep the solution simple.  
models.py contains the Receipt and Item models and these models take care of validation.
rules.py contains the functions for the points counting.  

main.py has the api controller logic and the app itself.  
