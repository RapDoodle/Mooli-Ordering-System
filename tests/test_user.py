import models.model_user as m
import controllers.controller_user as c

print(' * Testing: User...')

m.add_user('Bowen_WU', 'bowenwu@gmail.com', 'Testpassword12', 'Bowen', 'WU', 'M', '(310)-873-7333')
m.verify_credential('Bowen_WU', 'Testpassword12 ')
m.change_password('10000', 'Testpassword123')
m.verify_credential('Bowen_WU', 'Testpassword123')
assert c.sign_up('RyanLam', 'ryan@gmail.com', 'Testpassword12345', 'Ryan', 'Lam', 'M') == 10001
m.verify_credential('RyanLam', 'Testpassword12345 ')
assert c.update_user_info(10001, 'Ryan', 'Wong', 'F', '911') == {'status': 200}
assert c.change_password('10001', 'Testpassword12345', 'Testpassword123', 'Testpassword123') == {'status': 200}
m.verify_credential('RyanLam', 'Testpassword123')
# When original password is wrong
assert c.change_password('10001', 'Testpassword12345', 'Testpassword123', 'Testpassword123') == {'error': 'Invalid password'}
# When the new password and verify password don't match
c.change_password('10001', 'Testpassword123', 'Testpassword1234', 'Testpassword123') == {'error': 'Passwords do not match.'}

print(' ✓ User has passed all the tests')
