import logfire
from unstructured.partition.auto import partition

def parse_office(file_path: str):
    """
    Parse Office documenats ( .docx, .pptx) using the unstructured library.
    Unlike PDFs, these formats are structured and lightweight, so they are processed locally
    """

    with logfire.span("Office Document Parsing", filename=file_path):
        try:
            # Unstructured Automatically detects if it's docx or pptx
            elements = partition(filename=file_path)
            full_text = "\n".join([str(el) for el in elements])

            if not full_text.strip():
                logfire.warning(f"Unstructured returned empty text for {file_path}")
            else:
                logfire.info(f"Successfully Parsed {len(full_text)} characters")

            return full_text

        except Exception as e:
            logfire.error(f"Office parse failed : {e}")
            raise e