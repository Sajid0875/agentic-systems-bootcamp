class RateLimiter:
    def __init__(self, daily_limit):
        self._daily_limit = daily_limit
        self._requests_made = 0

    # Read-only property
    @property
    def requests_made(self):
        return self._requests_made

    # Getter
    @property
    def daily_limit(self):
        return self._daily_limit

    # Setter with validation
    @daily_limit.setter
    def daily_limit(self, value):
        if value <= 0:
            raise ValueError(
                "Daily limit must be greater than 0"
            )

        self._daily_limit = value

    # Computed property
    @property
    def remaining_requests(self):
        return (
            self._daily_limit
            - self._requests_made
        )

    def make_request(self):
        if self.remaining_requests <= 0:
            print("Rate limit exceeded!")
            return

        self._requests_made += 1
        print(
            f"Request successful. "
            f"Remaining: {self.remaining_requests}"
        )


# -------------------------
# Usage
# -------------------------

limiter = RateLimiter(5)

print("Daily Limit:", limiter.daily_limit)
print("Requests Made:", limiter.requests_made)
print("Remaining:", limiter.remaining_requests)

print()

limiter.make_request()
limiter.make_request()
limiter.make_request()

print()

print("Requests Made:", limiter.requests_made)
print("Remaining:", limiter.remaining_requests)

print()

limiter.daily_limit = 10

print("New Daily Limit:", limiter.daily_limit)
print("Remaining:", limiter.remaining_requests)