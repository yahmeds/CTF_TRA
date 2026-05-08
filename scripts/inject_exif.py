"""
Inject GPS EXIF into a JPEG for the level-4 challenge.

Usage:
    pip install pillow piexif
    python scripts/inject_exif.py static/photo.jpg

The flag is NOT written in any text field. The player must extract the GPS
coordinates and reverse-geocode them to find the location.
"""
import sys
from pathlib import Path

from PIL import Image
import piexif


# Laiterie Soummam ZAC, Akbou 06001, Algeria
LAT = 36.48105414081353
LON = 4.573131550138424

ARTIST = b"K."
SOFTWARE = b"darktable"


def deg_to_dms_rational(deg):
    deg = abs(deg)
    d = int(deg)
    m_full = (deg - d) * 60
    m = int(m_full)
    s = round((m_full - m) * 60 * 10000)
    return ((d, 1), (m, 1), (s, 10000))


def main(path_str):
    path = Path(path_str)
    if not path.exists():
        sys.exit(f"file not found: {path}")

    img = Image.open(path)
    if img.format != "JPEG":
        sys.exit(f"expected a JPEG, got {img.format}")

    zeroth_ifd = {
        piexif.ImageIFD.Artist: ARTIST,
        piexif.ImageIFD.Software: SOFTWARE,
    }
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: b"N",
        piexif.GPSIFD.GPSLatitude: deg_to_dms_rational(LAT),
        piexif.GPSIFD.GPSLongitudeRef: b"E",
        piexif.GPSIFD.GPSLongitude: deg_to_dms_rational(LON),
    }
    exif_dict = {"0th": zeroth_ifd, "Exif": {}, "GPS": gps_ifd, "1st": {}, "thumbnail": None}
    exif_bytes = piexif.dump(exif_dict)

    img.save(path, "jpeg", exif=exif_bytes, quality=90)
    print(f"injected GPS ({LAT}, {LON}) into {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python scripts/inject_exif.py <path-to-jpeg>")
    main(sys.argv[1])
