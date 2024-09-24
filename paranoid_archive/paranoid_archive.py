import os
import sys
import bcrypt
import zipfile
import io


ZIP_SIGNATURE = b'\x50\x4b\x03\x04'
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
        data = f.read()
        first_zip, second_zip = separate_files(data)

        if bcrypt.checkpw(password.encode('utf-8'), first_hash_block):
            extract_zipfile(first_zip, password)
            print("correct password")
        elif bcrypt.checkpw(password.encode('utf-8'), second_hash_block):
            extract_zipfile(second_zip, password)
            print("trap password entered")
        else:
            print("wrong password")




def separate_files(data):
    first_zip_start = data.find(ZIP_SIGNATURE)
    if first_zip_start == -1:
        raise ValueError("First ZIP signature not found")
    second_zip_start = data.find(ZIP_SIGNATURE, first_zip_start + 1)
    if second_zip_start == -1:
        raise ValueError("Second ZIP signature not found")
    first_zip = data[first_zip_start:second_zip_start]
    second_zip = data[second_zip_start:]
    return first_zip, second_zip

def extract_zipfile(data, password):
    output_dir = os.getcwd()
    with io.BytesIO(data) as file_like_object:

        with zipfile.ZipFile(file_like_object, 'r') as zipf:
            for file_info in zipf.infolist():
                try:
                    zipf.extract(file_info, path=output_dir, pwd=bytes(password, 'utf-8'))
                except RuntimeError as e:
                    print(f"Failed to extract {file_info.filename}: {e}")

if __name__ == "__main__":
    print("working...")
    # create_archive("correct_pwd", "trap_pwd", "correct_file", "trap_file", "archive.zip")
    extract_archive("archive.zip", "correct_pwd")