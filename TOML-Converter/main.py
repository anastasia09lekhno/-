import argparse
import os
from config_converter.parser import parse_toml
from config_converter.converter import convert_to_custom_language
from config_converter.errors import ConfigError

def main():
    parser = argparse.ArgumentParser(description="TOML-to-Custom-Language Converter")
    parser.add_argument("-i", "--input", required=True, help="Path to the input TOML file")
    parser.add_argument("-o", "--output", required=True, help="Path to the output file")
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    try:
        with open(args.input, "r", encoding="utf-8") as infile:
            toml_data = infile.read()

        parsed_data = parse_toml(toml_data)
        custom_config = convert_to_custom_language(parsed_data)

        with open(args.output, "w", encoding="utf-8") as outfile:
            outfile.write(custom_config)

        print(f"Conversion successful! Output saved to '{args.output}'.")

    except ConfigError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
