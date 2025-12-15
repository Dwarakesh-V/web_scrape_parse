import requests
from bs4 import BeautifulSoup
from url_parse import canonical_url_generic

def scrape_with_sections(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    # Fetch page
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove noise
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Any block you want treated as content
    block_tags = {"p", "li", "blockquote", "pre"}

    # Headings define section boundaries
    heading_levels = {"h1","h2","h3","h4","h5","h6"}

    sections = {}
    current_section = "ROOT"   # before the first heading
    sections[current_section] = []

    # Walk the document in-order
    for el in soup.descendants:
        if not hasattr(el, "name"):
            continue

        # Heading → new section
        if el.name in heading_levels:
            title = el.get_text(" ", strip=True)
            title = " ".join(title.split())
            current_section = title if title else "UNTITLED_SECTION"
            if current_section not in sections:
                sections[current_section] = []
            continue

        # Paragraph / list item / block
        if el.name in block_tags:
            text = el.get_text(" ", strip=True)
            if text:
                text = " ".join(text.split())
                sections[current_section].append(text)

    return sections


if __name__ == "__main__":
    url = "https://www.amazon.in/Hundred-Badminton-Marking-Lightweight-X-Cushion/dp/B0FM83V638/ref=sr_1_2_sspa?crid=G7W68H7TRUTN&dib=eyJ2IjoiMSJ9.SS1edm9RN-WISllZWvIgZaJqsH4RMYtG6uEkRBhsXH9N_pQeY9y867kK38fvHbRoHHhpG36ucKJWJ7BYX3HvRYkeeLcMajIpyHooOy8hPNjPvH3EBkyH3GDTmWz8nlBIK7h6kHxYRYWDzE0Vr27vwyAitwvpW979mqUPx8Kn4BQhPsvlfrY9ph8gEnh8E2_68_FDc4H7krdrcI3WArB0NTOkPaxXXI0Lv6a0Jbs_9CuZX-ypMSJ0eb_TeR1alIZChtIUpXjEzAr9g3LmDWsmUHShbi7z4sYLs7csFwja5Yc.xN4ebJa3bHAHjTC1h_mi0DepjQkhwolZS6S9M9Axc04&dib_tag=se&keywords=badminton%2Bshoes&qid=1765182418&sprefix=badminton%2Bshoe%2Caps%2C276&sr=8-2-spons&aref=IN8eisUA0p&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"
    url = canonical_url_generic(url)

    try:
        sections = scrape_with_sections(url)
    except Exception as e:
        print(f"Failed to scrape from url because of error: {e}")

    # Dump into a clean text file
    with open("sections_site.txt", "w", encoding="utf-8") as f:
        for title, blocks in sections.items():
            f.write(title + "\n")
            for b in blocks:
                f.write(b + "\n")
            f.write("\n")
