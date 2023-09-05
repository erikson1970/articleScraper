from clipboardClass import Clipboard
import logging, argparse, sys
import requests

config = {}


def createHTML(
    title: str = "Clipboard",
    body: str = "<p>Clipboard</p>",
    source: str = "https://www.w3schools.com/html/html_examples.asp",
) -> str:
    """Create an HTML file from the title, body, and source."""
    crlf = "\n"
    html = f"""
    <html>
        <head>
            <title>{title}</title>
        </head>
        <body>
            <h1>{'<BR>'.join(title.split(crlf))}</h1>
            <h3>Source: <a href='{source}' target='_blank'>Link Ref</a></h3>
            {body}
        </body>
    </html>
    """
    return html


log = logging.getLogger("__name__")


def create_parser(description, interface_factory, conf):
    """Create the command line parser."""
    p = argparse.ArgumentParser(description=description)

    # Article Source
    p.add_argument(
        "-s",
        "--source",
        default="stdin",
        choices=["stdin", "clipboard", "web", "file"],
        help="Source of text (defaults to stdin)",
    )
    p.add_argument("-p", "--path", default=None, help="Path to file or web page")

    # Article Output
    p.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.html",
        help="Output file name (defaults to output.html)",
    )

    # article Fields
    p.add_argument(
        "-t",
        "--title",
        type=str,
        default="Clipboard",
        help="Title of the article (defaults to Clipboard)",
    )

    g = p.add_mutually_exclusive_group()
    g.add_argument("-v", "--verbose", default=0, action="count")
    g.add_argument("-q", "--quiet", default=False, action="store_true")
    return p


def _version():
    """Return the version string."""
    return "0.1"


def _config_log(args):
    """Configure the logging module."""
    if args.verbose == 0:
        level, fmt = "INFO", "%(message)s"
    elif args.verbose == 1:
        level, fmt = "DEBUG", "%(message)s"
    elif args.verbose >= 2:
        level, fmt = (
            "DEBUG",
            "%(asctime)s %(levelname)-10s "
            "%(message)-100s "
            "%(filename)s:%(lineno)d",
        )
    if args.quiet:
        level, fmt = "WARNING", "%(message)s"
    logging.basicConfig(level=level, format=fmt)


def _main():
    fmt = "Simple Article Creator v{0:s}: "
    description = fmt.format(
        _version(),
    )
    interface = None

    def interface_factory():
        return interface

    p = create_parser(description, interface_factory, config)

    args = p.parse_args()
    _config_log(args)

    # get the data from the input
    if args.source == "stdin":
        input_str = sys.stdin.read()
    elif args.source == "clipboard":
        cl = Clipboard()
        input_str = cl.get_clipboard_data()
    elif args.source == "web":
        input_str = requests.get(args.path).text
    elif args.source == "file":
        with open(args.path, "r") as f:
            input_str = f.read()
    
    # create the html
    html = createHTML(title=args.title, body=input_str, source=args.path)

    # output the html

    

if __name__ == "__main__":
    _main()
