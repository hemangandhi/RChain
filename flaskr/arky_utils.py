from arky import api

api.use('rchain')

def get_threads(root):
    """
    Traverses the ledge and gets everything that's
    a successor node of the root thread (basically
    treating everything as a tree).

    Returns a list of dictionaries.
    """
    root_id = root.our_id
    for post_transaction in api.get("/api/transactions"):
        post = post_transaction.vendorField
        #work with it!

def make_user(password):
    """
    Returns an address for a user and their secret.
    """
    pass

def get_user_stats(user_address):
    """
    Given a key, returns the user's account info as a dict.
    Has address, unconfirmedBalance, balance, publicKey,
    unconfirmedSignature, secondSignature, secondPublicKey,
    multisignatures.

    Returns None if the user isn't found.
    """
    arky_res = api.get("/api/accounts", address=user_address)
    if not arky_res.success:
        return None
    else:
        return arky_res.account

