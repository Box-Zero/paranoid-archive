from argparse import ArgumentParser
import zipfile
import pyAesCrypt
import os
import sys

class ParanoidArchive:
    def __init__(self, archive_name, correct_password, buffer_size=64*1024):
        self.archive_name = archive_name
        self.correct_password = correct_password
        self.buffer_size = buffer_size

    def encrypt_file(self, file_name):
        encrypted_file_name = f"{file_name}.aes"
        pyAesCrypt.encryptFile(file_name, encrypted_file_name, self.correct_password, self.buffer_size)
        return encrypted_file_name

    def create_archive(self, real_file, fake_file):
        encrypted_file = self.encrypt_file(real_file)
        with zipfile.ZipFile(self.archive_name, 'w') as zipf:
            zipf.write(encrypted_file)
            zipf.write(fake_file)
        os.remove(encrypted_file)
        print(f"Created {self.archive_name} containing encrypted and fake files.")

    def extract_file(self, password):
        with zipfile.ZipFile(self.archive_name, 'r') as zipf:
            if password == self.correct_password:
                zipf.extract(f"{self.archive_name.split('.')[0]}.aes")
                try:
                    pyAesCrypt.decryptFile(f"{self.archive_name.split('.')[0]}.aes", self.archive_name.split('.')[0], password, self.buffer_size)
                    os.remove(f"{self.archive_name.split('.')[0]}.aes")
                    print("Correct file extracted and decrypted!")
                except ValueError:
                    print("Wrong password, cannot decrypt!")
            else:
                zipf.extract(f"{self.archive_name.split('.')[0]}.txt")
                print("Fake file extracted.")

def main():
    parser = ArgumentParser(prog='cli')
    parser.add_argument('compress', help="Compress using Paranoid-Archive")
    parser.add_argument('extract', help="Extract using Paranoid-Archive")
    
    parser.add_argument('--archive_name', help="Name of the archive to compress using Paranoid-Archive")
    parser.add_argument('--real_file_name', help="Name of the real file to compress using Paranoid-Archive, this will be the output of extraction if correct password is provided")
    parser.add_argument('--fake_file_name', help="Name of the fake file to compress using Paranoid-Archive, this will be the output of extraction if wrong password is provided.")
    parser.add_argument('--correct_password', help="The correct password")
    parser.add_argument('--paranoid_password', help="The paranoid password")

    args = parser.parse_args()

if __name__ == '__main__':
    main()
