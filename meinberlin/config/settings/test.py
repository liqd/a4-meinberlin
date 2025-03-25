from .dev import *

A4_ORGANISATION_FACTORY = "meinberlin.test.factories.organisations.OrganisationFactory"
A4_USER_FACTORY = "meinberlin.test.factories.UserFactory"
A4_MAP_ATTRIBUTION = (
    '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors'
)

ACCOUNT_EMAIL_VERIFICATION = "optional"

CAPTCHA_TEST_ACCEPTED_ANSWER = "testpass"
CAPTCHA_URL = "https://captcheck.netsyms.com/api.php"

TEST = True

try:
    from .polygons import *
except ImportError:
    pass
