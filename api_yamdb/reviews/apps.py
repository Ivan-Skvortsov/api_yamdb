from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    name = 'reviews'

    def ready(self):
        import reviews.signals  # noqa: F401
        reviews.signals  # to pass pep8 tests in ya.praktikum
