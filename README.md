# SubastaFinder Free

Prototipo web estático para GitHub Pages, sin servidor de pago. Incluye mapa Leaflet/OpenStreetMap, filtros de viviendas, terrenos, locales, naves y origen. No contiene inmuebles ficticios.

## Publicar gratis
1. Crea un repositorio en GitHub y sube **todos** los archivos de esta carpeta, incluido `.github/workflows/update.yml`.
2. En Settings > Pages, selecciona Deploy from a branch, rama `main`, carpeta `/ (root)`.
3. Abre la URL de Pages que te indique GitHub. Ten presente que **GitHub Pages es público incluso si el repositorio es privado**: no guardes datos personales ni información confidencial.
4. En Actions, ejecuta `Comprobar fuente de subastas` para comprobar acceso y encabezados del CSV.

## Estado real de la automatización
La tarea programada comprueba la fuente a diario, pero NO publica automáticamente anuncios porque todavía falta validar los encabezados, identificar inmuebles frente a otros bienes, determinar la vigencia real de cada expediente y sus condiciones de reutilización. El CSV judicial es histórico: no equivale a una lista de subastas abiertas. No hay integración bancaria autorizada ni geocodificación automática. El mapa solo presenta coordenadas aportadas y verificadas en `data/listings.json`.

## Datos
`data/listings.json` admite `{ "updated_at": "...", "listings": [{"title":"...","city":"...","province":"...","type":"Vivienda","source":"Subasta judicial","price":null,"status":"Vigencia sin verificar","note":"...","url":"https://...","lat":null,"lng":null}] }`. Solo introduce datos comprobados. Los anuncios bancarios requieren permiso de reutilización o integración permitida.

## Coste y privacidad
GitHub Pages, GitHub Actions (sujetos a cuotas) y OpenStreetMap (sujeto a política de uso de teselas) permiten empezar sin coste en uso moderado. No incluye login real. Si necesitas acceso estrictamente privado, GitHub Pages no es adecuado.
