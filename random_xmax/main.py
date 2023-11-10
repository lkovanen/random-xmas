import argparse
import json
import sys
import time

from Elf import Elf
from emails import send_real_email, send_test_email
from randomizer import create_random_mapping

MAILS_PER_SECOND = 14


def send_emails(elves: list[Elf], real_run: bool = False) -> None:
    recipient_index = create_random_mapping(len(elves))
    for giver, i_recipient in zip(elves, recipient_index):
        send_real_email(giver, elves[i_recipient], real_run)
        if real_run:
            # Wait a bit to avoid spamming the mail server.
            time.sleep(1.1 / MAILS_PER_SECOND)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Buy less, have a merrier christmas!"""
    )
    parser.add_argument(
        "--data",
        "-d",
        type=str,
        help="File with details on all the nice kids.",
    )
    parser.add_argument(
        "--test-email",
        type=str,
        help="If True, test sending email to given address.",
    )
    parser.add_argument(
        "--merry-christmas",
        action="store_true",
        default=False,
        help="If True, send real emails.",
    )

    args = parser.parse_args()

    if args.test_email:
        send_test_email(args.test_email)
        sys.exit(0)

    if not args.data:
        parser.print_help()
        sys.exit(1)

    with open(args.data) as f:
        data = json.load(f)

    elves = [Elf.model_validate(d) for d in data]
    print(f"Found details for {len(elves)} elves")

    send_emails(elves, real_run=args.merry_christmas)
