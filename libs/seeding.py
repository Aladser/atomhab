from django.db.models import Model

class Seeding:
    @staticmethod
    def seed_table(model: Model, data_list: list):
        """
            Заполняет таблицу базы данных
            :param model: модель
            :param data_list: массив строк таблицы
        """

        Seeding.__reset_autoincrement(model)
        method_obj_list = [model(**param) for param in data_list]
        model.objects.bulk_create(method_obj_list)

    @staticmethod
    def seed_users(model:Model, data_list: list, password:str=None):
        """
            Заполняет таблицу пользователей базы данных
            :param model: модель
            :param data_list: массив строк таблицы
            :param password: пароль пользователей
        """

        Seeding.__reset_autoincrement(model)
        for user_obj in data_list:
            user = model.objects.create(**user_obj)
            if password is not None:
                user.set_password(password)
            user.save()

    @staticmethod
    def __reset_autoincrement(model: Model):
        if hasattr(model, 'truncate'):
            model.truncate()
        else:
            model.objects.all().delete()
