import urllib2
import sys

class PaddingOracle(object):
	BLOCK_SIZE = 16
	CRYPTOTEXT_TEXT = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
	CRYPTOTEXT_BYTE = []
	TARGET = 'http://crypto-class.appspot.com/po?er='
	DECRYPTED = ""
	BLOCKS_COUNT = 0

	def __init__(self):
		for i in range(0, len(self.CRYPTOTEXT_TEXT), 2):
			val = int(self.CRYPTOTEXT_TEXT[i:i+2], 16)
			self.CRYPTOTEXT_BYTE.append(val)
		self.BLOCKS_COUNT = len(self.CRYPTOTEXT_BYTE)/self.BLOCK_SIZE

	def run(self):
		for block in range(0, self.BLOCKS_COUNT-1):
			cb = self.CRYPTOTEXT_BYTE[0 : len(self.CRYPTOTEXT_BYTE) - block * self.BLOCK_SIZE]
			for i in range(0, self.BLOCK_SIZE):
				cm = cb[0:len(cb)]
				found = 0
				pos = len(cb) - 1 - self.BLOCK_SIZE - i
				#guess
				for b in range(0, 256):
					#pad all bytes from current to the end of the block
					for k in range(0, i+1):
						cm[pos+k] = cb[pos+k] ^ (i+1)
					cm[pos] = cm[pos] ^ b
					status = self.query(self.byteArrayToHexString(cm))
					print "%d:%d:%d:%d > %d = %s" % (block, i, pos, b, status, self.byteArrayToHexString(cm))
					if status == 404:
						found = b
						break;
					if status == 200:
						found = b
				cb[pos] = cb[pos] ^ found
				self.DECRYPTED = str(unichr(found)) + self.DECRYPTED
				print "found>>%s -> %s" % (found, self.DECRYPTED)

	def query(self, q):
		target = self.TARGET + urllib2.quote(q)	# Create query URL
		req = urllib2.Request(target)		 # Send HTTP request to server
		try:
			f = urllib2.urlopen(req)		  # Wait for response
		except urllib2.HTTPError, e:		  
			return e.code
		return 200

	def byteArrayToHexString(self, a):
		q = ""
		for b in a:
			q += "%0.2X" % b
		return q;
			
if __name__ == "__main__":
	po = PaddingOracle()
	po.run()
	#po.xor(CRYPTOTEXT, GUESS)
	#po.query(CRYPTOTEXT)	   # Issue HTTP query with the given argument
	#print hex(int("12", 16) ^ int("0", 16))