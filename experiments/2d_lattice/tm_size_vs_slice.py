def tm_size_vs_slice(Ly_max: int = 6):
    for Ly in range(1, Ly_max + 1):
        size = 8 ** Ly
        print(f"Ly={Ly} -> transfer matrix slice dimension = {size}")


if __name__ == "__main__":
    tm_size_vs_slice(6)
