# Storing Variable Components in UFO files

## Introduction

### What are Variable Components?

In font tech, a "component" is generally understood to be a reference to another glyph, optionally applying a transformation. A glyph made exclusively of components is often called a "composite glyph".

In the UFO font storage format, [component references are described](https://unifiedfontobject.org/versions/ufo3/glyphs/glif/#component) with the `<component>` tag in `*.glif` files.

A Variable Component is like a "regular" component, but it adds the designspace location of the referenced glyph.

In Glyphs, a very similar contruct is known as “Smart Components”.

### What is a Local Design Space?

Around UFO, `.designspace` files are used to describe the axes and source locations for an interpolatable font system. The axes in this file are generally meant to face the end user. For example a "Weight" axis defines the range of weights the system is capable of. It also defines the source locations: for example all the "light" glyphs come from one UFO, and all the "bold" glyphs come from another.

In the context of Variable Components, however, it is often useful for glyphs to have their own designspace, which can implement features that are specific to the glyph, and are specific to Variable Component use.

### Better interpolatable transformations

Components in UFO can be transformed with an 2D Affine transformation matrix. This covers many useful transformations, but is not great for interpolation. For example, if a component is rotated by 20 degrees in one instance, and 40 degrees in another, it is not immediately obvious how to “interpolate” an Affine matrix so the intermediate will be rotated by 30 degrees.

To overcome this, we will define separate transformation parameters such as “rotation angle” and “scale factor”, instead of using the more compact Affine matrix.

## Variable Components in UFO

We will use the glyph "lib" mechanism to store the data for Variable Components and Local Design Spaces.

### Variable Component references

Instead of extending the existing `<component>` mechanism in UFO, we define an additional set of components that will have the desired properties.

The Variable Components for a glyph will be stored as a list in the `glyph.lib`, under this key:

- `com.black-foundry.variable-components`

The list contains zero or more dictionaries, each of which describes a variable component. Such a dictionary has at most three keys: `base`, `transformation` and `location`, the latter two being optional.

#### Base name

The value for the `base` key is the glyph name of the referenced glyph.

#### Transformation

The value for the `transformation` is a dictionary with the following keys:

| key | value | default value |
|-|-|-|
| `x` | `x` translation in font units | `0` |
| `y` | `y` translation in font units | `0` |
| `rotation` | rotation angle in counter-clockwise degrees | `0` |
| `xScale` | scale factor for the `x` dimension | `1` |
| `yScale` | scale factor for the `y` dimension | `1` |
| `xSkew` | skew angle `x` (needs clarification) | `0` |
| `ySkew` | skew angle `y` (ditto) | `0` |
| `xTransformationCenter` | the `x` value for the center of transformation | `0` |
| `yTransformationCenter` | the `y` value for the center of transformation | `0` |

All values are numbers. All keys are optional. If the `transformation` dictionary is empty, it can be omitted entirely.

#### Design Space Location

The value for the `location` key is a dictionary, with axis names as keys, and axis values as values. Axis names are strings, axis values are numbers. If the `location` dictionary is empty, it can be omitted entirely.

### Glyph-level Design Space

`com.black-foundry.glyph-designspace`

#### Axes

`axes`

#### Variation sources

`sources`

## Processing

### Transformation

### Missing Axis values

### Local Axes that redefine Global Axes

---

References:

- [UFO component specification](https://unifiedfontobject.org/versions/ufo3/glyphs/glif/#component)
- [DesignSpace documentation](https://fonttools.readthedocs.io/en/latest/designspaceLib/index.html)
- [Variable Components in OpenType proposal](https://github.com/BlackFoundryCom/variable-components-spec)
- [rcjktools](https://github.com/BlackFoundryCom/rcjk-tools)
