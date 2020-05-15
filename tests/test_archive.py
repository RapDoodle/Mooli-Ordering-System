import models.model_archive as m

print(' * Testing: Archive...')

index = m.get_archive_index('Milk Tea')
assert m.get_archive_index('Milk Tea') == index
assert m.get_archive_index('thisisanextremelyrandomstring') == index + 1

print(' ✓ Archive has passed all the tests')
