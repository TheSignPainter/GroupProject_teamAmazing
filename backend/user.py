from backend.hive_remote import getUser, getUserByID, addUser

class User():
    def __init__(self):
        self.id=None
        self.username=None
        self.email=None

    def todict(self):
        return self.__dict__

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id
 # def __repr__(self):
 #  return '<User %r>' % self.username

class User_Dal:
    persist = None

    # 通过用户名及密码查询用户对象
    @classmethod
    def login_auth(cls, username, password):
        #print('login_auth')
        result = {'isAuth': False}
        model = User()  # 实例化一个对象，将查询结果逐一添加给对象的属性
        rows = getUser(username, password)
        #print('查询结果>>>', rows)
        if rows:
            assert len(rows)==1
            rows = rows[0]
            result['isAuth'] = True
            model.id = rows[0]
            model.username = rows[1]
            model.email = rows[2]
        return result, model

    # flask_login回调函数执行的，需要通过用户唯一的id找到用户对象
    @classmethod
    def load_user_byid(cls, id):
        #print('load_user_byid')
        model = User()  # 实例化一个对象，将查询结果逐一添加给对象的属性
        rows = getUserByID(id)
        if rows:
            assert len(rows)==1
            rows = rows[0]
            result = {'isAuth': False}
            result['isAuth'] = True
            model.id = rows[0]
            model.username = rows[1]
            model.email = rows[2]
        return model

class User_Signup:
    @classmethod
    def signup(cls, username, email, password):
        result = {'check': False}
        model = User()
        # 缺少check unique email
        row = addUser(username, email, password)
        model.id = row[0]
        model.username = row[1]
        model.email = row[2]
        result['check'] = True
        return result, model