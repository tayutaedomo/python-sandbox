from fire import Fire


class Bin:
    """Convert binary number from/to decimal number."""

    def from_dec(self, n):
        """Convert binary number from decimal number."""
        return bin(n)

    def to_dec(self, n):
        """Convert binary number to decimal number."""
        return int(str(n), 2)


class Oct:
    """Convert octal number from/to decimal number."""

    def from_dec(self, n):
        """Convert octal number from decimal number."""
        return oct(n)

    def to_dec(self, n):
        """Convert octal number to decimal number."""
        return int(str(n), 8)


class Command:
    bin = Bin
    oct = Oct


if __name__ == "__main__":
    # Ref: https://qiita.com/SaitoTsutomu/items/a5eb827737c9d59af2af
    Fire(Command)
