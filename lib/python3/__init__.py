# Copyright (C) 2015, 2016, 2017 Monotype Imaging Inc. All rights reserved.
# Confidential information of Monotype Imaging Inc.
#
# __init__.py
#

"""
Package file for LibFont-fontio bridge.
"""

import os
import tempfile
import libfont3backend
from fontio3 import fontedit


#
# Globals
#

validOutputTypes = ['TTF', 'OTF', 'EOT', 'WOFF', 'WOFF2', 'SVG']

TYPE_STRING_MAP = {"TTF": 1, "OTF": 6, "EOT": 2, "WOFF": 3, "WOFF2": 4, "SVG": 5}

LIBFONT_ERROR_MAP = {
    0: "Success.",
    1: "Glyph was added to collection.",
    256: "Something wrong with the font.",
    257: "Item not covered in table.",
    260: "Out of memory.",
    264: "Invalid subtable.",
    265: "Invalid offset.",
    272: "Invalid length.",
    273: "Invalid index.",
    274: "Invalid type.",
    275: "Could not open file.",
    276: "Could not open file for write.",
    277: "Table missing.",
    278 : "maxp table and cff table mismatch.",
    512: "Unsupported.",
    513: "Invalid parameter.",
    514: "Stream overrun.",
    515: "Compression Error.",
    516: "Conversion Error.",
    528: "Refit Error.",
    529: "Componentization Error.",
    768: "Not Implemented.",
    1024: "LF_HARMONIZE_PATHS: The output path must be different from the input path.",
    1025: "LF_HARMONIZE_NUM_GLYPHS: All the input fonts must have the same number of glyphs.",
    1026: "LF_HARMONIZE_CMAP: The fonts do not have the glyphs in the same order.",
    1027: "LF_HARMONIZE_COMPOSITES: The fonts do not have composites at the same indexes, or components are different.",
    1028: "LF_HARMONIZE_POST_NAMES: The post table names of glyphs are not the same in all the fonts.",
    1029: "LF_HARMONIZE_POST_VERS: The fonts do not all have the same post table version, or have an unsupported version.",
    1030: "LF_HARMONIZE_CONTOURS: The fonts do not all have the same number of contours in the glyphs."
    }


#
# Exception class
#

class LibFontError(Exception):
    pass


#
# Methods
#

def getFontType(fontPath):
    """
    Returns the type of the given font file as a string. Possible
    return values are TTF, OTF, EOT, WOFF, WOFF2. Raises exception
    if libfont can't read the font.
    NOTE: Libfont does not read SVG fonts.
    """
    font = libfont3backend.lfapi_createFont()

    result = libfont3backend.lfapi_readFont(font, fontPath, False)
    if result != 0:
        raise LibFontError("Could not read font.")

    fonttype = libfont3backend.lfapi_getFontType(font)
    if type(fonttype) != str:
        raise LibFontError("Could not get font's type.")

    libfont3backend.lfapi_destroyFont(font)

    return fonttype

def getFontFlavor(fontPath):
    """
    Returns the flavor of the given font file as a string.
    Possible values are:
        "VERSION1"    0x00010000
        "VERSION2"    0x00020000
        "VERSION2.1"  0x00020001    (EOT)
        "VERSION2.2"  0x00020002    (EOT)
        "TRUETYPE"    0x74727565
        "CFF"         0x4F54544F    (woff, woff2 with cff table will return this)
        "WOFF"        0x774F4646
        "WOFF2"       0x774F4632
        "UNKONWN"     0xFFFFFFFF
    Raises exception if libfont can't read the font.
    NOTE: Libfont does not read SVG fonts.
    """
    font = libfont3backend.lfapi_createFont()

    result = libfont3backend.lfapi_readFont(font, fontPath, False)
    if result != 0:
        raise LibFontError("Could not read font.")

    sig = libfont3backend.lfapi_getFontFlavor(font)
    if type(sig) != str:
        raise LibFontError("Could not get font's flavor.")

    libfont3backend.lfapi_destroyFont(font)

    return sig


# Name table nameIDs which are used below:
# copyright notice      = 0
# font family name      = 1
# font subsumily name   = 2
# font full name        = 4


