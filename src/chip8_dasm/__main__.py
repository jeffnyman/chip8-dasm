import sys

if sys.version_info < (3, 7):
    sys.stderr.write("\nc8dasm requires Python 3.7 or later.\n")
    sys.stderr.write(
        "Your current version is: "
        f"{sys.version_info.major}.{sys.version_info.minor}\n"
    )
    sys.exit(1)

if __name__ == "__main__":
    print("\nCHIP-8 Disassembler\n")
