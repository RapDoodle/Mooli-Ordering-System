import models.model_customer as m

print('[UNIT TESTING] Testing: Customer...')

m.add_customer('bowenwu', 'bowenwu@gmail.com', 'Testpassword12', 'Bowen', 'WU', 'M', '(310)-873-7333')
m.verify_credential('bowenwu', 'Testpassword12 ')
m.change_password('1000000', 'Testpassword123')
m.verify_credential('bowenwu', 'Testpassword123')

print('[UNIT TESTING] Customer has passed all the tests')