def getFontNameString(fontPath, nameID=0, platformID=3, encodingID=1, languageID=0x409):
    """
    Returns the 3,1,U.S. English string for the given nameID from the font.
    """
    if platformID != 3 or encodingID != 1 or languageID != 0x409:
        raise LibFontError("Sorry libfont doesn't support getting anything other than 3,1,English US.")

    font = libfont3backend.lfapi_createFont()

    result = libfont3backend.lfapi_readFont(font, fontPath, False)
    if result != 0:
        raise LibFontError("Could not read font.")

    result = libfont3backend.sfnt_unpack(font)
    if result != 0:
        raise LibFontError("Failed to unpack font.")

    retval = libfont3backend.name_getString(font, nameID, platformID, encodingID, languageID)
    if type(retval) != str:
        print(type(retval))
        if retval == 274:
            raise LibFontError("Font's name table does not have nameID %d.", nameID)
        else:
            raise LibFontError("Unable to get the name table string.")

    libfont3backend.lfapi_destroyFont(font)

    return retval


def getCopyright(fontPath):
    """
    Returns the 3,1,English-US Copyright string from the given font
    as a Unicode string. Raises exception if there is a problem,
    or the string is not in the font.
    """
    return getFontNameString(fontPath, 0)


def getFamilyName(fontPath):
    """
    Returns the 3,1,English-US Family Name string from the given font
    as a Unicode string. Raises exception if there is a problem,
    or the string is not in the font.
    """
    return getFontNameString(fontPath, 1)


def getSubFamilyName(fontPath):
    """
    Returns the 3,1,English-US Subfamily Name string from the given font
    as a Unicode string. Raises exception if there is a problem,
    or the string is not in the font.
    """
    return getFontNameString(fontPath, 2)


def getFullFontName(fontPath):
    """
    Returns the 3,1,English-US Full Font Name string from the given font
    as a Unicode string. Raises exception if there is a problem,
    or the string is not in the font.
    """
    return getFontNameString(fontPath, 4)


def extensionForType(typeString):
    """
    Returns the extension for the given font type.
    """
    return {"TTF": ".ttf",
            "OTF": ".otf",
            "EOT": ".eot",
            "WOFF": ".woff",
            "WOFF2": ".woff2",
            "SVG": ".svg"}.get(typeString.upper(), 0)


def subsetFont(inputFont, unicodes, outputType, outputFont, **kwargs):
    """
    Subsets inputFont with unicodes to outputFont having type outputType.
    Some parameters can be set via kwargs, otherwise libfont defaults are used.
    Raises exception if there is a problem.

    Params:
        inputFont       full path to input font
        unicodes        list of integers (not a Unicode string)
        outputType      type of font to write ('TTF', 'OTF', 'EOT', 'WOFF', 'WOFF2', or 'SVG')
        outputFont      full path to output font, including extension. Method ExtensionForType can
                        be used to get the extension for a given type
        **kwargs        optional arguments (the first controls subsetting, the 2nd controls whether
                        all tables are retained, and the rest control writing)
                        "normalize"   (boolean) True will cause normalization to be run on the Unicodes
                                                (assumption is that they are in natural text order)
                        "alltables"   (boolean) True to keep all tables
                        "sfnt_ttf"    (boolean) True to force woff, woff2, and eot fonts to have
                                                glyf and loca tables.
                        "sfnt_cff"    (boolean) True to force woff, woff2, and eot output fonts to
                                                have a cff table.
                        "woff"        (integer) woff compression level (0-9). Default = 9.
                        "woffminsize" (integer) minimum table size which will be compressed. Default = 0.
                        "woff2"       (integer) woff2 compression level (0-11). Default = 6.
                        "convtol"     (float)   conversion tolerance (0.3-5.0). Default = 0.5.
                        "post"        (integer) post table version (0x00020000 or 0x00030000). Default 0 (keeps original
                                                version).
                        "upm"         (integer) units per em of output font. (doesn't work yet)
                        "svgid"       (string)  svg id to be put into SVG font
                        "metadata"    (string)  to insert metadata: path to the metadata file
                                                to extract metadata: path to non-existent file to write metadata to
                                                to remove metadata from font: "NULL"
                        "privatedata" (string)  to insert private data: path to the private data file
                                                to extract private data: path to non-existent file to write private
                                                data
                                                to remove private data from font: "NULL"
    """
    if not outputType.upper() in validOutputTypes:
        raise LibFontError("Unknown output type: %s" % outputType)

    font = libfont3backend.lfapi_createFont()

    keepall = False
    if ("alltables" in kwargs) and (kwargs["alltables"] == True):
        keepall = True

    result = libfont3backend.lfapi_readFont(font, inputFont, keepall)
    if result != 0:
        libfont3backend.lfapi_destroyFont(font)
        raise LibFontError("Could not read font.")

    subsetargs = {}
    if "normalize" in kwargs:
        subsetargs = {"normalize": kwargs["normalize"]}

    # for key in subsetargs:
    #     print "keyword arg: %s: %s" % (key, kwargs[key])

    result = libfont3backend.lfapi_subsetFont(font, unicodes, **subsetargs)
    if result != 0:
        libfont3backend.lfapi_destroyFont(font)
        if result == -1:
            raise LibFontError("Failed to subset font. Error parsing kwargs.")
        raise LibFontError("Failed to subset font. Libfont error code: %s %s" %
                           (result, LIBFONT_ERROR_MAP.get(result, 0)))

    outtype = TYPE_STRING_MAP.get(outputType, 0)

    result = libfont3backend.lfapi_writeFont(font, outputFont, outtype, **kwargs)

    libfont3backend.lfapi_destroyFont(font)

    if result != 0:
        if result == -1:
            raise LibFontError("Failed to write font. Error parsing kwargs.")
        raise LibFontError("Failed to write font. Libfont error code: %s %s" %
                           (result, LIBFONT_ERROR_MAP.get(result, 0)))


