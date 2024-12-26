
def _pre_init_method(env):
    env.cr.execute("""update account_payment_method set code='new_third_party_checks_old' where code='new_third_party_checks';""")
    env.cr.execute("""update account_payment_method set code='in_third_party_checks_old' where code='in_third_party_checks';""")
    env.cr.execute("""update account_payment_method set code='out_third_party_checks_old' where code='out_third_party_checks';""")
