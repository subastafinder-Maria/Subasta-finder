"""Actualiza el catálogo solo con registros cuya correspondencia de campos se ha validado.
Sin mapeo confirmado, conserva el catálogo y nunca publica registros especulativos.
"""
import csv, io, json, os, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DEST=ROOT/'data'/'listings.json'
URL=os.getenv('SUBASTAS_CSV_URL','https://catalogodatos.justicia.es/csv/Subastas_Judiciales.csv')
# Establecer estas variables SOLO después de inspeccionar los encabezados reales del CSV.
FIELDS=['TITLE_FIELD','CITY_FIELD','PROVINCE_FIELD','URL_FIELD','PRICE_FIELD','TYPE_FIELD']

def main():
    with urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'SubastaFinderPersonal/1.0'}),timeout=25) as resp:
        raw=resp.read(20_000_000).decode('utf-8-sig')
    dialect=csv.Sniffer().sniff(raw[:10000],delimiters=',;\t')
    reader=csv.DictReader(io.StringIO(raw),dialect=dialect)
    columns=reader.fieldnames or []
    print('Columnas de la fuente:',columns)
    mapping={k:os.getenv(k,'').strip() for k in FIELDS}
    if not all(mapping.values()) or any(v not in columns for v in mapping.values()):
        print('Importación detenida: falta validar la correspondencia exacta de columnas. Catálogo sin cambios.')
        return
    listings=[]
    for row in reader:
        title=row[mapping['TITLE_FIELD']].strip()
        city=row[mapping['CITY_FIELD']].strip()
        province=row[mapping['PROVINCE_FIELD']].strip()
        url=row[mapping['URL_FIELD']].strip()
        if not title or not city or not url.startswith('https://'):
            continue
        # Conservar solo registros cuyo origen se conoce. No inferir estado abierto ni geolocalización.
        rawprice=row[mapping['PRICE_FIELD']].strip().replace(' ','').replace('€','')
        try: price=float(rawprice.replace('.','').replace(',','.')) if ',' in rawprice else float(rawprice)
        except ValueError: price=None
        listings.append({'title':title,'city':city,'province':province,'url':url,'price':price,'type':row[mapping['TYPE_FIELD']].strip() or 'Otro','source':'Subasta judicial','status':'Vigencia sin verificar','note':'Importado de fuente histórica; verificar expediente','lat':None,'lng':None})
    # Un histórico sin estado de apertura no se publica como catálogo de oportunidades activas.
    print(f'{len(listings)} filas mapeadas; publicación automática desactivada hasta validar vigencia.')

if __name__=='__main__':
    try: main()
    except Exception as exc: print('Actualización no completada:',repr(exc))