def writeFont(inputFont, outputType, outputFont, **kwargs):
    """
    Converts inputFont to outputFont. outputFont is written to disk.
    By default non-essential tables are removed. To keep all tables,
    specify alltables=True in the kwargs.

    Params:
        inputFont       full path to input font
        outputType      type of font to write ('TTF', 'OTF', 'EOT', 'WOFF', 'WOFF2', or 'SVG')
        outputFont      full path to output font, including extension. Method ExtensionForType can
                        be used to get the extension for a given type.
        **kwargs        optional arguments:
                       "alltables"    (boolean) True to keep all tables. By default the following
                                                are retained:  cmap, cvt, fpgm, gasp, glyf, GDEF,
                                                GPOS, GSUB, hdmx, head, hhea, hmtx, kern, loca,
                                                maxp, name, OS/2, post, prep,vdmx, vhea, vmtx
                        "sfnt_ttf"    (boolean) True to force woff, woff2, and eot fonts to have
                                                glyf and loca tables.
                        "sfnt_cff"    (boolean) True to force woff, woff2, and eot output fonts to
                                                have a cff table.
                        "woff"        (integer) woff compression level (0-9). Default = 9.
                        "woffminsize" (integer) minimum table size which will be compressed. Default = 0.
                        "woff2"       (integer) woff2 compression level (0-11). Default = 6.
                        "convtol"     (float)   conversion tolerance (0.3-5.0). Default = 0.5.
                        "post"        (integer) post table version (0x00020000 or 0x00030000). Default 0 (keeps original
                                                version).
                        "upm"         (integer) units per em of output font. (doesn't work yet)
                        "svgid"       (string)  svg id to be put into SVG font
                        "metadata"    (string)  to insert metadata: path to the metadata file
                                                to extract metadata: path to non-existent file to write metadata to
                                                to remove metadata from font: "NULL"
                        "privatedata" (string)  to insert private data: path to the private data file
                                                to extract private data: path to non-existent file to write private
                                                data to
                                                to remove private data from font: "NULL"
    """
    if outputType not in validOutputTypes:
        raise LibFontError("Unknown output type: %s" % outputType)

    font = libfont3backend.lfapi_createFont()

    keepall = False
    if ("alltables" in kwargs) and (kwargs["alltables"] == True):
        keepall = True

    result = libfont3backend.lfapi_readFont(font, inputFont, keepall)
    if result != 0:
        libfont3backend.lfapi_destroyFont(font)
        raise LibFontError("Could not read font.")

    outtype = TYPE_STRING_MAP.get(outputType, 0)

    result = libfont3backend.lfapi_writeFont(font, outputFont, outtype, **kwargs)

    libfont3backend.lfapi_destroyFont(font)

    if result != 0:
        if result == -1:
            raise LibFontError("Failed to write font. Error parsing kwargs.")
        raise LibFontError("Failed to write font. Libfont error code: %s %s" %
                           (result, LIBFONT_ERROR_MAP.get(result, 0)))


