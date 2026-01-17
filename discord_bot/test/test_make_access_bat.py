from src.make_access_bat import BatMaker


def test_make_bat():
    maker = BatMaker("test", 80)

    assert (
        "cloudflared access tcp --hostname test --url localhost:80"
        == maker.make_command()
    )


def test_make_file():
    maker = BatMaker("test", 80)
    maker.make_file()
    from pathlib import Path

    file_path = Path("access.bat")

    assert file_path.exists()
