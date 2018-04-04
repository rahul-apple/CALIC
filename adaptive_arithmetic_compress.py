import sys
import arithmeticcoding
python3 = sys.version_info.major >= 3


# Command line main application function.
def main(args):
	# Handle command line arguments
	if len(args) != 2:
		sys.exit("Usage: python adaptive_arithmetic_compress.py InputFile OutputFile")
	inputfile  = args[0]
	outputfile = args[1]

	# Perform file compression
	with open(inputfile, "rb") as inp:
		bitout = arithmeticcoding.BitOutputStream(open(outputfile, "wb"))
		try:
			compress(inp, bitout)
		finally:
			bitout.close()


def compress(inp, bitout):
	initfreqs = arithmeticcoding.FlatFrequencyTable(257)
	freqs = arithmeticcoding.SimpleFrequencyTable(initfreqs)
	enc = arithmeticcoding.ArithmeticEncoder(bitout)
	while True:
		# Read and encode one byte
		symbol = inp.read(1)
		if len(symbol) == 0:
			break
		symbol = symbol[0] if python3 else ord(symbol)
		enc.write(freqs, symbol)
		freqs.increment(symbol)
	enc.write(freqs, 256)  # EOF
	enc.finish()  # Flush remaining code bits


# Main launcher
if __name__ == "__main__":
	main(sys.argv[1 : ])
