import boto3
from botocore.exceptions import ClientError
from Elf import Elf

# The character encoding for the email.
CHARSET = "UTF-8"
AWS_REGION = "us-east-1"
JOULUPUKKI_EMAIL = "Joulupukki <joulu.pukki@lauri.io>"


def email_body_text(giver: Elf, gift_recipient: Elf) -> tuple[str, str]:
    return f"""{headline(giver)},
    
{receiver_message()} {gift_recipient.name}.

{receiver_wishes_text(gift_recipient)}

{ending()}

t: Joulupukki
"""


def email_body_html(giver: Elf, gift_recipient: Elf) -> tuple[str, str]:
    return f"""<html>
<head></head>
<body>
<p>{headline(giver)},</p>

<p>{receiver_message()} <b>{gift_recipient.name}</b>.</p>

{receiver_wishes_html(gift_recipient)}

<p>{ending()}</p>

<p>t: Joulupukki</p>
</body>
</html>
"""


def headline(giver: Elf) -> str:
    return f"Parahin {giver.name}"


def receiver_message() -> str:
    return "Tänä vuonna joululahjasi saaja on"


def ending() -> str:
    return "Nähdään aattona!"


def receiver_wishes_text(gift_recipient: Elf) -> str:
    if len(gift_recipient.wishes) > 1:
        return f"{gift_recipient.name} {multi_wish_text()}{''.join([f'\r\n- {w}' for w in gift_recipient.wishes])}"

    if len(gift_recipient.wishes) == 1:
        return f"{gift_recipient.name} {single_wish_text()} {gift_recipient.wishes[0]}"

    return f"{gift_recipient.name} {no_wish_text()}"


def receiver_wishes_html(gift_recipient: Elf) -> str:
    if len(gift_recipient.wishes) > 1:
        return f"<p>{gift_recipient.name} {multi_wish_text()}</p><ul>{''.join([f'<li>{w}</li>' for w in gift_recipient.wishes])}</ul>"

    if len(gift_recipient.wishes) == 1:
        return f"<p>{gift_recipient.name} {single_wish_text()} {gift_recipient.wishes[0]}</p>"

    return f"<p>{gift_recipient.name} {no_wish_text()}</p>"


def multi_wish_text() -> str:
    return "on ollut tänä vuonna erityisen kiltti ja on lähettänyt Joulupukille listan mahdollisia lahjatoiveita:"


def single_wish_text() -> str:
    return (
        "on ollut tänä vuonna varsin kiltti ja lähetti Joulupukille yhden lahjatoiveen:"
    )


def no_wish_text() -> str:
    return "ei kirjoittanut Joulupukille lahjatoiveita, mutta kertoi pitävänsä kaikista sopivista yllätyksistä!"


def send_real_email(giver: Elf, gift_recipient: Elf, real_run: bool) -> None:
    subject = "Postia joulupukilta!"
    body_text = email_body_text(giver, gift_recipient)
    body_html = email_body_html(giver, gift_recipient)
    if real_run:
        send_email(giver.email, subject, body_text, body_html)
    else:
        print(f"Would send email to '{giver.email}' with subject '{subject}'")
        print(body_text)
        print("=======")
        print(body_html)


def send_test_email(recipient: str) -> None:
    sender = JOULUPUKKI_EMAIL
    subject = "Amazon SES Test (Joulupukki)"

    # The email body for recipients with non-HTML email clients.
    body_text = (
        "Amazon SES Test (Python)\r\n"
        "This email was sent with Amazon SES using the "
        "AWS SDK for Python (Boto)."
    )

    # The HTML body of the email.
    body_html = """<html>
    <head></head>
    <body>
    <h1>Amazon SES Test (SDK for Python)</h1>
    <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """
    send_email(sender, recipient, subject, body_text, body_html)


def send_email(recipient: str, subject: str, body_text: str, body_html: str) -> None:
    client = boto3.client("ses", region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={"ToAddresses": [recipient]},
            Message={
                "Body": {
                    "Html": {"Charset": CHARSET, "Data": body_html},
                    "Text": {"Charset": CHARSET, "Data": body_text},
                },
                "Subject": {"Charset": CHARSET, "Data": subject},
            },
            Source=JOULUPUKKI_EMAIL,
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        print(f"Email sent to '{recipient}'! Message ID:"),
        print(response["MessageId"])
