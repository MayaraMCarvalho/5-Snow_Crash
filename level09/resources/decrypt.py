import sys

if (len(sys.argv) != 2):
	print("Usage: python decrypt.py <file>")
	sys.exit(1)

name_file = sys.argv[1]

try:
	with open(name_file, "rb") as f:
		data = f.read()
except Exception as e:
	print(f"Error reading file: {e}")
	sys.exit(1)

result = ""

for i in range(len(data)):
	val = ord(data[i]) if type(data[i]) is str else data[i]

	if val == 10 and i == len(data) - 1:
		break

	result += chr((val - i) % 256)

print(f"Decrypted result: {result}")
