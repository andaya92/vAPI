import EnvironmentPickler

'''
Run to create environment file
Move .pkl to parent dir

'''

env = {
    "STRIPE_API_KEY" : 'sk_test_fWqQzMbbfiKxEJkgJAsJeqXV',
    "DATABASE" : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vol_API',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'mostdope'
    },
}

if __name__ == "__main__":
	EnvironmentPickler.save_obj(env, "volunteer_API_env")