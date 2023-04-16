from xml.dom import minidom
import os
import argparse

# Indirect dependencies
import svgcheck

# Create a list of all the standard SVG attributes that exist in the SVG specification.
valid_attributes = ['d', 'xmlns', 'style', 'x', 'y', 'rx', 'ry', 'height', 'width', 'fill', 'stroke', 'stroke-width', 'viewBox', 'transform', 'stroke-linecap',
                    'stroke-linejoin', 'stroke-miterlimit', 'stroke-dasharray', 'stroke-dashoffset', 'stroke-opacity', 'fill-opacity', 'fill-rule', 'clip-rule', 'cx', 'cy', 'r']

# Create a list of all the standard SVG elements that exist in the SVG specification.
valid_elements = ['svg', 'path', 'rect', 'g', 'defs', 'linearGradient', 'stop', 'radialGradient', 'clipPath', 'mask', 'filter', 'feGaussianBlur', 'feOffset', 'feBlend', 'feColorMatrix', 'feMerge', 'feMergeNode', 'feComposite', 'feFlood', 'feTile', 'feTurbulence', 'feDisplacementMap', 'feDiffuseLighting', 'feSpecularLighting', 'feDistantLight', 'fePointLight', 'feSpotLight', 'feMorphology', 'feConvolveMatrix', 'feImage', 'feComponentTransfer', 'feFuncR', 'feFuncG', 'feFuncB', 'feFuncA', 'feComposite', 'feMerge', 'feMergeNode', 'feOffset', 'feGaussianBlur', 'feColorMatrix', 'feBlend', 'feFlood', 'feTile', 'feTurbulence', 'feDisplacementMap', 'feDiffuseLighting', 'feSpecularLighting', 'feDistantLight', 'fePointLight', 'feSpotLight', 'feMorphology', 'feConvolveMatrix', 'feImage', 'feComponentTransfer', 'feFuncR', 'feFuncG', 'feFuncB', 'feFuncA', 'feComposite', 'feMerge', 'feMergeNode', 'feOffset', 'feGaussianBlur', 'feColorMatrix', 'feBlend', 'feFlood', 'feTile', 'feTurbulence', 'feDisplacementMap', 'feDiffuseLighting', 'feSpecularLighting', 'feDistantLight', 'fePointLight', 'feSpotLight', 'feMorphology', 'feConvolveMatrix', 'feImage', 'feComponentTransfer', 'feFuncR', 'feFuncG', 'feFuncB', 'feFuncA', 'feComposite', 'feMerge', 'feMergeNode', 'feOffset', 'feGaussianBlur', 'feColorMatrix', 'feBlend', 'feFlood', 'feTile', 'feTurbulence', 'feDisplacementMap', 'feDiffuseLighting', 'feSpecularLighting', 'feDistantLight', 'fePointLight', 'feSpotLight',
                  'feMorphology', 'feConvolveMatrix', 'feImage', 'feComponentTransfer', 'feFuncR', 'feFuncG', 'feFuncB', 'feFuncA', 'feComposite', 'feMerge', 'feMergeNode', 'feOffset', 'feGaussianBlur', 'feColorMatrix', 'feBlend', 'feFlood', 'feTile', 'feTurbulence', 'feDisplacementMap', 'feDiffuseLighting', 'feSpecularLighting', 'feDistantLight', 'fePointLight', 'feSpotLight', 'feMorphology', 'feConvolveMatrix', 'feImage', 'feComponentTransfer', 'feFuncR', 'feFuncG', 'feFuncB', 'feFuncA', 'feComposite', 'feMerge', 'feMergeNode', 'feOffset', 'feGaussianBlur', 'feColorMatrix', 'feBlend', 'feFlood', 'feTile', 'feTurbulence', 'feDisplacementMap', 'feDiffuseLighting', 'feSpecularLighting', 'feDistantLight', 'fePointLight', 'feSpotLight', 'feMorphology', 'feConvolveMatrix', 'feImage', 'feComponentTransfer', 'feFuncR', 'feFuncG', 'feFuncB', 'feFuncA', 'feComposite', 'feMerge', 'feMergeNode', 'feOffset', 'feGaussianBlur', 'feColorMatrix', 'feBlend', 'feFlood', 'feTile', 'feTurbulence', 'feDisplacementMap', 'feDiffuseLighting', 'feSpecularLighting', 'feDistantLight', 'fePointLight', 'feSpotLight', 'feMorphology', 'feConvolveMatrix', 'feImage', 'feComponentTransfer', 'feFuncR', 'feFuncG', 'feFuncB', 'feFuncA', 'feComposite', 'feMerge', 'feMergeNode', 'feOffset', 'feGaussianBlur', 'feColorMatrix', 'feBlend', 'feFlood', 'feTile', 'feTurbulence', 'feDisplacementMap', 'feDiffuseLighting', 'feSpecularLighting', 'feDistantLight', 'fePointLight', 'feSpotLight', 'feMorphology']


# Removes all non-essential attributes from an element and calls itself recursively on all children if the child is necessary to keep (i.e. is not metadata, comment, etc).
def clean_element(element: minidom.Element):
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


# Removes all whitespace (newlines included) from an element and calls itself recursively on all children.
def remove_wasted_space(element: minidom.Element):
    for child in list(element.childNodes):
        if child.nodeType == minidom.Node.ELEMENT_NODE:
            remove_wasted_space(child)
        elif child.nodeType == minidom.Node.TEXT_NODE:
            child.data = child.data.replace(
                ' ', '').replace('\n', '').replace('\t', '')


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

    parser.add_argument('-v', '--validate',
                        type=bool,
                        default=True,
                        help="Whether to validate after purification or not ([Default] True or False).")

    parser.add_argument('-o', '--overwrite',
                        type=bool,
                        default=False,
                        help="Whether to overwrite the original files or not (True or [Default] False).")

    args = parser.parse_args()

    subfolder = 'purified' if args.overwrite else ''
    purified_folder = os.path.join(args.directory, subfolder)

    if not os.path.exists(purified_folder):
        os.makedirs(purified_folder)

    all_files = [file for file in os.listdir(
        args.directory) if os.path.isfile(os.path.join(args.directory, file))]

    # Purify all SVG files in the specified directory
    for file in all_files:
        if file.endswith('.svg'):
            doc = minidom.parse(os.path.join(args.directory, file))
            main_svg = doc.getElementsByTagName('svg')[0]

            clean_element(main_svg)
            remove_wasted_space(main_svg)

            purified_file = os.path.join(purified_folder, file)

            with open(purified_file, 'w') as f:
                f.write(main_svg.toxml())

            # Validates and repairs the purified file
            if args.validate:
                os.system(f'svgcheck -r -q {purified_file}')
