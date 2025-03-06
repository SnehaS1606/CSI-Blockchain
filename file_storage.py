import hashlib
import os
import threading

# Storage for chunks (key: CID, value: chunk data)
chunk_storage = {}

# Storage for file metadata (key: file name, value: list of CIDs)
file_metadata = {}

def generate_cid(data):
    """Generate a CID (hash) for a chunk of data."""
    return hashlib.sha256(data).hexdigest()

def store_file(file_path):
    """
    Store a file by breaking it into chunks and storing them.
    Deduplication is applied to avoid storing duplicate chunks.
    """
    with open(file_path, "rb") as file:
        data = file.read()
        file_name = os.path.basename(file_path)
        chunk_size = 1024  # 1 KB chunks (you can adjust this)
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        cids = []

        for chunk in chunks:
            cid = generate_cid(chunk)
            if cid not in chunk_storage:  # Deduplication
                chunk_storage[cid] = chunk
            cids.append(cid)

        file_metadata[file_name] = cids
        print(f"Stored file: {file_name} with CIDs: {cids}")

def retrieve_file(file_name, output_path):
    """
    Retrieve a file by fetching its chunks and combining them.
    This is a sequential implementation.
    """
    if file_name not in file_metadata:
        print(f"File {file_name} not found.")
        return

    cids = file_metadata[file_name]
    chunks = []

    for cid in cids:
        if cid in chunk_storage:
            chunks.append(chunk_storage[cid])
        else:
            print(f"Chunk {cid} not found.")
            return

    # Combine chunks to reconstruct the file
    data = b"".join(chunks)
    with open(output_path, "wb") as file:
        file.write(data)
    print(f"Retrieved file: {file_name} to {output_path}")

def fetch_chunk(cid, chunks, index):
    """
    Helper function to fetch a chunk and store it in the correct position.
    Used for parallel retrieval.
    """
    if cid in chunk_storage:
        chunks[index] = chunk_storage[cid]
    else:
        print(f"Chunk {cid} not found.")

def retrieve_file_parallel(file_name, output_path):
    """
    Retrieve a file by fetching its chunks in parallel and combining them.
    This is a faster implementation using threads.
    """
    if file_name not in file_metadata:
        print(f"File {file_name} not found.")
        return

    cids = file_metadata[file_name]
    chunks = [None] * len(cids)
    threads = []

    # Create and start threads to fetch chunks in parallel
    for i, cid in enumerate(cids):
        thread = threading.Thread(target=fetch_chunk, args=(cid, chunks, i))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Combine chunks to reconstruct the file
    data = b"".join(chunks)
    with open(output_path, "wb") as file:
        file.write(data)
    print(f"Retrieved file: {file_name} to {output_path}")

# Example usage
if __name__ == "__main__":
    # Step 1: Store a file
    store_file("example.txt")  # Replace "example.txt" with your file path

    # Step 2: Retrieve the file (sequential)
    retrieve_file("example.txt", "output_sequential.txt")

    # Step 3: Retrieve the file (parallel)
    retrieve_file_parallel("example.txt", "output_parallel.txt")