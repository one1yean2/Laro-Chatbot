class Config(object):

    # Flask
    SECRET_KEY = "84b9ebfa0b5bab16df6601da5c35b0f8ebb5d062ebdddd14bff178960dfeea30"
    # SERVER_NAME = "127.0.0.1:5000"
    # SERVER_NAME = "938e-125-27-102-233.ngrok-free.app"
    APPLICATION_ROOT = "/"
    PREFERRED_URL_SCHEME = "http"
    
    #Flask Redis
    REDIS_URL = "redis://localhost:6379"
    
    #Flask Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USERNAME = "yeeninw55@gmail.com"
    MAIL_PASSWORD = "gqdg lvgj eygn rpma"
    MAIL_USE_TLS = True
    
    # Flask SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///laro2.db"
    
    # Flask APScheduler
    SCHEDULER_API_ENABLED = True