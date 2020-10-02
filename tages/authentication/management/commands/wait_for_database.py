from django.core.management.base import BaseCommand
from django.db import connections
from django.db import DEFAULT_DB_ALIAS
import time

DEFAULT_TIMEOUT = 20


class Command(BaseCommand):
    help = 'Wait until database is ready'
    requires_model_validation = False
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument(
            '-t', '--timeout', type=int, action='store', dest='timeout',
            default=DEFAULT_TIMEOUT, help='Timeout for database connection'
        )
        parser.add_argument(
            '--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS,
            help='Nominates a specific database to wait for. '
                 'Defaults to the "default" database.'
        )
        parser.add_argument(
            '--test-mode', action='store_true', dest='test_mode',
            default=False,
            help='Test mode: it does not actually check database.'
        )

    def wait_for_database(self, timeout=DEFAULT_TIMEOUT,
                          database=DEFAULT_DB_ALIAS, test_mode=False):
        ready = False
        connection = connections[database]
        for i in range(timeout):
            try:
                if not test_mode:
                    connection.connect()  # pragma: no cover
                ready = True
                break
            except Exception as e:  # pragma: no cover
                # Check error type
                error = str(e).splitlines()[0]
                if error.startswith('fe_sendauth: no password supplied'):
                    ready = True
                    break
                if error.startswith('FATAL:  no pg_hba.conf entry'):
                    ready = True
                    break
                msg = 'could not connect to server: Connection refused'
                if error.startswith(msg):
                    pass
                msg = 'FATAL:  the database system is starting up'
                if error.startswith(msg):
                    pass
                else:
                    self.stdout.write(error)
            time.sleep(1)  # pragma: no cover
        if not test_mode:
            connection.close()  # pragma: no cover
        return ready

    def handle(self, *args, **options):
        kwargs = dict(
            timeout=options['timeout'],
            database=options['database'],
            test_mode=options['test_mode'],
        )
        ready = self.wait_for_database(**kwargs)
        if ready:
            msg = 'Database "{0}" ready'.format(options['database'])
            self.stdout.write(self.style.SUCCESS(msg))
        else:  # pragma: no cover
            db = options['database']
            msg = 'Database "{0}". Timeout reached'.format(db)
            self.stderr.write(self.style.ERROR(msg))
            exit(1)
