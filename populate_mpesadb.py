import argparse
import os
import shutil
import traceback
from getpass import getpass
from pdfminer.high_level import extract_text
from langchain.schema.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    documents = load_documents()
    add_to_chroma(documents)

def load_documents():
    documents = []
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".pdf"):
            filepath = os.path.join(DATA_PATH, filename)
            documents.extend(load_pdf(filepath))
    return documents

def load_pdf(filepath):
    documents = []
    password = None
    
    print(f"Processing file: {filepath}")
    
    # Extract text using pdfminer
    try:
        text = extract_text(filepath, password=password)
        print("Successfully extracted text using pdfminer")
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        password = getpass(f"Enter the password for {filepath}: ")
        try:
            text = extract_text(filepath, password=password)
            print("Successfully extracted text using pdfminer with password")
        except Exception as e:
            print(f"Error extracting text with password: {str(e)}")
            print("Full traceback:")
            traceback.print_exc()
            return documents
    
    # Process extracted text
    lines = text.split('\n')
    metadata = {}
    transactions = []
    detailed_statement_started = False  
    
    for line in lines:
        if "Customer Name:" in line:
            metadata['customer_name'] = line.split(":")[1].strip()
        elif "Mobile Number:" in line:
            metadata['mobile_number'] = line.split(":")[1].strip()
        elif "Statement Period:" in line:
            metadata['statement_period'] = line.split(":")[1].strip()
        elif "DETAILED STATEMENT" in line:
            detailed_statement_started = True
        elif detailed_statement_started and line.strip() and not line.startswith('Page') and not line.startswith('Receipt No.'):
            parts = line.split()
            if len(parts) >= 7:
                transactions.append(parts)
    
    # Create documents
    for index, transaction in enumerate(transactions):
        receipt_no = transaction[0]
        completion_time = f"{transaction[1]} {transaction[2]}"
        details = " ".join(transaction[3:-3])
        status = transaction[-3]
        paid_in = transaction[-2] if transaction[-2] != '-' else '0.00'
        withdrawn = transaction[-1] if transaction[-1] != '-' else '0.00'
        
        text = f"Receipt No: {receipt_no} | Completion Time: {completion_time} | Details: {details} | Status: {status} | Paid In: {paid_in} | Withdrawn: {withdrawn}"
        doc_metadata = {
            **metadata,
            "source": filepath,
            "transaction_index": index + 1,
            "id": f"{filepath}:{index + 1}"
        }
        documents.append(Document(page_content=text, metadata=doc_metadata))
    
    print(f"Successfully processed {len(documents)} transactions")
    return documents

def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = [chunk for chunk in chunks if chunk.metadata["id"] not in existing_ids]

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("✅ No new documents to add")

def clear_database():
    if os.path.exists(CHROMA_PATH):
        
        
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()