import hashlib
from pathlib import Path


def compute_file_hash(file_path:Path|str, quiet=False) -> None:
    file_path = Path(file_path)
    hash_path = file_path.with_suffix(file_path.suffix + ".hash")

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found or {file_path} not file.")
    
    with open(file_path, "rb") as file:
        file_hash = hashlib.sha256(file.read()).digest()

    with open(hash_path, "wb") as hash_file:
        hash_file.write(file_hash)
    if not quiet:
        print(f"File hash saved to: {hash_path}.") 


def verify_file_hash(file_path:Path|str, quiet=False) -> bool:
    file_path = Path(file_path)
    hash_path = file_path.with_suffix(file_path.suffix + ".hash")

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found or {file_path} not file.")
    if not hash_path.exists() or not hash_path.is_file():
        if not quiet: print(f"File not found or {hash_path} not file.")
        return False
 
    with open(file_path, "rb") as file:
        calculated_hash = hashlib.sha256(file.read()).digest()

    with open(hash_path, "rb") as hash_file:
        stored_hash = hash_file.read()

    if calculated_hash == stored_hash:
        if not quiet:
            print("Hash of the file match.")
        return True
    if not quiet:
        print("Hash of the file does not match.")
    return False
