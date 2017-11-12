# -*- encoding: utf8 -*-
# © Toons

from ecdsa.keys import SigningKey
from ecdsa.util import sigencode_der_canonize
from ecdsa.curves import SECP256k1

from . import __PY3__, StringIO, ArkyDict, arkydify
if not __PY3__: import cfg, slots
else: from . import cfg, slots

import base58, struct, hashlib, binascii, requests, json

# byte as int conversion
basint = (lambda e: e) if __PY3__ else \
			(lambda e: ord(e))
# read value as binary data from buffer
unpack = lambda fmt, fileobj: struct.unpack(fmt, fileobj.read(struct.calcsize(fmt)))
# write value as binary data into buffer
pack = lambda fmt, fileobj, value: fileobj.write(struct.pack(fmt, *value))
# read bytes from buffer
unpack_bytes = lambda f, n: unpack("<"+"%ss" % n, f)[0]
# write bytes into buffer
pack_bytes = (lambda f, v: pack("<"+"%ss" % len(v), f, (v,))) if __PY3__ else \
				(lambda f, v: pack("<"+"s" * len(v), f, v))


# define core exceptions
class NotGrantedAttribute(Exception): pass


class NoSecretDefinedError(Exception): pass


class NoSenderDefinedError(Exception): pass


class NotSignedTransactionError(Exception): pass


class StrictDerSignatureError(Exception): pass


def _hexlify(data):
	result = binascii.hexlify(data)
	return str(result.decode() if isinstance(result, bytes) else result)


def _unhexlify(data):
	result = binascii.unhexlify(data)
	return result if isinstance(result, bytes) else result.encode()


def _compressEcdsaPublicKey(pubkey):
	first, last = pubkey[:32], pubkey[32:]
	# check if last digit of second part is even (2%2 = 0, 3%2 = 1)
	even = not bool(basint(last[-1]) % 2)
	return (b"\x02" if even else b"\x03") + first


def getKeys(secret="passphrase", seed=None, network=None):
	"""
	Generate keyring containing network, public key, signing and checking keys as
	attribute. secret or seed have to be provided, if network is not,
	cfg.__NETWORK__ is automatically selected.

	Keyword arguments:
	secret (str or bytes) -- a human pass phrase
	seed (byte)           -- a sha256 sequence bytes (private key actualy)
	network (object)      -- a python object

	Returns ArkyDict
	"""
	network = ArkyDict(**network) if network else cfg.__NETWORK__  # use cfg.__NETWORK__ network by default
	seed = hashlib.sha256(secret.encode("utf8") if not isinstance(secret, bytes) else secret).digest() if not seed else seed

	keys = ArkyDict()
	# save wallet address
	keys.wif = getWIF(seed, network)
	# save network option
	keys.network = network
	# generate signing and verifying object and public key
	keys.signingKey = SigningKey.from_secret_exponent(int(binascii.hexlify(seed), 16), SECP256k1, hashlib.sha256)
	keys.checkingKey = keys.signingKey.get_verifying_key()
	keys.public = _compressEcdsaPublicKey(keys.checkingKey.to_string())

	return keys


def getAddress(keys):
	"""
	Computes ARK address from keyring.

	Argument:
	keys (ArkyDict) -- keyring returned by `getKeys`

	Returns str
	"""
	network = keys.network
	ripemd160 = hashlib.new('ripemd160', keys.public).digest()[:20]
	seed = network.pubKeyHash + ripemd160
	return base58.b58encode_check(seed)


def getWIF(seed, network):
	"""
	Computes WIF address from seed.

	Argument:
	seed (bytes)     -- a sha256 sequence bytes
	network (object) -- a python object

	Returns str
	"""
	# network = network
	compressed = network.get("compressed", True)
	seed = network.wif + seed[:32] + (b"\x01" if compressed else b"")
	return base58.b58encode_check(seed)


