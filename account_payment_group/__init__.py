
from . import models

def _pre_init_method(env):
    env.cr.execute("""update account_payment_method set code='new_third_party_checks_' where code='new_third_party_checks';""")
    env.cr.execute("""update account_payment_method set code='in_third_party_checks_' where code='in_third_party_checks';""")
    env.cr.execute("""method set code='out_third_party_checks_' where code='out_third_party_checks';""")
