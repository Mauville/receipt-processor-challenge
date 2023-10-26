# Receipt Processor Submission

Hi! My name is Oscar Vargas.

You can run the commands below and read on while everything gets ready.

I think you use Mac at Fetch, so I'll write the commands in bash.

```bash
git clone https://www.github.com/Mauville/receipt-processor-challenge
cd receipt-processor-challenge
docker build -t receipt-processor .
docker run -p 5000:5000 receipt-processor
```

## How did we do it?

A simple Python Flask application.

I used a hashmap for storing the receipts (`O(1)`, baby), hashed by their UUIDs.

I built the code adhering to SOLID principles and a layered architecture. Some notable sections are:

### Repositories

Receipts are stored in-memory, managed via a Singleton pattern—typical for database connectors.

I opted for UUIDs over hashes because they inherently reduce collision risks and are specifically designed for unique
identification.
UUID4 is random unlike a hash, so finding duplicates in the system is a bit harder.

### Test and Unit

Contains integration and unit testing respectively for the endpoints.

Ideally, we'd use Fixtures instead of hardcoding the test cases every time we want to use them. These avoid test cases
breaking when new functionality is added.

I wanted to keep the codebase small and tidy, so I used the inbuilt testing solutions that Python provides.

# How could we make this better?

**1. Persisting data.**

Since a receipt is quite unstructured, we could use a NoSQL database such as MongoDB*.
MySQL could also be used, if the schema of a receipt is consistent.

*I've actually worked at MongoDB before, so I think it's mature enough to support a big app like Fetch.

**2. Avoiding recalculation of points.**

We could store the point count on the ticket and implement update logic, or cache
it (Redis) if high availability is needed.

**3. Implementing a duplicate detector mechanism.**

Right now, duplicate tickets will be stored with different UUIDs. A duplicate should not be able to exist on the system.

**4. Implement proper validation of receipts and other cybersecurity measures.**

Ensure proper validation of receipts, lock down the API, and manage PII effectively.

**5. Gather metrics about the usage of the system.**

Our user is always who'll tell us what's needed from us. Some relevant
metrics could be peak usage times, most purchased products, etc.

# Sounds great, what now?

You now have my solution running on `localhost:5000`.

Send a POST request to `receipts/process` to store it and get its UUID:

```bash
curl --header "Content-Type: application/json" \
--request POST \
--data '{"retailer": "Target", "purchaseDate": "2022-01-02", "purchaseTime": "13:13", "total": "1.25", "items": [{ "shortDescription": "Pepsi - 12-oz", "price": "1.25" }]}' \
http://localhost:5000/receipts/process
```

Send a GET request to `receipts/<UUID>/points` to get its points.

```bash
curl --request GET http://localhost:5000/receipts/<YOUR_UUID_HERE>/points
```

I hope you enjoy reading my code (start in `main`), as much as I did coding this!