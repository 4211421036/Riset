import random

# Buat PRNG data
data = [random.randint(0, 1) for _ in range(1000000)]  # 1.000.000 bit

# Simpan ke file
with open(r"c:/Users/asus/public/unnes-py/sts-2.1.2/prng_data.bin", "wb") as f:
    for bit in data:
        f.write(bit.to_bytes(1, 'big'))
