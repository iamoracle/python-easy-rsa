from pathlib import Path

from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

class Encryption:

    public_key = None

    private_key = None

    def __init__(self, path: Path = None, name: tuple[str, str] = ('public.pem', 'private.pem'), key_length: int = 4096):
        """
        RSA wrapper to generate encryption keys, sign a message, decrypt and encrypt messages\n
        args:\n
        [path]: directory where the keys are stored or to be stored\n
        [name]: names of the files \n
        [key_length]: encryption key length \n
        """

        self.path = path if path else Path(__file__).parent.absolute()

        self.public_name = name[0]

        self.private_name = name[1]

        self.key_length = key_length

    def generate_keys(self):
        """
        WARNING: danger\n
        will overwrite existing keys with the same name and path \n
        will overwrite keys in memory too! \n
        """

        key = RSA.generate(self.key_length)

        self.private_key = key.export_key('PEM')

        self.public_key = key.publickey().exportKey('PEM')

    def load_key(self, name: str, path = None) -> bytes:
        """
        this function 
        loads a particular file containing a key
        """

        path = path if path else self.path

        path = self.path

        file_full_path = str(path / name)

        return self.__file_read_helper(file_full_path)

    def load_keys(self):
        """
        loads the initialized keys in __init__ \n
        will overwrite keys in memory!
        """

        self.public_key = self.load_key(name=self.public_name)

        self.private_key = self.load_key(name=self.private_name)


    def __file_read_helper(self, path) -> bytes:
        """
        does the actual work of loading the file
        """

        with open(path, 'r') as file:

            return file.read().encode()

    def __file_save_helper(self, path, data):
        """
        does the actual work of saving the file
        """

        with open(path, 'w') as file:

            file.write(data.decode())    

    def save_key(self, key, name: str, path: Path = None):

        path = path if path else Path(__file__).parent.absolute()

        file_path = str(path / name)

        self.__file_save_helper(file_path, key)


    def save_keys(self, path: Path = None, name: tuple[str, str] = ('public.pem', 'private.pem')):

        public_name = name[0] if name else self.public_name

        private_name = name[1] if name else self.private_name

        self.save_key(self.public_key, path=path, name=public_name)

        self.save_key(self.private_key, path=path, name=private_name)

    def encrypt(self, message: str, public_key: str) -> str:

        public_key = public_key if public_key else self.public_key

        public_key = RSA.importKey(public_key)

        pkcsi_public_key = PKCS1_OAEP.new(public_key)

        encrypted_message = pkcsi_public_key.encrypt(message.encode())

        return encrypted_message.hex()

    def decrypt(self, message: str, private_key: str) -> str:

        private_key = private_key if private_key else self.private_key

        private_key = RSA.importKey(private_key)

        pkcsi_private_key = PKCS1_OAEP.new(private_key)

        decrypted_message = pkcsi_private_key.decrypt(bytes.fromhex(message))

        return decrypted_message.decode()

    def sign(self, message: str, private_key: str = None) -> str:

        private_key = private_key if private_key else self.private_key

        digest = SHA256.new(message.encode())

        private_key = RSA.importKey(private_key)

        pkcsi_private_key = PKCS1_v1_5.new(private_key)

        signature = pkcsi_private_key.sign(digest)

        return signature.hex()

    def verify_sign(self, message: str, signature: str, public_key: str = None) -> bool:

        public_key = public_key if public_key else self.public_key

        digest = SHA256.new(message.encode())

        public_key = RSA.importKey(public_key)

        pkcsi_public_key = PKCS1_v1_5.new(public_key)

        signature = bytes.fromhex(signature)

        verified = pkcsi_public_key.verify(digest, signature)

        return verified
