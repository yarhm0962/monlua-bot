import unittest
from fulcrum_deobf import decrypt, MOD
from direct import recover, affine

class DecryptTests(unittest.TestCase):
    def test_independent_encoded_roundtrips(self):
        # Inverse equations independently construct encrypted samples.
        plaintext=bytes(range(256));key=[117,13,171,53,29];start=732523
        inv=pow(key[2],-1,256)
        for alg in 'OQUV':
            state=start;encoded=[]
            for b in plaintext:
                if alg=='O':state=(state*key[0]+key[1])%MOD
                elif alg=='Q':state=(state*key[0]+key[1]*key[0])%MOD
                elif alg=='U':state=(state*key[0]-key[1])%MOD
                else:state=(state*key[0]-key[1]*key[0])%MOD
                f=state+(state//256)*key[3]+(state//65536)*key[4]
                if alg=='O':v=b*inv+f
                elif alg=='Q':v=(b+f)*inv
                elif alg=='U':v=b*inv-f
                else:v=(b-f)*inv
                encoded.append(v%256)
            self.assertEqual(decrypt(alg,encoded,key,start),plaintext)
    def test_real_literal_and_shuffle_guard(self):
        text="aN=((dr+12934798)-(dr+863399));cc[1]={((dr+3723505)-(dr+2120)),((dr+2877762)-(dr+376213)),77,127,139};bW[1]={185,17,51,154};x=bV(bW[1],cc[1],aN);"
        found=recover(text)
        self.assertEqual(len(found),1)
        self.assertEqual(found[0]['utf8'],'type')
        self.assertEqual(recover(text.replace('x=bV','bW[1],x=x,bW[1];x=bV')),[])
        self.assertEqual(affine('(dr+5)-(dr+3)'),2)
        with self.assertRaises(ValueError):affine('__import__("os")')

    def test_validation(self):
        for bad in ([-1],[256],[True]):
            with self.assertRaises(ValueError):decrypt('O',bad,[1,2,3,4,5],1)
        with self.assertRaises(ValueError):decrypt('X',[],[1,2,3,4,5],1)
        with self.assertRaises(ValueError):decrypt('O',[],[1,2],1)
if __name__=='__main__':unittest.main()
