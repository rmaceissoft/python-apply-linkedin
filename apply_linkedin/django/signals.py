from django.dispatch import Signal


new_apply_with_linkedin = Signal(providing_args=["application", "request"])