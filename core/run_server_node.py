import json
import sys
from nodehelpers.protocol_const import DEFAULT_CRED_PATH


def get_credentials(cred_path):
    with open(cred_path) as f:
        return json.load(f)


if __name__ == "__main__":
    try:
        
        cred = get_credentials(DEFAULT_CRED_PATH)

        if cred["router"]:
            from routingnode import router
            router.run(cred["id"])
        else:
            from computenode import computer
            computer.run(cred["eth_cred"]["address"], cred["public_ip"])

    except Exception as e:
        raise e
    