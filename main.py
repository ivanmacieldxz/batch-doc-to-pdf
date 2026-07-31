import sys
from cli import parse_args, run_cli

def main():
    args = parse_args()
    
    if args.input_dir:
        # User provided an input directory, run CLI mode
        run_cli(args)
    else:
        # No input directory provided, launch GUI mode
        try:
            # We import gui here so that if the user only wants CLI,
            # they don't strictly need GUI dependencies if we add them later.
            from gui import run_gui
            run_gui()
        except ImportError:
            print("GUI module not found or dependencies missing.")
            print("For now, please use the CLI mode by providing an input directory:")
            print("  python main.py /path/to/documents")
            sys.exit(1)

if __name__ == "__main__":
    main()
