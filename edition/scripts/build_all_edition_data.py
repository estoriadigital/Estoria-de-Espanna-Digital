from pathlib import Path

# here add all the data generation scripts

edition_dir = Path(__file__).resolve().parent.parent

link = Path(edition_dir / 'static' / 'data' / 'transcription')
target = Path(edition_dir / 'transcription')
try:
    link.symlink_to(target)
except FileExistsError:
    pass

link = Path(edition_dir / 'static' / 'data' / 'reader')
target = Path(edition_dir / 'reader')
try:
    link.symlink_to(target)
except FileExistsError:
    pass

link = Path(edition_dir / 'static' / 'data' / 'critical')
target = Path(edition_dir / 'critical')
try:
    link.symlink_to(target)
except FileExistsError:
    pass
