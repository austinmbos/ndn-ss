

import time
import json
import base64

from CryptoUtil import *


# generate the sym keys for users

austin_sym_key = create_sym_key()
encoded_sym_key = base64.b64encode(austin_sym_key).decode('ascii')

priv_key = gen_priv_key()
pub_key = get_pub_key(priv_key)
priv_key = get_priv_bytes(priv_key)
pub_key = get_pub_bytes(pub_key)
priv_key = base64.b64encode(priv_key).decode('ascii')
pub_key = base64.b64encode(pub_key).decode('ascii')



users = {'austin': 
            {
                'sym_key':encoded_sym_key,
                'pub_key':pub_key,
                'priv_key':priv_key
            }
        }



with open("system-info.json","w") as f:
    json.dump(users,f)

