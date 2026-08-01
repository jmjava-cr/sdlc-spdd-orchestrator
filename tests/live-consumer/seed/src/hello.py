"""Minimal app surface for live-consumer matrix seeding."""


def greet(name: str = "world") -> str:
    return f"hello, {name}"


if __name__ == "__main__":
    print(greet())
