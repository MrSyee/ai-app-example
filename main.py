import argparse

from crew import ResearchCrew


def parse_args():
    parser = argparse.ArgumentParser(description="Run the crew with specific topic")
    parser.add_argument("--topic", type=str, default="AI LLMs", help="The topic to research")
    return parser.parse_args()


def main():
    args = parse_args()
    inputs = {
        "topic": args.topic,
    }

    ResearchCrew().kickoff(inputs)


if __name__ == "__main__":
    main()
