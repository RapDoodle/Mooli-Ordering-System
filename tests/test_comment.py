import models.model_comment as m

print(' * Testing: Comment...')

m.add_comment('10000', 1, 4, 'I love milk tea.')
m.add_comment(10001, 1, 2, 'Poor taste ever!!')
m.add_comment(10001, 1, 5, 'Wow!!')
m.add_comment(10001, 1, 5, 'Great!!')
m.add_comment(10001, 1, 5, 'Great!!')
m.add_comment(10001, 1, 5, 'Great!!')
assert len(m.get_comments(param = 1, limit = 5, offset = 0)) == 5
m.remove_comment(4)
m.remove_comment(5)
m.remove_comment(6)
assert len(m.get_comments(param = 1, limit = 5, offset = 0)) == 3
assert list(m.get_comments(param = 1, limit = 5, offset = 0)[0].keys()) == ['comment_id', 'user_id', 'product_id', 'rating', 'body', 'created_at']
m.add_comment(10001, 2, 5, 'Love it!')
assert str(m.get_product_ratings(1)) == '3.67'
assert str(m.get_product_ratings(1)) == '3.67'

print(' ✓ Comment has passed all the tests')
