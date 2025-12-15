import re
from urllib.parse import urlparse, urlunparse

JUNK_PATTERNS = re.compile(
    r"^(ref=|utm_|sp_|sr=|qid=|crid=|session|tracking)",
    re.IGNORECASE
)

def canonical_url_generic(url: str) -> str:
    parsed = urlparse(url)
    parts = parsed.path.split("/")

    clean = []
    for p in parts:
        if not p:
            continue
        if JUNK_PATTERNS.match(p):
            break
        clean.append(p)

    clean_path = "/" + "/".join(clean)

    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        clean_path,
        "",
        "",
        ""
    ))

if __name__ == "__main__":
    print(canonical_url_generic("https://www.amazon.in/Hundred-Badminton-Marking-Lightweight-X-Cushion/dp/B0FM83V638/ref=sr_1_2_sspa?crid=G7W68H7TRUTN&dib=eyJ2IjoiMSJ9.SS1edm9RN-WISllZWvIgZaJqsH4RMYtG6uEkRBhsXH9N_pQeY9y867kK38fvHbRoHHhpG36ucKJWJ7BYX3HvRYkeeLcMajIpyHooOy8hPNjPvH3EBkyH3GDTmWz8nlBIK7h6kHxYRYWDzE0Vr27vwyAitwvpW979mqUPx8Kn4BQhPsvlfrY9ph8gEnh8E2_68_FDc4H7krdrcI3WArB0NTOkPaxXXI0Lv6a0Jbs_9CuZX-ypMSJ0eb_TeR1alIZChtIUpXjEzAr9g3LmDWsmUHShbi7z4sYLs7csFwja5Yc.xN4ebJa3bHAHjTC1h_mi0DepjQkhwolZS6S9M9Axc04&dib_tag=se&keywords=badminton%2Bshoes&qid=1765182418&sprefix=badminton%2Bshoe%2Caps%2C276&sr=8-2-spons&aref=IN8eisUA0p&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"))