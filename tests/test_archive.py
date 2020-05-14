import models.model_archive as m

print(' * Testing: Archive...')

assert m.get_archive_index('Milk Tea') == 1
assert m.get_archive_index('Milk Tea') == 1
assert m.get_archive_index(12.99) == 2

print(' ✓ Archive has passed all the tests')
