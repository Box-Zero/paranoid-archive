import os
import sys
import bcrypt
import zipfile

def create_archive(correct_pwd, trap_pwd, correct_file, trap_file, archive_name):
    correct_pwd_hash = bcrypt.hashpw(correct_pwd.encode('utf-8'), bcrypt.gensalt())
    trap_pwd_hash = bcrypt.hashpw(trap_pwd.encode('utf-8'), bcrypt.gensalt())
    print(correct_pwd_hash)
    print(len(trap_pwd_hash))

    correct_file_zip_name = correct_pwd_hash.hex()
    trap_file_zip_name = trap_pwd_hash.hex()

    print(correct_file_zip_name)
    print(trap_file_zip_name)

    with zipfile.ZipFile(correct_file_zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(correct_file)
        zipf.setpassword(bytes(correct_pwd, 'utf-8'))

    with zipfile.ZipFile(trap_file_zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(trap_file)
        zipf.setpassword(bytes(trap_pwd, 'utf-8'))

    with open(correct_file_zip_name, 'rb') as z1:
        zip1_data = z1.read()

    with open(trap_file_zip_name, 'rb') as z2:
        zip2_data = z2.read()
    
    with open(archive_name, 'wb') as output:
        output.write(correct_pwd_hash)
        output.write(trap_pwd_hash)
        output.write(zip1_data)
        output.write(zip2_data)

    os.remove(correct_file_zip_name)
    os.remove(trap_file_zip_name)

def extract_archive(archive_name, password):
    with open(archive_name, 'rb') as f:
        first_hash_block = f.read(60)
        second_hash_block = f.read(60)
        print(first_hash_block)
        print(second_hash_block)
        if bcrypt.checkpw(password.encode('utf-8'), first_hash_block):
            print("correct password")
        else:
            print("incorrect password")

if __name__ == "__main__":
    print("working...")
    # create_archive("correct_pwd", "trap_pwd", "correct_file", "trap_file", "archive.zip")
    extract_archive("archive.zip", "correct_pwd")