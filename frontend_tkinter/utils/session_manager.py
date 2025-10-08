class SessionManager:
    """Singleton SessionManager for handling user sessions"""
    
    _instance = None
    _user_id = None
    _username = None
    _role = None
    _token = None
    _logged_in = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance
    
    def store_user(self, user_id, username, role, token):
        SessionManager._user_id = user_id
        SessionManager._username = username
        SessionManager._role = role
        SessionManager._token = token
        SessionManager._logged_in = True
    
    def get_user(self):
        if self.is_logged_in():
            return {
                'user_id': SessionManager._user_id,
                'username': SessionManager._username,
                'role': SessionManager._role,
            }
        return None
    
    def get_token(self):
        return SessionManager._token
    
    def get_role(self):
        return SessionManager._role
    
    def is_logged_in(self):
        return SessionManager._user_id is not None and SessionManager._token is not None
    
    def clear_session(self):
        SessionManager._user_id = None
        SessionManager._username = None
        SessionManager._role = None
        SessionManager._token = None
        SessionManager._logged_in = False