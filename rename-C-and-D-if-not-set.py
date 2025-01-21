import xml.etree.ElementTree as ET
import argparse

def update_xml(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Update macros
    for parameter in root.findall(".//parameter"):
        param_id = parameter.get("id")
        given_name = parameter.find("givenName")

        if param_id == "Global-246":
            if given_name is None or not (given_name.text or "").strip():
                if given_name is None:
                    given_name = ET.SubElement(parameter, "givenName")
                given_name.text = "Sust. Pedal"

        elif param_id == "Global-245":
            if given_name is None:
                given_name = ET.SubElement(parameter, "givenName")
            given_name.text = "Pitchbend"
    
    # Write the changes to the output file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update XML file with specific rules.")
    parser.add_argument("input_file", help="Path to the input XML file.")
    parser.add_argument("output_file", help="Path to save the updated XML file.")

    args = parser.parse_args()
    update_xml(args.input_file, args.output_file)
