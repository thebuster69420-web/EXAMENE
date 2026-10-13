from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check
from checker import SITES

# Adresele se iau doar din lista SITES (nu sunt scrise direct în cod)
OK_SITE = SITES[0]               # https://example.com
STATUS_200 = SITES[3]            # răspunde mereu 200
STATUS_404 = SITES[6]            # răspunde mereu 404
STATUS_500 = SITES[7]            # răspunde mereu 500
MISSING_SITE = SITES[9]          # domeniu inexistent
TWO_HEADERS = SITES[10]          # X-Frame-Options și X-Content-Type-Options
LOWERCASE_HEADER = SITES[11]     # x-frame-options scris cu litere mici
RANDOM_200_500 = SITES[12]       # răspunde aleatoriu 200 sau 500

# Partea 1: apeluri pentru build_url și is_https
print("Partea 1, build_url:", build_url("example.com", "login"))
print("Partea 1, build_url:", build_url("example.com", "/login"))
print("Partea 1, is_https:", is_https(OK_SITE))
print("Partea 1, is_https:", is_https(MISSING_SITE))   # adresă http:// -> False
print()

# Partea 2: apeluri pentru show_response
print("Partea 2, show_response (site ok):")
show_response(OK_SITE)
print("Partea 2, show_response (site inexistent):")
show_response(MISSING_SITE)
print()

# Partea 3: apeluri pentru check_site, pe fiecare adresă din SITES
for url in SITES:
    print("Partea 3, check_site:", url, "->", check_site(url))
print()

# Partea 4: apelul scan_sites()
print("Partea 4, scan_sites:")
scan_sites()
print()

# Partea 5: apeluri pentru check_headers
print("Partea 5, check_headers (2 antete):", check_headers(TWO_HEADERS))
print("Partea 5, check_headers (litere mici):", check_headers(LOWERCASE_HEADER))
print("Partea 5, check_headers (fara antete):", check_headers(OK_SITE))
print("Partea 5, check_headers (site inaccesibil):", check_headers(MISSING_SITE))
# Notă: nicio adresă din SITES nu trimite toate cele 4 antete, deci scorul 100
# nu poate fi arătat aici; codul îl calculează la fel (4 din 4 -> 100).
print()

# Partea 6: apeluri pentru retry_check
print("Partea 6, retry_check (200):", retry_check(STATUS_200))
print("Partea 6, retry_check (404):", retry_check(STATUS_404))
print("Partea 6, retry_check (500):", retry_check(STATUS_500))
print("Partea 6, retry_check (500, attempts=2):", retry_check(STATUS_500, attempts=2))
print("Partea 6, retry_check (inexistent):", retry_check(MISSING_SITE))
print("Partea 6, retry_check (200 sau 500 aleatoriu):", retry_check(RANDOM_200_500))
