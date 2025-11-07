from Crypto.PublicKey import RSA
key = RSA.generate(2048)
open("receiver_private.pem","wb").write(key.export_key())
open("receiver_public.pem","wb").write(key.publickey().export_key())
