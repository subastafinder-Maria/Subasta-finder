
import csv
import io
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
URL = os.getenv(
    "SUBASTAS_CSV_URL",
    "https://catalogodatos.justicia.es/csv/Subastas_Judiciales.csv"
)
DEST = ROOT / "data" / "auction_summary.json"

def main():
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "SubastaFinderPersonal/1.0"}
    )
    with urllib.request.urlopen(request, timeout=40) as response:
        raw = response.read(30_000_000).decode("utf-8-sig")

    dialect = csv.Sniffer().sniff(
        raw[:10000], delimiters=",;\t"
    )
    reader = csv.DictReader(io.StringIO(raw), dialect=dialect)

    required = {"Estado", "Inmuebles"}
    columns = set(reader.fieldnames or [])

    if not required.issubset(columns):
        raise ValueError(
            f"Columnas necesarias ausentes: {required - columns}"
        )

    statuses = Counter()
    total = 0
    with_real_estate = 0

    for row in reader:
        total += 1
        statuses[(row.get("Estado") or "").strip()] += 1

        value = (row.get("Inmuebles") or "").strip()
        try:
            count = int(float(value.replace(",", ".")))
        except ValueError:
            count = 0

        if count > 0:
            with_real_estate += 1

    result = {
        "source": URL,
        "updated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "total_records": total,
        "records_with_real_estate": with_real_estate,
        "statuses": dict(sorted(statuses.items())),
        "note": (
            "Resumen estadistico. Los estados del CSV "
            "no acreditan vigencia actual. "
            "No se publican inmuebles sin ubicacion verificada."
        )
    }

    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Resumen actualizado: {total} registros")
    print(f"Registros con inmuebles: {with_real_estate}")
    print(f"Guardado en: {DEST}")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
