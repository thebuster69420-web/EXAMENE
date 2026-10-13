import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

TIMEOUT = 5  # secunde de așteptare pentru fiecare cerere GET


def short_error(e):
    """Transformă o excepție din requests într-un mesaj scurt, ușor de citit."""
    # Timeout se verifică primul: ConnectTimeout este și Timeout, și ConnectionError
    if isinstance(e, requests.Timeout):
        return f"timeout: site-ul nu a raspuns in {TIMEOUT} secunde"
    if isinstance(e, requests.ConnectionError):
        return "eroare de conexiune: site inexistent sau inaccesibil"
    return "eroare la cerere: " + type(e).__name__


# ---------------- Partea 1 ----------------

def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    host = host.rstrip("/")          # "example.com/" devine "example.com"
    if not path.startswith("/"):
        path = "/" + path
    return "https://" + host + path


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


# ---------------- Partea 2 ----------------

def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as e:
        print("Eroare:", short_error(e))
        return

    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))


# ---------------- Partea 3 ----------------

def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as e:
        return {"status": None, "error": short_error(e)}

    # Content-Type vine de obicei cu charset la final ("text/html; charset=UTF-8"),
    # păstrăm doar tipul propriu-zis
    content_type_header = response.headers.get("Content-Type")
    if content_type_header:
        content_type = content_type_header.split(";")[0].strip()
    else:
        content_type = "unknown"

    return {
        "status": response.status_code,
        "content_type": content_type,
        "length": len(response.content),
        "server": response.headers.get("Server", "unknown"),
    }


# ---------------- Partea 4 ----------------

def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    # 1. verificăm fiecare adresă și păstrăm rezultatele într-o listă
    results = []
    for url in SITES:
        result = check_site(url)
        result["url"] = url
        results.append(result)

    # 2. păstrăm doar site-urile cu status 200
    working = [r for r in results if r["status"] == 200]

    # 3. sortăm după lungime, cel mai mare primul
    working.sort(key=lambda r: r["length"], reverse=True)

    for r in working:
        print(f"{r['url']} -> {r['status']}, {r['length']} octeti")

    # 4. rezumatul
    failed = len(results) - len(working)
    print(f"Reusite: {len(working)} | Esuate: {failed}")


# ---------------- Partea 5 ----------------

def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as e:
        return {"status": None, "error": short_error(e)}

    # numele antetelor primite, cu litere mici, ca să nu conteze majusculele
    received_lower = {name.lower() for name in response.headers.keys()}

    # parcurgem SECURITY_HEADERS în ordine, deci listele păstrează ordinea ei
    present = []
    missing = []
    for header in SECURITY_HEADERS:
        if header.lower() in received_lower:
            present.append(header)
        else:
            missing.append(header)

    score = round(len(present) / len(SECURITY_HEADERS) * 100)

    return {"present": present, "missing": missing, "score": score}


# ---------------- Partea 6 ----------------

def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    last_status = None   # ultimul status primit de la server
    last_error = None    # ultima eroare de conexiune / timeout
    attempts_made = 0    # câte cereri am trimis cu adevărat

    while attempts_made < attempts:
        attempts_made += 1
        try:
            response = requests.get(url, timeout=TIMEOUT)
        except requests.RequestException as e:
            last_error = short_error(e)
            continue  # conexiune picată sau timeout: mai încercăm

        last_status = response.status_code
        if last_status < 500:
            break  # 2xx, 3xx sau 4xx: nu are rost să mai încercăm

    result = {"status": last_status}
    # cheia "error" apare doar dacă nicio încercare n-a primit răspuns de la server
    if last_status is None and last_error is not None:
        result["error"] = last_error
    result["attempts"] = attempts_made
    return result
