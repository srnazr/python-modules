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


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            handled = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    handled = True
                    break
            if handled is False:
                print(
                    "DataStream error - Can't process element "
                    "in stream: " + str(element)
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if len(self._processors) == 0:
            print("No processor found, no data")
        else:
            for proc in self._processors:
                total = proc.total_processed()
                left = proc.remaining()
                print(
                    proc.name + ": total " + str(total)
                    + " items processed, remaining " + str(left)
                    + " on processor"
                )


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===\n")

    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor")
    numeric = NumericProcessor()
    stream.register_processor(numeric)

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print("\nSend first batch of data on stream:", batch)
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)

    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nConsume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for i in range(3):
        numeric.output()
    for i in range(2):
        text.output()
    log.output()
    stream.print_processors_stats()