def getBytes(transaction):
	"""
	Hash transaction object into bytes data.

	Argument:
	transaction (core.Transaction) -- transaction object

	Returns bytes sequence
	"""
	buf = StringIO() # create a buffer

	# write type and timestamp
	pack("<bi", buf, (transaction.type, int(transaction.timestamp)))
	# write senderPublicKey as bytes in buffer
	try:
		pack_bytes(buf, _unhexlify(transaction.senderPublicKey))
	# raise NoSenderDefinedError if no sender defined
	except (AttributeError, TypeError):
		raise NoSenderDefinedError("%r does not belong to any ARK account" % transaction)
	# unused
	if getattr(transaction, "requesterPublicKey", False):
		pack_bytes(buf, _unhexlify(transaction.requesterPublicKey))
	# decode reciever Ark address
	if getattr(transaction, "recipientId", False):
		recipientId = base58.b58decode_check(transaction.recipientId)
	else:
		recipientId = b"\x00"*21
	pack_bytes(buf, recipientId)
	# put vendor field value (64 bytes limited)
	if getattr(transaction, "vendorField", False):
		vendorField = transaction.vendorField[:64].encode().ljust(64, b"\x00")
	else:
		vendorField = b"\x00"*64
	pack_bytes(buf, vendorField)

	# write amount and fee value
	pack("<QQ", buf, (int(transaction.amount),int(transaction.fee)))

	typ = transaction.type
	if typ == 1 and "signature" in transaction.asset:
		pack_bytes(buf, _unhexlify(transaction.asset.signature.publicKey))
	elif typ == 2 and "delegate" in transaction.asset:
		pack_bytes(buf, transaction.asset.delegate.username.encode())
	elif typ == 3 and "votes" in transaction.asset:
		pack_bytes(buf, ("".join(transaction.asset.votes)).encode())
	elif typ == 4 and "multisignature" in transaction.asset:
		pass

	# if there is a signature
	if getattr(transaction, "signature", False):
		pack_bytes(buf, _unhexlify(transaction.signature))
	# if there is a second signature
	if getattr(transaction, "signSignature", False):
		pack_bytes(buf, _unhexlify(transaction.signSignature))

	result = buf.getvalue()
	buf.close()
	return result.encode() if not isinstance(result, bytes) else result


def fromBytes(data):
	"""
	Generate Transaction object from bytes data.

	Argument:
	data (bytes) -- transaction hash generated by core.getBytes

	Returns core.Transaction object
	"""

	tx = Transaction()
	buf = StringIO(data)

	tx.type, tx.timestamp = unpack("<bi", buf)
	object.__setattr__(tx, "key_one", ArkyDict(public=unpack_bytes(buf, 33)))
	rid = unpack_bytes(buf, 21).replace(b"\x00", b"")
	if rid != "": tx.recipientId = base58.b58encode_check(rid)
	vf = unpack_bytes(buf, 64).replace(b"\x00", b"").decode()
	if vf != "": tx.vendorField = vf
	tx.amount, fee = unpack("<QQ", buf)

	idx = []
	for i in range(len(data)):
		if basint(data[i]) == 0x30:
			j = i+basint(data[i+1])+2
			if j <= len(data):
				try:
					object.__setattr__(tx, "signature" if not hasattr(tx, "signature") else "signSignature", _hexlify(checkStrictDER(data[i:j])))
					idx.append(i)
				except:
					pass

	start = buf.tell()
	stop = len(data) if not len(idx) else min(idx)
	asset = data[start:stop]

	if tx.type == 1:
		object.__setattr__(tx, "asset", ArkyDict(signature=ArkyDict(publicKey=_hexlify(asset))))
	elif tx.type == 2:
		object.__setattr__(tx, "asset", ArkyDict(delegate=ArkyDict(username=str(asset.decode()))))
	elif tx.type == 3:
		object.__setattr__(tx, "asset", ArkyDict(votes=[str(asset[i:i+67].decode()) for i in range(0, len(asset), 67)]))
	elif tx.type == 4:
		pass

	if hasattr(tx, "signature"):
		object.__setattr__(tx, "id", _hexlify(hashlib.sha256(getBytes(tx)).digest()))
	
	return tx


# toonsbuf here :)
def getHex(transaction): return _hexlify(getBytes(transaction))


def fromHex(hexa): return fromBytes(_unhexlify(hexa))


