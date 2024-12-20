from pathlib import Path

def generate_docs():
    docs_path = Path("docs/api.md")
    with docs_path.open("w", encoding="utf-8") as f:
        f.write("# API Documentation\n\n")
        f.write("This is an automatically generated API documentation.\n\n")
        # Add your logic here to dynamically fetch API details
        f.write("## Example Endpoint\n")
        f.write("- GET `/api/example/`\n")

if __name__ == "__main__":
    generate_docs()
