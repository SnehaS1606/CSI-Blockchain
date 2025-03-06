# CSI-Blockchain
File Storage System with Deduplication and Parallel Retrieval
This project implements a file storage system that efficiently stores and retrieves files by breaking them into smaller chunks and avoiding duplicate storage. The system uses Content Identifiers (CIDs) to uniquely identify chunks, enabling deduplication. Files can be retrieved either sequentially or in parallel for improved performance.

Key Features
Chunking: Files are divided into smaller chunks (e.g., 1 KB each).

Deduplication: Identical chunks are stored only once, saving storage space.

CID Generation: Each chunk is assigned a unique identifier using the SHA-256 hash function.

Parallel Retrieval: Chunks are fetched simultaneously to speed up file reconstruction.

How It Works
Store a File: The file is split into chunks, and each chunk is hashed to generate a CID. If a chunk with the same CID already exists, it is not stored again (deduplication).

Retrieve a File: The file is reconstructed by fetching its chunks using their CIDs. Retrieval can be done sequentially or in parallel for faster performance.

Verification: The retrieved file is compared with the original to ensure data integrity.

Technologies Used
Python: For implementing the storage and retrieval logic.

SHA-256: For generating unique CIDs.

Threading: For parallel retrieval of chunks.

Applications
Efficient storage systems (e.g., cloud storage, backup systems).

Data deduplication for reducing storage costs.

Learning parallel processing and file handling in Python.

