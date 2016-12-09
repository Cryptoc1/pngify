# PNGify Spec

This spec is meant to define how PNGify formats [meta]data for storage and transcoding between text and PNGs.

## PNGify Header
The PNGify Header is a bencoded string that prefixes the text to be transcoded into the PNG. It's identified by a starting semi-colon (`;`), and an ending semi-colon, followed by three tab characters (`;\t\t\t`). The header MUST be at the beginning of the image, and CAN NOT be compressed.

The header is used to identify key information about the data that's been encoded, such as: The version of the PNGify encoder used, the compression method used.

The key note here, is that it stores the compression method used. This is important because it allows the PNGify decoder to automatically decompress data without the need for the user to specify.

Parsed Example:
```
{
  'cm': 'brotli',
  'v': 1
}
```

Encoded Example:
```
d2:cm6:brotli1:vi1ee
```
