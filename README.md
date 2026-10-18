# Statistics API with strict CORS

## Endpoint
GET /stats?values=1,2,3

Returns count, sum, minimum, maximum, mean, and the required account email. Values are computed on every request.

Allowed browser origin (exact match): https://dash-1dlfvd.example.com

Every HTTP response receives X-Request-ID and X-Process-Time, including preflight responses and errors.

## Deploy on Render
1. Create a new Web Service or Blueprint from this repository.
2. Build command: pip install -r requirements.txt
3. Start command: uvicorn app:app --host 0.0.0.0 --port $PORT
4. Test /stats?values=1,2,3 on the assigned HTTPS URL.
5. Submit only the base URL, not /stats.

## Local run
pip install -r requirements.txt
uvicorn app:app --reload