def signSerial(serial, signingKey):
	"""
	Sign serialized transaction using signingKey.

	Argument:
	serial (serial)                    -- transaction hash generated by core.getBytes
	signingKey (ecdsa.keys.SigningKey) -- signing key given by core.getKeys

	Updates serial and returns signature + id
	"""

	if not isinstance(serial, ArkyDict): serial = arkydify(serial)
	signature = _hexlify(signingKey.sign_deterministic(getBytes(serial), hashlib.sha256, sigencode=sigencode_der_canonize))
	setattr(serial, "signSignature" if getattr(serial, "signature", False) else "signature", signature)
	id_ = _hexlify(hashlib.sha256(getBytes(serial)).digest())
	setattr(serial, "id", id_)
	return {"signature": signature, "id": id_}


def checkStrictDER(sig):
	"""
	https://github.com/bitcoin/bips/blob/master/bip-0066.mediawiki#der-encoding-reference
	Check strict DER signature compliance.

	Argument:
	sig (bytes) -- signature bytes sequence

	Raises StrictDerSignatureError exception or returns sig
	"""
	sig_len = len(sig)
	# Extract the length of the R element.
	r_len = basint(sig[3])
	# Extract the length of the S element.
	s_len = basint(sig[5+r_len])

	# Minimum and maximum size constraints.
	if 8 > sig_len > 72:
		raise StrictDerSignatureError("Bad signature size (<8 or >72)")
	# A signature is of type 0x30 (compound).
	if basint(sig[0]) != 0x30:
		raise StrictDerSignatureError("A signature is not of type 0x30 (compound)")
	# Make sure the length covers the entire signature.
	if basint(sig[1]) != (sig_len - 2):
		raise StrictDerSignatureError("Length %d does not covers the entire signature (%d)" % (sig[1], sig_len))
	# Make sure the length of the S element is still inside the signature.
	if (5 + r_len) >= sig_len:
		raise StrictDerSignatureError("S element is not inside the signature")
	# Verify that the length of the signature matches the sum of the length of the elements.
	if (r_len + s_len + 6) != sig_len:
		raise StrictDerSignatureError("Signature length does not matches sum of the elements")
	# Check whether the R element is an integer.
	if basint(sig[2]) != 0x02:
		raise StrictDerSignatureError("R element is not an integer")
	# Zero-length integers are not allowed for R.
	if r_len == 0:
		raise StrictDerSignatureError("Zero-length is not allowed for R element")
	# Negative numbers are not allowed for R.
	if basint(sig[4]) & 0x80:
		raise StrictDerSignatureError("Negative number is not allowed for R element")
	# Null bytes at the start of R are not allowed, unless R would otherwise be interpreted as a negative number.
	if r_len > 1 and basint(sig[4]) == 0x00 and not basint(sig[5]) & 0x80:
		raise StrictDerSignatureError("Null bytes at the start of R element is not allowed")
	# Check whether the S element is an integer.
	if basint(sig[r_len+4]) != 0x02:
		raise StrictDerSignatureError("S element is not an integer")
	# Zero-length integers are not allowed for S.
	if s_len == 0:
		raise StrictDerSignatureError("Zero-length is not allowed for S element")
	# Negative numbers are not allowed for S.
	if basint(sig[r_len+6]) & 0x80:
		raise StrictDerSignatureError("Negative number is not allowed for S element")
	# Null bytes at the start of S are not allowed, unless S would otherwise be interpreted as a negative number.
	if s_len > 1 and basint(sig[r_len+6]) == 0x00 and not basint(sig[r_len+7]) & 0x80:
		raise StrictDerSignatureError("Null bytes at the start of S element is not allowed")
	return sig


