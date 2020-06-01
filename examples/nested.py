from nommy import parser, le_u8, string


@parser
class Header:
    id: le_u8
    recipient: string(None)
    sender: string(None)


@parser
class Body:
    subject: string(None)
    text: string(None)


@parser
class Email:
    header: Header
    body: Body


def main():
    email, rest = Email.parse(
        b'\xffjoeblow@example.org\0sender@example.org\0subject\0message\0\xff'
    )
    print(f'full email: {email!r}')
    print(f'email header: {email.header!r}')
    print(f'email body: {email.body!r}')
    print(f'rest: {rest!r}')


if __name__ == '__main__':
    main()
