import sys
from transformers import AutoTokenizer

from utils import load_file, identify_cve, repair_code

def main(file_path):


if __name__ == "__main__":
	if len(sys.argv) > 1:
	    file_path = sys.argv[1]
	    main(file_path)
	else:
	    print("Usage: python main.py <file_path>")