class Transaction(object):
	"""
	Transaction object is the core of the API. This object is a container with smart
	behaviour according to attribute value that are settled in.

	Attributes that can be set using object interface :
	type               (int)
	amount             (int)
	timestamp          (float)
	asset              (ArkyDict)
	secret             (str)
	vendorField        (str)
	recipientId        (str)
	requesterPublicKey (str)
	"""
	# here are attribute that can be set through object interface
	attr = ["type", "amount", "timestamp", "asset", "vendorField", "secret", "secondSecret", "recipientId", "requesterPublicKey"]

	# here are some shortcut using public key
	senderPublicKey = property(lambda obj:_hexlify(obj.key_one.public), None, None, "alias for public key, read-only attribute")
	address = property(lambda obj:base58.b58encode_check(cfg.__NETWORK__.pubKeyHash + hashlib.new('ripemd160', obj.key_one.public).digest()[:20]), None, None, "alias for sender address, read-only attribute")

	def __init__(self, **kwargs):
		# the four minimum attributes that defines a transaction
		self.type = kwargs.pop("type", 0)
		self.amount = kwargs.pop("amount", 0)
		self.timestamp = slots.getTime() - 60  # get backward 60s to avoid error:Invalid transaction timestamp
		self.asset = kwargs.pop("asset", ArkyDict())
		for attr,value in kwargs.items():
			setattr(self, attr, value)

	def __setattr__(self, attr, value):
		if attr not in Transaction.attr:
			raise NotGrantedAttribute("%s attribute can not be set using object interface" % attr)
		if attr == "secret":
			# secret is not stored
			self._unsign()
			keys = getKeys(value)
			object.__setattr__(self, "key_one", keys)
		elif attr == "secondSecret":
			# second secret is not stored
			if hasattr(self, "signSignature"):
				delattr(self, "signSignature")
			object.__setattr__(self, "key_two", getKeys(value))
		elif attr == "type":
			self._unsign()
			# when doing `<object>.type = value` automaticaly set the associated fees
			if value == 0:   object.__setattr__(self, "fee", cfg.__FEES__.send)
			elif value == 1: object.__setattr__(self, "fee", cfg.__FEES__.secondsignature)
			elif value == 2: object.__setattr__(self, "fee", cfg.__FEES__.delegate)
			elif value == 3: object.__setattr__(self, "fee", cfg.__FEES__.vote)
			elif value == 4: object.__setattr__(self, "fee", cfg.__FEES__.multisignature)
			elif value == 5: object.__setattr__(self, "fee", cfg.__FEES__.dapp)
			object.__setattr__(self, attr, value)
		elif value != None:
			self._unsign()
			object.__setattr__(self, attr, value)

	def __del__(self):
		if hasattr(self, "key_one"): delattr(self, "key_one")
		if hasattr(self, "key_two"): delattr(self, "key_two")

	def __repr__(self):
		return "<%(signed)s type-%(type)d transaction(A%(amount).8f) from %(from)s to %(to)s>" % {
			"signed": "double-signed" if hasattr(self, "signSignature") else
				"signed" if hasattr(self, "signature") else
					"unsigned",
			"type": self.type,
			"amount": self.amount/100000000.,
			"from": self.address,
			"to": getattr(self, "recipientId", '"No one"')
		}

	def _unsign(self):
		if hasattr(self, "signature"):
			delattr(self, "signature")
		if hasattr(self, "signSignature"):
			delattr(self, "signSignature")
		if hasattr(self, "id"):
			delattr(self, "id")

	def sign(self, secret=None, secondSecret=None):
		self._unsign()
		# if secret is given, set a new secret (setting a new key_one)
		if secret != None:
			self.secret = secret
		# if no key_one attribute is set --> no secret defined, no owner defined
		elif not hasattr(self, "key_one"):
			raise NoSecretDefinedError("No secret defined")
		# store signature under signature attribute
		stamp1 = getattr(self, "key_one").signingKey.sign_deterministic(getBytes(self), hashlib.sha256, sigencode=sigencode_der_canonize)
		object.__setattr__(self, "signature", _hexlify(stamp1))
		
		# if secondSecret is given, set a new secondSecret (setting a new key_two), only if account had registered a second signature
		if secondSecret != None:
			self.secondSecret = secondSecret
		# if key_two attribute is set
		if hasattr(self, "key_two"):
			# store second signature under signSignature attribute
			stamp2 = getattr(self, "key_two").signingKey.sign_deterministic(getBytes(self), hashlib.sha256, sigencode=sigencode_der_canonize)
			object.__setattr__(self, "signSignature", _hexlify(stamp2))
		
		# generate id
		object.__setattr__(self, "id", _hexlify(hashlib.sha256(getBytes(self)).digest()))
		return self

	def serialize(self):
		data = ArkyDict()
		for attr in [a for a in [
			"id", "timestamp", "type", "fee", "amount", 
			"recipientId", "senderPublicKey", "requesterPublicKey", "vendorField",
			"asset", "signature", "signatures", "signSignature"
		] if hasattr(self, a)]:
			value = getattr(self, attr)
			if attr in ["amount", "timestamp", "fee"]:
				value = int(value)
			elif attr == "asset":
				value = arkydify(value)
			setattr(data, attr, value)
		return data
