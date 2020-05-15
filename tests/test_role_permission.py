import models.model_role as m

print(' * Testing: Role and Permission...')

assert len(m.get_all_permissions()) == 0
assert len(m.get_all_roles()) == 0
m.add_role('superadmin', [])
assert len(m.get_all_roles()) == 1
m.add_permission('dashboard')
m.add_permission('product')
m.add_permission('coupon')
m.add_role('admin', [1, 2])
assert len(m.get_all_roles()) == 2
assert len(m.get_all_permissions()) == 3
m.delete_permission(1)
assert len(m.get_all_permissions()) == 2
m.add_permission('report')
m.update_role(2, 'product_manager', [2, 4])
assert len(m.get_permissions(2, 'role_id')) == 2
assert len(m.get_permissions('product_manager', 'role_name')) == 2

print(' ✓ Role and Permission has passed all the tests')
