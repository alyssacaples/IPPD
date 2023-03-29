import xml.etree.ElementTree as ET


xml_parse_path = ".\XML_Output\Augmented-5-OFF_OutputXMLs\picture101.xml"

tree = ET.parse(xml_parse_path)
root = tree.getroot()
#filename = root.SubElement(root, "filename")

print(root.tag)

filename = root.find("filename")
print(filename.text)

filename.text = "soup"
print(filename.text)

#filename.set('text', "cool_cucumber")

tree.write(xml_parse_path)


# ET.SubElement(root, "folder").set = "train"
# ET.SubElement(root, "filename").set = "6"
# ET.SubElement(root, "path").set = "/content/drive/MyDrive/Training_Session/train"
