class RePublicOsArchiveRouter:

    apps_to_archive = ['spotify', 'strava', 'twitter', 'google']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.apps_to_archive:
            return 'archive'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.apps_to_archive:
            return 'archive'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.apps_to_archive
            or obj2._meta.app_label in self.apps_to_archive
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
