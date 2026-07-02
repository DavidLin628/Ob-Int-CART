import sys
import os
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def run_notebook(path):
    notebook_path = Path(path)
    output_path = notebook_path.with_name(notebook_path.stem + "_executed.ipynb")

    nb = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=900,
        kernel_name=os.environ.get("KERNEL_NAME", "python3"),
        resources={"metadata": {"path": str(Path.cwd())}},
        allow_errors=False,
    )
    client.execute()
    nbformat.write(nb, output_path)
    print(f"Executed notebook written to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python scripts/run_notebook.py "Ob-Int CART.ipynb"')
    run_notebook(sys.argv[1])
