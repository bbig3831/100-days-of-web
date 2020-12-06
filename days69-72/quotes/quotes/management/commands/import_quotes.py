import csv
import sys

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import requests

from quotes.models import Quote

GITHUB_URL = 'https://raw.githubusercontent.com/bbelderbos'
DATA_FILE = f'{GITHUB_URL}/inspirational-quotes/master/Quotes.csv'
DEFAULT_USER = 'ben'
MAX_QUOTES = 20

class Command(BaseCommand):
    help = 'Script to insert a set of quotes in our demo app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            dest='username',
            default=DEFAULT_USER,
            help='Username to associate the quotes with'
        )
        parser.add_argument(
            '--limit',
            dest='limit',
            default=MAX_QUOTES,
            help=f'Number of quotes to create (default={MAX_QUOTES})'
        )

    def handle(self, *args, **options):

        if Quote.objects.count() > 0:
            sys.exit('Not an empty DB, cowardly exiting')

        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            error = (f'User {username} does not exist in DB, creat it '
                     'via manage.py or register on the quotes site')
            sys.exit(error)

        try:
            max_quotes = int(options['limit'])
        except ValueError:
            sys.exit('Please specify a numeric value for limit')

        resp = requests.get(DATA_FILE)
        lines = resp.text.strip().splitlines()
        headers = 'quote author genre'.split()
        reader = csv.DictReader(lines, fieldnames=headers, delimiter=';')

        quotes = []
        for row in list(reader)[1:max_quotes+1]:
            quote = Quote(
                quote=row['quote'],
                author=row['author'],
                user=user
            )
            quotes.append(quote)

        Quote.objects.bulk_create(quotes)

        print(f'Done: {max_quotes} quotes created')