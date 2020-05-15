import models.model_staff as m
import models.model_role as m_r

print(' * Testing: Staff...')

staff = m.add_staff('mooliadmin', 'mooli@repo.ink', 'Testpassword123', 2)
assert len(m_r.get_permissions(staff, 'user_id')) == 2

print(' ✓ Staff has passed all the tests')
