#!/usr/bin/env python3

import connexion
import encoder
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'ECE 461 - Fall 2021 - Project 2'},
                pythonic_params=True)

    app.run(port=8080)


if __name__ == '__main__':
    main()
