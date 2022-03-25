class Development:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:qwe123123@127.0.0.1/testPlatform'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SESSION_USE_SINGER = True   # cookie中sessionID进行隐藏处理



class Produce:
    pass


env_map = {
    'dev':Development,
    'pro':Produce
}