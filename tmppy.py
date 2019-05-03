import requests


r = requests.post('https://cst-499-volunteer-api.herokuapp.com/home/account/new/',
					{'account_type' : 'volunteer',
					'username': 'account_test',
					'email' : 'tat@g.com',
					'password' : 'kidskids22',
					'password_confirm' : 'kidskids22'})


print(r.text)