def writeFontToMemory(inputFont, outputType, **kwargs):
    """
    Converts inputFont to an in memory font of outputType.
    By default non-essential tables are removed. To keep all tables, specify alltables=True in the kwargs.
    Returns a bytestring containing the converted font if it works. Raises exception on failure.

    Params:
        inputFont       full path to input font.
        outputType      type of font to write ('TTF', 'OTF', 'EOT', 'WOFF', 'WOFF2', or 'SVG')

        **kwargs        optional arguments:
                       "alltables"    (boolean) True to keep all tables. By default the following
                                                are retained:  cmap, cvt, fpgm, gasp, glyf, GDEF,
                                                GPOS, GSUB, hdmx, head, hhea, hmtx, kern, loca,
                                                maxp, name, OS/2, post, prep,vdmx, vhea, vmtx
                        "sfnt_ttf"    (boolean) True to force woff, woff2, and eot fonts to have
                                                glyf and loca tables.
                        "sfnt_cff"    (boolean) True to force woff, woff2, and eot output fonts to
                                                have a cff table.
                        "woff"        (integer) woff compression level (0-9). Default = 9.
                        "woffminsize" (integer) minimum table size which will be compressed. Default = 0.
                        "woff2"       (integer) woff2 compression level (0-11). Default = 6.
                        "convtol"     (float)   conversion tolerance (0.3-5.0). Default = 0.5.
                        "post"        (integer) post table version (0x00020000 or 0x00030000). Default 0 (keeps original
                                                version).
                        "upm"         (integer) units per em of output font. (doesn't work yet)
                        "svgid"       (string)  svg id to be put into SVG font
                        "metadata"    (string)  to insert metadata: path to the metadata file
                                                to extract metadata: path to non-existent file to write metadata to
                                                to remove metadata from font: "NULL"
                        "privatedata" (string)  to insert private data: path to the private data file
                                                to extract private data: path to non-existent file to write private
                                                data to
                                                to remove private data from font: "NULL"
    """
    if outputType not in validOutputTypes:
        raise LibFontError("Unknown output type: %s" % outputType)

    font = libfont3backend.lfapi_createFont()

    keepall = False
    if ("alltables" in kwargs) and (kwargs["alltables"] == True):
        keepall = True

    result = libfont3backend.lfapi_readFont(font, inputFont, keepall)
    if result != 0:
        libfont3backend.lfapi_destroyFont(font)
        raise LibFontError("Could not read font.")

    result = libfont3backend.lfapi_writeFontToMemory(font, TYPE_STRING_MAP.get(outputType, 0), **kwargs)

    libfont3backend.lfapi_destroyFont(font)

    if type(result) == int:
        if result == -1:
            raise LibFontError("Failed to write font. Error parsing kwargs.")
        raise LibFontError("Failed to write font. Libfont error code: %s %s" %
                           (result, LIBFONT_ERROR_MAP.get(result, 0)))

    return result


def fontEditorFromFont(inputFont, retainAllTables=False):
    """
    Returns an Editor object from the given font. Operates by using libfont to
    create a temporary ttf or otf font (on disk) then creates the Editor with
    e = fontedit.Editor.frombytes()

    Params:
        inputFont           full path to input font
        retainAllTables     set to True to keep all tables. By default the following
                            are retained:  cmap, cvt, fpgm, gasp, glyf, GDEF, GPOS, GSUB,
                            hdmx, head, hhea, hmtx, kern, loca, maxp, name, OS/2, post, prep,
                            vdmx, vhea, vmtx
    """
    font = libfont3backend.lfapi_createFont()

    result = libfont3backend.lfapi_readFont(font, inputFont, retainAllTables)
    if result != 0:
        libfont3backend.lfapi_destroyFont(font)
        raise LibFontError("Could not read font.")

    tempdir = tempfile.gettempdir()

    tmpoutput = os.path.join(tempdir, 'libfont3.tmp')

    fonttype = libfont3backend.lfapi_getFontType(font)

    if type(fonttype) != str:
        libfont3backend.lfapi_destroyFont(font)
        raise LibFontError("Failed to get font type.")

    flavor = libfont3backend.lfapi_getFontFlavor(font)

    tempFormat = "TTF"
    if type(fonttype) != str:
        libfont3backend.lfapi_destroyFont(font)
        raise LibFontError("Failed to get font flavor.")

    if fonttype == "OTF" or flavor == "CFF":
        tempFormat = "OTF"

    result = libfont3backend.lfapi_writeFont(font, tmpoutput, TYPE_STRING_MAP.get(tempFormat, 0))
    if result != 0:
        libfont3backend.lfapi_destroyFont(font)
        raise LibFontError("Failed to write temporary font.")

    try:
        with open(tmpoutput, 'rb') as f:
            b = f.read()
            e = fontedit.Editor.frombytes(b)
    except:
        raise LibFontError("Failed to read temporary font.")
    finally:
        os.remove(tmpoutput)

    libfont3backend.lfapi_destroyFont(font)

    return e


