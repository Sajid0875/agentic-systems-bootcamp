import argparse


def main():

    parser = argparse.ArgumentParser(
        description="Simple CLI Tool"
    )

    parser.add_argument(
        "name",
        help="User name"
    )

    parser.add_argument(
        "--age",
        type=int,
        default=18,
        help="User age"
    )

    args = parser.parse_args()

    print(f"Name: {args.name}")
    print(f"Age: {args.age}")


if __name__ == "__main__":
    raise SystemExit(main())