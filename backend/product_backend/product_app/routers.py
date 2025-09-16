class UserRouter:
    route_app_labels = {"product_app"}

    def db_for_read(self, model, **hints):
        if model._meta.db_table == "my_app_user":
            return "user_db"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.db_table == "my_app_user":
            return "user_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.db_table == "my_app_user" or obj2._meta.db_table == "my_app_user":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Never migrate user table in product DB
        if model_name == "user":
            return False
        return None
