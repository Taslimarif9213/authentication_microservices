import datetime

import pytz
from django.utils.crypto import get_random_string

from error_logging.db_log_handler import log_error

# Error-code: 1xxxx

otp_validity = 120


class OTPService:

    def generate_otp(self):
        try:
            return get_random_string(6, '0123456789')

        except Exception as e:
            log_error(e, 10000)
            raise e

    def verify_otp(self, created_at):
        try:
            return True if (datetime.datetime.now().astimezone(
                tz=pytz.UTC) - created_at).seconds <= otp_validity else False

        except Exception as e:
            log_error(e, 10000)
            raise e
    