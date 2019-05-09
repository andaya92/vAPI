import EnvironmentPickler

'''
Run to create environment file
Move .pkl to parent dir

'''

env = {
    "STRIPE_API_KEY" : 'sk_test_fWqQzMbbfiKxEJkgJAsJeqXV',
    "SECRET_KEY" : "2%5*r@ywgx73xg5+1*u8u%p0)@q6sbou7zd1=_+je#k46t)o%7",
    "DATABASE_URL" : 'sqlite:///vol_API.sqlite3',
    "DATABASE_URL_MYSQL" : 'mysql://root:mostdope@127.0.0.1:3306/vol_API'
}

if __name__ == "__main__":
	EnvironmentPickler.save_obj(env, "volunteer_API_env")