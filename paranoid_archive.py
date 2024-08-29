import zipfile
import pyAesCrypt
import os

class ParanoidArchive:
    def __init__(self, archive_name, real_file, fake_file, correct_password, buffer_size=64*1024):
        self.archive_name = archive_name
        self.real_file = real_file
        self.fake_file = fake_file
        self.correct_password = correct_password
        self.buffer_size = buffer_size

    def encrypt_real_file(self):
        encrypted_file_name = f"{self.real_file}.aes"
        pyAesCrypt.encryptFile(self.real_file, encrypted_file_name, self.correct_password, self.buffer_size)
        return encrypted_file_name

    def create_archive(self):
        encrypted_file = self.encrypt_real_file()
        with zipfile.ZipFile(self.archive_name, 'w') as zipf:
            zipf.write(encrypted_file)
            zipf.write(self.fake_file)
        os.remove(encrypted_file)
        print(f"Created {self.archive_name} containing encrypted and fake files.")

    def extract_file(self, password):
        with zipfile.ZipFile(self.archive_name, 'r') as zipf:
            if password == self.correct_password:
                zipf.extract(f"{self.real_file}.aes")
                try:
                    pyAesCrypt.decryptFile(f"{self.real_file}.aes", self.real_file, password, self.buffer_size)
                    os.remove(f"{self.real_file}.aes")
                    print("Correct file extracted and decrypted!")
                except ValueError:
                    print("Wrong password, cannot decrypt!")
            else:
                zipf.extract(self.fake_file)
                print("Fake file extracted.")

if __name__ == "__main__":
    print("Started")
    archive = ParanoidArchive(
        archive_name="protected_data.zip",
        real_file="real_data.txt",
        fake_file="fake_data.txt",
        correct_password="correct_password"
    )
    
    # Create the archive
    archive.create_archive()

    # Attempt to extract based on user password
    user_password = input("Enter the password: ")
    archive.extract_file(user_password)
