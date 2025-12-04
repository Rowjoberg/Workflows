import os

from natsort import natsorted  # Install with: pip install natsort

# Base directory for your local PyPI-like repository
base_dir = r"C:/dev/PythonPI"


def normalize_name(name):
    """Normalize package name according to PEP 503"""
    return name.lower().replace("_", "-").replace(".", "-")


def generate_package_index(
    actual_package_path, index_path, package_name, original_name
):
    """Generate index.html for a specific package"""
    # List files from the actual package directory, not the simple/ directory
    files = [
        f
        for f in os.listdir(actual_package_path)
        if os.path.isfile(os.path.join(actual_package_path, f))
        and f.endswith((".whl", ".tar.gz", ".zip"))
    ]
    files = natsorted(files)

    html_content = f"<!DOCTYPE html>\n<html><head><title>Links for {package_name}</title></head><body>\n"
    html_content += f"<h1>Links for {package_name}</h1>\n"

    for f in files:
        # Link should be relative to the package index: ../../original_name/filename
        html_content += f'<a href="../../{original_name}/{f}">{f}</a><br/>\n'

    html_content += "</body></html>"

    # Write to the simple/ directory index location
    with open(os.path.join(index_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)


def generate_root_index():
    """Generate the root simple index"""
    # Create simple directory if it doesn't exist
    simple_dir = os.path.join(base_dir, "simple")
    os.makedirs(simple_dir, exist_ok=True)

    root_html = (
        "<!DOCTYPE html>\n<html><head><title>Simple Index</title></head><body>\n"
    )
    root_html += "<h1>Simple Index</h1>\n"

    for item in os.listdir(base_dir):
        package_path = os.path.join(base_dir, item)
        if os.path.isdir(package_path) and item != "simple":
            normalized_name = normalize_name(item)

            # Create package directory in simple/
            package_simple_dir = os.path.join(simple_dir, normalized_name)
            os.makedirs(package_simple_dir, exist_ok=True)

            # Generate package index - pass both the actual package path and index path
            generate_package_index(
                package_path, package_simple_dir, normalized_name, item
            )

            # Add link to root index
            root_html += f'<a href="{normalized_name}/">{normalized_name}</a><br/>\n'

    root_html += "</body></html>"

    with open(os.path.join(simple_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(root_html)


if __name__ == "__main__":
    generate_root_index()
    print("✅ Root index.html and individual package indexes generated successfully.")
    print(f"📁 Index created at: {os.path.join(base_dir, 'simple', 'index.html')}")
