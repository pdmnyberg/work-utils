import hashlib
import secrets
import sys
import datetime
import os


def sha1(value):
    return hashlib.sha1(value.encode()).hexdigest()


def get_user_query(username, password, firstname="", lastname=""):
    salt = secrets.token_hex(16)
    hashed_password = sha1(salt+sha1(password))
    timestamp = datetime.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
    return (
f"""
insert into users (
    login,
    hashed_password,
    firstname,
    lastname,
    admin,
    status,
    last_login_on,
    language,
    created_on,
    updated_on,
    type,
    salt,
    must_change_passwd,
    passwd_changed_on
) values (
    '{username}',
    '{hashed_password}',
    '{firstname}',
    '{lastname}',
    't',
    '1',
    '{timestamp}',
    'en-GB',
    '{timestamp}',
    '{timestamp}',
    'User',
    '{salt}',
    'f',
    '{timestamp}'
);
"""
    )


def main(argv):
    script_name = os.path.basename(__file__)
    try:
        print(get_user_query(*argv[1:]))
    except TypeError:
        print(f"Usage: python {script_name} <username> <password> [firstname] [lastname]")


if __name__ == "__main__":
    main(sys.argv)
