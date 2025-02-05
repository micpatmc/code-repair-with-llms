from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)

if __name__ == "__main__":
    file_path = "C:\\Users\\Gavin Cruz\\Documents\\SD1\\finalspace\\code-repair-with-llms\\ObjectArrayCodec.java"
    java_code = None
    with open(file_path, "r") as file:
        java_code = file.read()

    java_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.JAVA, chunk_size=500, chunk_overlap=50
    )

    java_docs = java_splitter.create_documents([java_code])
    with open("java_split.txt", "w") as file:
        for doc in java_docs:
            file.write(doc.page_content)
            file.write("\n-------------------------------------------------------\n")

    