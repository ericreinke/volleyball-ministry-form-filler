import FormFiller
from SelfClient import SelfClient, client_init_and_start
import argparse

#Solve ssl issue:
# pip install --upgrade certifi
# export SSL_CERT_FILE=$(python -m certifi)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Google Form Autofill and Submit")
    # parser.add_argument("url", help="Google Form URL")
    # args = parser.parse_args()
    
    # FormFiller.complete_form(args.url)
    client_init_and_start()
    
    
