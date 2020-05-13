import models.model_comment as m

print('[UNIT TESTING] Testing: Comment...')

m.add_comment('1000000', 1, 4, 'I love milk tea.')
m.add_comment(1000001, 1, 2, 'Poor taste ever!!')
m.add_comment(1000001, 1, 5, 'Wow!!')
m.add_comment(1000000, 1, 5, 'Great!!')
m.add_comment(1000000, 1, 5, 'Great!!')
m.add_comment(1000000, 1, 5, 'Great!!')
assert len(m.get_comments(param = 1, limit = 5, offset = 0)) == 5
m.remove_comment(4)
m.remove_comment(5)
m.remove_comment(6)
assert len(m.get_comments(param = 1, limit = 5, offset = 0)) == 3

print('[UNIT TESTING] Comment has passed all the tests')
