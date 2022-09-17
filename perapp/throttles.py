from rest_framework.throttling import UserRateThrottle


class TOdoRateThrottle(UserRateThrottle):
    scope = 'Todo'