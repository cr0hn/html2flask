import re
import argparse
from typing import Set

from .config import RunningConfig

REGEX = {
    "href": re.compile(r'''href=[\'"]?([^\'" >]+)'''),
    "src": re.compile(r'''src=[\'"]?([^\'" >]+)'''),

}

def jinjarize(html: str, links: Set[str], config: RunningConfig) -> str:

    for link in links:
        if link.endswith("css"):
            base_path = config.base_path_css or ""

        elif any(link.endswith(x) for x in ("jpg", "jpeg", "png", "gif", "svg", "webp", "ico", "bmp", "tiff", "tif")):
            base_path = config.base_path_images or ""

        elif link.endswith("js"):
            base_path = config.base_path_javascript or ""

        else:
            base_path = ""

        html = html.replace(link, f"{{{{ url_for('static', filename='{base_path}{link}') }}}}")

    return html


def convert(config: RunningConfig = None) -> str:
    with open(config.html_file, "r") as f:
        html = f.read()

    # ----------------------------------------------------------------------------------------------------------------------
    # Find all hrefs
    # ----------------------------------------------------------------------------------------------------------------------
    for tag, regex in REGEX.items():

        links = set()

        for href in regex.findall(html):
            # Contains
            if any(x in href for x in ('javascript:',)):
                continue

            # Starts
            if any(href.startswith(x) for x in ('http', '#')):
                continue

            # Ends
            if any(href.endswith(x) for x in ('html', 'htm')):
                continue

            links.add(href)

        html = jinjarize(html, links, config)

    return html

def main():
    banner = 'HTML to Jinja2 Flask Converter'

    parser = argparse.ArgumentParser(
        description=banner
    )
    parser.add_argument('--debug',
                        default=False,
                        action="store_true",
                        help="enable debug mode")
    parser.add_argument('-c', '--base-path-css',
                        default=None,
                        help="base path for css files")
    parser.add_argument('-i', '--base-path-images',
                        default=None,
                        help="base path for images")
    parser.add_argument('-j', '--base-path-javascript',
                        default=None,
                        help="base path for javascript files")
    parser.add_argument('html_file',
                        help="HTML file to convert")
    args = parser.parse_args()

    config = RunningConfig.from_cli(args)

    print(convert(config))

if __name__ == '__main__':
    main()
