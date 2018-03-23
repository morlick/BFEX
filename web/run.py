from bfex.app import create_app
import os

if __name__ == "__main__":
    # Config setup	
    if 'BFEX_CONFIG' not in os.environ:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.json')
        os.environ['BFEX_CONFIG'] = path
    app = create_app()
    app.run(host="localhost", port=8901)
