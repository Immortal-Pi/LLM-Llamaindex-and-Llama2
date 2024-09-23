import argparse
import os
import shutil
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import  Document
# get embeddings
from langchain.vectorstores.chroma import  Chroma

CHROMA_PATH=''
DATA_PATH=''