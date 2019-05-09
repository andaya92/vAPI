import EnvironmentPickler

'''
Run to create environment file
Move .pkl to parent dir

'''

env = {
    "STRIPE_API_KEY" : 'sk_test_fWqQzMbbfiKxEJkgJAsJeqXV',
    "SECRET_KEY" : "2%5*r@ywgx73xg5+1*u8u%p0)@q6sbou7zd1=_+je#k46t)o%7",
    "DB_mysql" : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vol_API',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'mostdope'
    },
    "DB_sqlite" : {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'vol_API',
    },
    "DB_heroku" : {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dd7gonermmlu4d',
        'USER': 'bwwaqpuwcrxdtb',
        'PASSWORD': 'dc17a84de530180fa85638f177c2e3ee7dcaddefb6b844db502c3c4200b4a132',
        'HOST': 'ec2-54-243-241-62.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

if __name__ == "__main__":
	EnvironmentPickler.save_obj(env, "volunteer_API_env")