import sys
sys.path.insert(0, './bls')


from bls.bls_sig_g1 import sign
from bls.consts import *




if __name__ == "__main__":
    sign("asb", "", ciphersuite="ad")