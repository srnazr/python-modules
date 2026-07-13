from abc import ABC, abstractmethod
from typing import Any, Protocol, Union


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

    def output_pipeline(self, nb: int, plugin: "ExportPlugin") -> None:
        for proc in self._processors:
            batch: list[tuple[int, str]] = []
            count = 0
            while count < nb:
                if proc.remaining() == 0:
                    break
                one_item = proc.output()
                batch.append(one_item)
                count = count + 1
            if len(batch) > 0:
                plugin.process_output(batch)


class ExportPlugin(Protocol):

    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:

    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = []
        for rank, value in data:
            values.append(value)
        print("CSV Output:")
        print(",".join(values))


class JSONExportPlugin:

    def process_output(self, data: list[tuple[int, str]]) -> None:
        pairs = []
        for rank, value in data:
            one_pair = "\"item_" + str(rank) + "\": \"" + value + "\""
            pairs.append(one_pair)
        print("JSON Output:")
        print("{" + ", ".join(pairs) + "}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===\n")

    print("Initialize Data Stream...\n")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors")
    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(numeric)
    stream.register_processor(text)
    stream.register_processor(log)

    first_batch: list[Any] = [
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
    print("\nSend first batch of data on stream:", first_batch)
    stream.process_stream(first_batch)
    print()
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    csv_plugin = CSVExportPlugin()
    stream.output_pipeline(3, csv_plugin)
    print()
    stream.print_processors_stats()

    second_batch: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print("\nSend another batch of data:", second_batch)
    stream.process_stream(second_batch)
    print()
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    json_plugin = JSONExportPlugin()
    stream.output_pipeline(5, json_plugin)
    print()
    stream.print_processors_stats()