def fontEditorToFont(e, outputType, outputFont, **kwargs):
    """
    Writes font of given type. Operates by using libfont to
    create a temporary font using fontio; then writes to outputFont using libfont.

    Params:
        e               -- Editor object
        outputType      -- type of font to write ('TTF', 'OTF', 'EOT', 'WOFF', 'WOFF2', or 'SVG')
        outputFont      -- full path to output font, including extension. ExtensionForType() can be
                           used to get the extension
        **kwargs        -- optional arguments:
                           "alltables"   (boolean) True to keep all tables. By default the following
                                                   are retained:  cmap, cvt, fpgm, gasp, glyf, GDEF,
                                                   GPOS, GSUB, hdmx, head, hhea, hmtx, kern, loca,
                                                   maxp, name, OS/2, post, prep, vdmx, vhea, vmtx
                           "sfnt_ttf"    (boolean) True to force woff, woff2, and eot fonts to have
                                                   glyf and loca tables.
                           "sfnt_cff"    (boolean) True to force woff, woff2, and eot output fonts to
                                                   have a cff table.
                           "woff"        (integer) woff compression level (0-9). Default = 9.
                           "woffminsize" (integer) minimum table size which will be compressed. Default = 0
                           "woff2"       (integer) woff2 compression level (0-11). Default = 6.
                           "convtol"     (float)   conversion tolerance (0.3-5.0). Default = 0.5.
                           "post"        (integer) post table version (0x00020000 or 0x00030000). Default 0 (keeps
                                                   original version).
                           "upm"         (integer) units per em of output font. (doesn't work yet)
                           "svgid"       (string)  svg id to be put into SVG font
                           "metadata"    (string)  to insert metadata: path to the metadata file
                                                   to extract metadata: path to non-existent file to write metadata to
                                                   to remove metadata from font: "NULL"
                           "privatedata" (string)  to insert private data: path to the private data file
                                                   to extract private data: path to non-existent file to write private
                                                   data to
                                                   to remove private data from font: "NULL"
    """
    if outputType not in validOutputTypes:
        raise LibFontError("Unknown output type: %s" % outputType)

    tempdir = tempfile.gettempdir()

    tmpinput = os.path.join(tempdir, 'libfont.tmp')
    #  print (tmpinput)

    e.writeFont(tmpinput)

    font = libfont3backend.lfapi_createFont()

    keepall = False
    if ("alltables" in kwargs) and (kwargs["alltables"] == True):
        keepall = True

    result = libfont3backend.lfapi_readFont(font, tmpinput, keepall)
    if result != 0:
        libfont3backend.lfapi_destroyFont(font)
        raise LibFontError("Could not read font.")

    result = libfont3backend.lfapi_writeFont(font, outputFont, TYPE_STRING_MAP.get(outputType, 0), **kwargs)

    os.remove(tmpinput)

    libfont3backend.lfapi_destroyFont(font)

    if result != 0:
        if result == -1:
            raise LibFontError("Failed to write font. Error parsing kwargs.")
        raise LibFontError("Failed to write font. Libfont error code: %s %s" %
                           (result, LIBFONT_ERROR_MAP.get(result, 0)))



def writeCSSFile(inputFont, CSSFile, **kwargs):
    """
    Writes a sample CSS file for the given font. Default is to put
    eot, woff2. woff, and ttf entries into the file. To override that
    specify the ones you want in the kwargs

    Params:
        inputFont       -- full path to input font
        CSSFile         -- full path to the CSS file

        **kwargs        -- optional arguments:
                            "types"    (string) comma delimted list of font types, may be 'TTF',
                                                'OTF', 'EOT', 'WOFF', 'WOFF2', or 'SVG' (case
                                                sensitive)
                            "svgID"    (string) string to put into CSS file for the name of the SVG
                                                font, overrides default behavior
                            "basename" (string) name of font to put in CSS file, default is the name
                                                of the font file
    """


    font = libfont3backend.lfapi_createFont()

    result = libfont3backend.lfapi_readFont(font, inputFont, False)
    if result != 0:
        libfont3backend.lfapi_destroyFont(font)
        raise LibFontError("Could not read font.")

    base = ''

    if not ("basename" in kwargs):
        path, file = os.path.split(inputFont)
        base, ext = os.path.splitext(file)

    result = libfont3backend.lfapi_writeCSSFile(font, base, CSSFile, **kwargs)
    if result != 0:
        libfont3backend.lfapi_destroyFont(font)
        raise LibFontError("Failed to write CSS file.")

    libfont3backend.lfapi_destroyFont(font)



#
# Test code
#


def _test():
    import doctest
    doctest.testmod()

if __debug__:
    pass

if __name__ == "__main__":
    if __debug__:
        _test()
