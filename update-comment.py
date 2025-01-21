import xml.etree.ElementTree as ET
import argparse

def update_comment(input_file, output_file, info_text):
    # Load and parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    for preset in root.findall("preset"):
        attributes = preset.find("attributes")
        if attributes is not None:
            comment_attr = attributes.find("./attribute[@name='Comment']")
            if comment_attr is not None:
                # If Comment attribute exists, append the new info_text
                existing_text = comment_attr.text if comment_attr.text else ""
                if existing_text.strip():
                    comment_attr.text = f"{existing_text}\n\n{info_text}"
                else:
                    comment_attr.text = info_text
            else:
                # If Comment attribute does not exist, create it
                new_comment = ET.SubElement(attributes, "attribute")
                new_comment.set("name", "Comment")
                new_comment.text = info_text

    # Write the updated XML to the output file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update XML file with specific rules.")
    parser.add_argument("input_file", help="Path to the input XML file.")
    parser.add_argument("output_file", help="Path to save the updated XML file.")
    parser.add_argument("info_text", help="Text to add to preset comment")

    args = parser.parse_args()
    update_comment(args.input_file, args.output_file, args.info_text)
