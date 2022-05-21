from fire import Fire


class Command:
    min = min
    max = max


if __name__ == "__main__":
    # Ref: https://qiita.com/SaitoTsutomu/items/a5eb827737c9d59af2af
    Fire(Command)
