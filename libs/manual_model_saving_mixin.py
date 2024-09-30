class ManualModelSavingMixin:
    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        super().save(*args, force_insert, force_update, using, update_fields)
