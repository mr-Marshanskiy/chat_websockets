from abc import abstractmethod


class ActiveUsersService:
    @abstractmethod
    def get_active_users(self):
        raise NotImplementedError

    @abstractmethod
    def add_active_user(self, user):
        raise NotImplementedError

    @abstractmethod
    def rm_active_user(self, user):
        raise NotImplementedError


class ActiveUsersTempSetService(ActiveUsersService):
    def __init__(self, active_users, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ACTIVE_USERS = active_users

    def get_active_users(self):
        return self._ACTIVE_USERS

    def add_active_user(self, user_id):
        self._ACTIVE_USERS.add(user_id)
        return

    def rm_active_user(self, user_id):
        try:
            self._ACTIVE_USERS.remove(user_id)
        except KeyError:
            pass
        finally:
            return

    def select_only_active(self, user_ids):
        return set(user_ids).intersection(self.get_active_users())
