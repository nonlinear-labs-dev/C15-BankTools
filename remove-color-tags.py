import xml.etree.ElementTree as ET
import argparse

def replace_color(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    for preset in root.findall("preset"):
        attributes = preset.find("attributes")
        if attributes is not None:
            color_attr = attributes.find("./attribute[@name='color']")
            if color_attr is not None:
                color_attr.text = "none"

    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update XML file with specific rules.")
    parser.add_argument("input_file", help="Path to the input XML file.")
    parser.add_argument("output_file", help="Path to save the updated XML file.")

    args = parser.parse_args()
    replace_color(args.input_file, args.output_file)