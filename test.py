from setup import init_test_db

init_test_db()

import tests.test_category
import tests.test_product
import tests.test_user
import tests.test_redeem_card
import tests.test_comment
import tests.test_coupon
import tests.test_item
import tests.test_order
