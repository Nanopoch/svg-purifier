import os
import argparse
from xml.dom import minidom
from scour import scour

# Create a list of all the standard SVG attributes that exist in the SVG specification.
valid_attributes = ['d', 'xmlns', 'style', 'x', 'y', 'rx', 'ry', 'height', 'width', 'fill', 'stroke', 'stroke-width', 'viewBox', 'transform', 'stroke-linecap',
                    'stroke-linejoin', 'stroke-miterlimit', 'stroke-dasharray', 'stroke-dashoffset', 'stroke-opacity', 'fill-opacity', 'fill-rule', 'clip-rule', 'cx', 'cy', 'r']

# Create a list of all the standard SVG elements that exist in the SVG specification.
valid_elements = ['svg', 'path', 'rect', 'g']


# Removes all non-essential attributes from an element and calls itself recursively on all children if the child is necessary to keep (i.e. is not metadata, comment, etc).
def clean_element(element: minidom.Element):
    # Explicitly remove the width and height attributes from the main SVG element
    if element.tagName == 'svg':
        if 'width' in element.attributes:
            element.removeAttribute('width')

        if 'height' in element.attributes:
            element.removeAttribute('height')

    # Remove all attributes that are not necessary
    for attr in list(element.attributes.keys()):
        if attr not in valid_attributes:
            element.removeAttribute(attr)

    # Remove all children that are not necessary
    for child in list(element.childNodes):
        if child.nodeType == minidom.Node.ELEMENT_NODE:
            if child.tagName not in valid_elements:
                element.removeChild(child)
            else:
                clean_element(child)
        else:
            element.removeChild(child)


# Entry point
if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        prog="SVG Purifier",
        description="Removes all unnecessary elements, attributes and whitespace from an SVG file.",
        add_help=True)

    parser.add_argument('-d', '--directory',
                        type=str,
                        required=True,
                        help="The directory of the SVG files to be purified.")

    parser.add_argument('-o', '--output',
                        type=str,
                        default="purified",
                        help="Output directory for purified SVG files ([Default] 'purified' folder in the same directory as the SVG directory).")

    args = parser.parse_args()

    all_directories = [x[0] for x in os.walk(args.directory)]

    for directory in all_directories:
        all_files = []

        for (dirpath, dirnames, filenames) in os.walk(directory):
            for file in filenames:
                all_files.append(os.path.join(dirpath, file))

        # Purify all SVG files in the current directory
        for unpurified_file in all_files:
            if unpurified_file.endswith('.svg'):
                doc = minidom.parse(unpurified_file)
                main_svg = doc.getElementsByTagName('svg')[0]

                clean_element(main_svg)

                svg_xml = main_svg.toxml()

                # Validates and repairs the purified file
                scour_options = scour.sanitizeOptions()
                scour_options.indent_type = 'none'
                scour_options.no_line_breaks = True
                scour_options.newlines = False
                scour_options.enable_id_stripping = True
                scour_options.shorten_ids = True
                scour_options.strip_xml_prolog = True
                scour_options.remove_descriptive_elements = True
                scour_options.strip_comments = True
                scour_options.enable_viewboxing = True

                svg_xml = scour.scourString(
                    main_svg.toxml(), options=scour_options)

                purified_file = os.path.join(args.output, unpurified_file)

                if not os.path.exists(os.path.dirname(purified_file)):
                    os.makedirs(os.path.dirname(purified_file))

                with open(purified_file, 'w') as f:
                    f.write(svg_xml)
