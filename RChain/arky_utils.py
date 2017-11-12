from arky import api
from arky import core
import json

api.use("rchain")

def all_threads():
    """
    Returns every thread in the ledger.
    """
    roots = []
    seen = {}
    trans = api.get("/api/transactions")
    if not trans.success:
        print(trans)
        return None
    for post_transaction in trans.transactions:
        if 'vendorField' not in post_transaction:
            continue
        post = json.loads(post_transaction['vendorField'])
        post['kids'] = []
        if len(seen) == 0:
            roots.append(post)
            seen[post['id']] = post
        elif post['id'] in seen:
            seen[post['id']]['votes'] += post['votes']
        elif post['parent'] in seen:
            seen[post['parent']]['kids'].append(post)
            seen[post['id']] = post
        else:
            seen[post['id']] = post
            roots.append(post)
    return roots


def get_threads(root=None):
    """
    Traverses the ledge and gets everything that's
    a successor node of the root thread (basically
    treating everything as a tree).

    Returns the root post with kids as the direct responses.
    """
    if root is not None:
        root = json.loads(root.vendorField)
        root['kids'] = []
        seen_ids = {root_id: root['id']}
    else:
        seen_ids = {}
    trans = api.get("/api/transactions")
    if not trans.success:
        print(trans)
        return None
    for post_transaction in trans.transactions:
        if 'vendorField' not in post_transaction:
            continue
        post = json.loads(post_transaction['vendorField'])
        if len(seen_ids) == 0:
            seen_ids[post['id']] = post
            root = post
            post['kids'] = []
        elif post is None: continue
        elif post['id'] in seen_ids:
            seen_ids[post['id']]['votes'] += post['votes']
        elif post['parent'] in seen_ids:
            post['kids'] = []
            seen_ids[post['parent']]['kids'].append(post)
            seen_ids[post['id']] = post
    return root

def make_user(password):
    """
    Returns an address for a user and their secret.
    Suppose you have "rv = make_user("something")"
    So the secret is probably rv[1]['signingKey']
    and the address is definately rv[0].
    """
    private_info = core.getKeys(password)
    addr = core.getAddress(private_info)
    return addr, private_info

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

def put_post(post, passpharse):
    tx = core.Transaction(vendorField=post, secret=passpharse)
    api.sendTx(tx)
