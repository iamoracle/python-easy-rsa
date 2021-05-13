# python-easy-rsa

# Generating a Public Key and Private Key 

```python

# the directory where the keys are to be stored
# in this case we are using the current file directory
path = Path(__file__).absolute().parent

# initialize the encrypter
encryption = Encryption(path, name=('public_key.pem', 'private1.pem'))

# generates both private and public keys
encryption.generate_keys()
```

## Loading Existing Private Key and Public Key


```python

# the directory where the keys are stored
# in this case we are using the current file 

# initialize the encrypter
encryption = Encryption(path, name=('public_key.pem', 'private1.pem'))

# loads both private and public keys
encryption.load_keys()

# at this point both public and private keys are loaded in memory
# check example below to encrypt using the load or generate keys

```

## Encrypting a message

```python
# initialize the encrypter
encryption = Encryption(path, name=('public_key.pem', 'private1.pem'))

# generates or load both private and public keys
encryption.load_keys() # or encryption.generate_keys()

encrypted = encryption.encrypt('hello world')

# return encrypted string

decrypted = encryption.decrypt(encrypted)

# returns a decrypted message 
# 'hello world'
```


## Encrypt with a custom key from a custom

```python
# one time encryption

# load a public key file
file_content = open('file.pem')

encryption = Encryption()

encrypted = encryption.encrypt('hello world', file_content)
```


## Decrypt with a custom key from a custom file

```python
# one time decryption

file_content = open('file.pem')

encryption = Encryption()

encrypted_message = 'somethin encrypted'

decrypted = encryption.decrypt('hello world', file_content)

# returns a decrypted message
```


## Sign and Verify Message

``python
# loads key from file
encryption = Encryption(path, name=('public_key.pem', 'private1.pem'))

# generates or load both private and public keys
encryption.load_keys() # or encryption.generate_keys()

# sign a string with a private key
hash = encryption.sign('hello world') # or encryption.sign('hello world', private_key_rfrom_file)
# returns a signed hash 

# verify if a message is signed by a private key using its counter public key 
verified = encryption.verify_sign('hello world', hash) # or encryption.verify_sign('hello world', hash, public_key_from_file)
# returns bool
```
