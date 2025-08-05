 URL Shortener Microservice (AffordMed Round 1 Backend Assignment)

 Overview

This project is a URL Shortener microservice built with Django. It allows users to:
- Shorten a long URL (`POST /shorturls`)
- Redirect from the shortened URL (`GET /<shortcode>`)
- Retrieve statistics for a shortened URL (`GET /shorturls/<shortcode>`)

---

 API Endpoints
1 Create Short URL
- **Method:** `POST`
- **Endpoint:** `/shorturls`
- **Body:**
```json
{
  "url": "https://example.com/some/very/long/url",
  "validity": 30,
  "shortcode": "abcd1"
}
Response:
{
  "shortLink": "http://127.0.0.1:8000/abcd1",
  "expiry": "2025-01-01T00:30:00Z"
}

2. Redirect Short URL
Method: GET

Endpoint: /<shortcode>

Functionality: Redirects to the original long URL if not expired.

3. Get URL Statistics
Method: GET

Endpoint: /shorturls/<shortcode>

Response:
{
  "shortcode": "abcd1",
  "original_url": "https://example.com",
  "created_at": "2025-08-05T12:00:00Z",
  "expiry": "2025-08-05T12:30:00Z",
  "total_clicks": 5,
  "clicks": [
    {
      "timestamp": "2025-08-05T12:10:00Z",
      "referrer": "https://google.com",
      "location": "India"
    }
  ]
}

Setup Instructions
Navigate to the project root:
cd Q1-URl_Shortner_Service
Create a virtual environment and activate it:
Install dependencies:
pip install -r requirements.txt
Apply migrations:
python manage.py makemigrations
python manage.py migrate
Run the server:
python manage.py runserver


RESULTS:
Q1 Result.png
Q2 Result.png
Q3 Result.png