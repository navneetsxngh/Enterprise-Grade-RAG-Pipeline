from bs4 import BeautifulSoup
import logfire

def parse_html(file_path: str):
    """
    Parse HTML content using BeautifulSoup.
    Clean scripts, styles and extracts readable text for RAG.
    """
    with logfire.span("HTML Parsing", filename=file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            soup = BeautifulSoup(content, "html.parser")

            # 1. Remove Junk (Scripts, Styles and Metadata)
            for script in soup(["scripts", "style", "meta", "noscript"]):
                script.decompose()

            # 2. Extract Text
            text = soup.get_text(separator="\n")

            # 3. Clean Whitespaces
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            text_clean = '\n'.join(chunk for chunk in chunks if chunk)

            return text_clean

        except Exception as e:
            logfire.error(f"HTML Parse failed : {e}")
            raise e