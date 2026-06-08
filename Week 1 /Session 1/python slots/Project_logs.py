class LogEntry:
    """
    LogEntry uses __slots__ to reduce memory usage.
    Only these attributes can exist:
    timestamp, level, message
    """

    __slots__ = ("timestamp", "level", "message")

    def __init__(self, timestamp, level, message):
        self.timestamp = timestamp
        self.level = level
        self.message = message

    def __str__(self):
        return f"[{self.timestamp}] [{self.level}] {self.message}"


def display_logs(logs):
    print("\n===== SYSTEM LOGS =====")

    for log in logs:
        print(log)

    print("=======================\n")


def count_errors(logs):
    error_count = 0

    for log in logs:
        if log.level == "ERROR":
            error_count += 1

    return error_count


def count_warnings(logs):
    warning_count = 0

    for log in logs:
        if log.level == "WARNING":
            warning_count += 1

    return warning_count


def main():
    logs = [
        LogEntry("12:00", "INFO", "Server started"),
        LogEntry("12:01", "INFO", "Database connected"),
        LogEntry("12:03", "WARNING", "Memory usage high"),
        LogEntry("12:05", "ERROR", "Database disconnected"),
        LogEntry("12:07", "INFO", "Reconnecting database"),
        LogEntry("12:08", "ERROR", "Authentication failed"),
    ]

    display_logs(logs)

    print("Total Logs:", len(logs))
    print("Warnings:", count_warnings(logs))
    print("Errors:", count_errors(logs))

    print("\nTesting __slots__...\n")

    try:
        logs[0].ip_address = "127.0.0.1"
    except AttributeError as e:
        print("AttributeError Caught:")
        print(e)


if __name__ == "__main__":
    main()