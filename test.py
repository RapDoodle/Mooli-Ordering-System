from setup import init_test_db

init_test_db()

import tests.test_category
import tests.test_product
import tests.test_user
import tests.test_redeem_card
import tests.test_coupon
import tests.test_cart_item
import tests.test_order
import tests.test_archive
import tests.test_role_permission
import tests.test_staff
