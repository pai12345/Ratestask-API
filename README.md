# Xeneta - Rates task

Application having details, functionality and information for Xeneta rates task.

- Task 1: Includes HTTP based API.
- Task 2: Includes solution for Batch Processing.

# Task 1 - API

## Getting Started

### Prerequisites

- Python version above 3.0
- Python pip

### Assumptions

- Both orign and destination codes are case sensitive as both origin, destination params accept either port codes or region slugs.
- Price cannot be null but can be 0.
- Date format is YYYY-MM-DD.

### GET Request Task

#### Part 1

API returns a list with the average prices for each day on a route between port codes origin and destination.

API takes following URL parameters:

- date_from
- date_to
- origin
- destination

Sample: `http://localhost:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=NOSVG`

#### Part 2

API return an empty value (JSON null) for days on which there are less than 3 prices in total.

API takes following URL parameters:

- date_from
- date_to
- origin
- destination

Sample: `http://localhost:5000/rates_null?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=NOSVG`

### POST Request Task

#### Part 1

API endpoint for uploading price.

API takes following payload attributes:

- date_from
- date_to
- origin
- destination
- price

Sample: `{ "date_from":"2016-11-01", "date_to":"2016-12-10", "origin":"CNSGH", "destination":"NOKRS", "price":100 }`

#### Part 2

API endpoint extended to accept prices in different currencies. Exchange rates computed as per https://openexchangerates.org/

API takes following payload attributes:

- date_from
- date_to
- origin
- destination
- price
- currency

Sample: `{ "date_from":"2016-11-01", "date_to":"2016-12-10", "origin":"CNSGH", "destination":"NOKRS", "price":100, "currency": "EUR" }`

### Installation

To install application:

1. Clone the repository.

   `git clone https://github.com/pai12345/Ratestask-API.git`

2. Install pipenv for creating virtual environments.

   `pip install pipenv`

### Execution

For executing the application.

`pipenv run python index.py`

# Task 2 - Batch Processing

Navigate to Task2 folder for the Design and Approach doc on receiving and updating batches of tens of thousands of new prices.
