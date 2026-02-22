address = "3c1c26d3453b7797ebcf302d358ead8a630eba5d"

vanity = "00" * 32
signature = "00" * 65

extradata = "0x" + vanity + address + signature

print(extradata)
print("Length:", len(extradata))