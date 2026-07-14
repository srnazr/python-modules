from abc import ABC, abstractmethod
from typing import Any, Union


class DataProcessor(ABC):
    name = "Data Processor"

    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._counter: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if len(self._storage) == 0:
            raise IndexError("No data left in this processor")
        oldest_item = self._storage[0]
        self._storage.remove(oldest_item)
        return oldest_item

    def total_processed(self) -> int:
        return self._counter

    def remaining(self) -> int:
        return len(self._storage)

    def _store(self, value: str) -> None:
        new_item = (self._counter, value)
        self._storage.append(new_item)
        self._counter = self._counter + 1


class NumericProcessor(DataProcessor):
    name = "Numeric Processor"

    def _is_number(self, item: Any) -> bool:
        if isinstance(item, bool):
            return False
        if isinstance(item, int):
            return True
        if isinstance(item, float):
            return True
        return False

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            if len(data) == 0:
                return False
            everything_ok = True
            for item in data:
                if self._is_number(item) is False:
                    everything_ok = False
            return everything_ok
        else:
            if self._is_number(data):
                return True
            else:
                return False

    def ingest(
        self, data: Union[int, float, list[Union[int, float]]]
    ) -> None:
        is_data_ok = self.validate(data)
        if is_data_ok is False:
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                text_value = str(item)
                self._store(text_value)
        else:
            text_value = str(data)
            self._store(text_value)


class TextProcessor(DataProcessor):
    name = "Text Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        elif isinstance(data, list):
            if len(data) == 0:
                return False
            everything_ok = True
            for item in data:
                if isinstance(item, str) is False:
                    everything_ok = False
            return everything_ok
        else:
            return False

    def ingest(self, data: Union[str, list[str]]) -> None:
        if self.validate(data) is False:
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._store(item)
        else:
            self._store(data)


class LogProcessor(DataProcessor):
    name = "Log Processor"

    def _is_valid_entry(self, entry: Any) -> bool:
        if isinstance(entry, dict) is False:
            return False
        if "log_level" not in entry:
            return False
        if "log_message" not in entry:
            return False
        if isinstance(entry["log_level"], str) is False:
            return False
        if isinstance(entry["log_message"], str) is False:
            return False
        return True

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            if len(data) == 0:
                return False
            everything_ok = True
            for item in data:
                if self._is_valid_entry(item) is False:
                    everything_ok = False
            return everything_ok
        else:
            if self._is_valid_entry(data):
                return True
            else:
                return False

    def ingest(
        self, data: Union[dict[str, str], list[dict[str, str]]]
    ) -> None:
        if self.validate(data) is False:
            raise ValueError("Improper log data")
        if isinstance(data, list):
            entries = data
        else:
            entries = [data]
        for entry in entries:
            level = entry["log_level"]
            message = entry["log_message"]
            combined_text = level + ": " + message
            self._store(combined_text)


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    print("Trying to validate input '42':", numeric.validate(42))
    print("Trying to validate input 'Hello':", numeric.validate("Hello"))
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")
    except ValueError as error:
        print("Got exception:", error)
    numbers: list[Union[int, float]] = [1, 2, 3, 4, 5]
    print("Processing data:", numbers)
    numeric.ingest(numbers)
    print("Extracting 3 values...")
    for i in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    text = TextProcessor()
    print("Trying to validate input '42':", text.validate(42))
    words = ["Hello", "Nexus", "World"]
    print("Processing data:", words)
    text.ingest(words)
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log = LogProcessor()
    print("Trying to validate input 'Hello':", log.validate("Hello"))
    logs = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print("Processing data:", logs)
    log.ingest(logs)
    print("Extracting 2 values...")
    for i in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")
