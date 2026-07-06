import random
import typing


PLAYERS = ["alice", "bob", "charlie", "dylan"]
ACTIONS = ["run", "eat", "sleep", "grab", "move",
           "climb", "swim", "use", "release"]


def gen_event() -> typing.Generator:
    while True:
        name = random.choice(PLAYERS)
        action = random.choice(ACTIONS)
        yield (name, action)


def consume_event(events: list) -> typing.Generator:
    while len(events) > 0:
        index = random.randrange(len(events))
        event = events[index]
        events.pop(index)
        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")

    generator = gen_event()
    for i in range(1000):
        name, action = next(generator)
        print(f"Event {i}: Player {name} did action {action}")

    event_list = [next(generator) for i in range(10)]
    print(f"Built list of 10 events: {event_list}")

    for event in consume_event(event_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {event_list}")


if __name__ == "__main__":
    main()
