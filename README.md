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

Variable Components are glyph elements in *addition* to regular components. They can co-exist with outlines and regular components.

With the mechanisms of this document in place, a glyph shape can be composed of three types of elements:

1. Outlines (standard UFO glyph)
2. Components (standard UFO glyph)
3. Variable Components (`glyph.lib` additions)

The Variable Components for a glyph will be stored as a non-empty list in the `glyph.lib`, under this key:

- `com.black-foundry.variable-components`

The list contains one or more dictionaries, each of which describes a variable component. Such a dictionary has at most three keys: `base`, `transformation` and `location`, each of the latter two being optional.

If there are no variable components, the list should *not* be written to `glyph.lib`.

#### Base name

The value for the `base` key is the glyph name of the referenced glyph.

#### Component Transformation

The value for the `transformation` key is a dictionary with the following items:

| key | value | default value |
|-|-|-|
| `translateX` | `x` translation in font units | `0` |
| `translateY` | `y` translation in font units | `0` |
| `rotation` | rotation angle in counter-clockwise degrees | `0` |
| `scaleX` | scale factor for the `x` dimension | `1` |
| `scaleY` | scale factor for the `y` dimension | `1` |
| `skewX` | skew angle `x` in counter-clockwise degrees | `0` |
| `skewY` | skew angle `y` in counter-clockwise degrees | `0` |
| `tCenterX` | the `x` value for the center of transformation | `0` |
| `tCenterY` | the `y` value for the center of transformation | `0` |

All values are numbers. All keys are optional. If the `transformation` dictionary is empty, it should be omitted entirely.

#### Component Design Space Location

The value for the `location` key is a dictionary, with axis names as keys, and axis values as values. Axis names are strings, axis values are numbers. If the `location` dictionary is empty, it should be omitted entirely.

### Glyph-level Design Space

A glyph-level design space can be defined as a dictionary value under the `com.black-foundry.glyph-designspace` key in the `glyph.lib`, in the default source for the glyph.

The dictionary must have two keys: `axes` and `sources`.

#### Axes

The value for the `axes` key is a non-empty list of axis descriptions, each of which is a dictionary with the following items:

| key | value |
|-|-|
| `name` | The `name` of the axis |
| `minimum` | The `minimum` value for the axis |
| `default` | The `default` value for the axis |
| `maximum` | The `maximum` value for the axis |

These items correspond to the same-named `.designspace` `<axis>` attributes. All field are mandatory.

#### Variation sources

The value for the `sources` key is a non-empty list of source descriptions, each of which is a dictionary with the following fields:

| key | value | optional? |
|-|-|-|
| `location` | The design space `location` of the source, as a dictionary of axis name / axis value pairs. If an axis is omitted, the default value for that axis is used. | mandatory |
| `filename` | The file name or relative path (\*) of the UFO containing the source glyph data | optional: if not given, *this* UFO is used |
| `layername` | The UFO layer containing the source glyph data | optional: if not given, the default layer is used |

\*) Similar to a `.designspace` `<source>` element `filename` attribute, this `filename` is relative to the parent folder of *this* UFO.

## Processing

### Transformation

A decomposed transformation can be expressed with commonly used 2D Affine transform operations, like in the following pseudo code (angles are in degrees):

	translate(tCenterX, tCenterY)
	translate(translateX, translateY)
	rotate(rotation)
	scale(scaleX, scaleY)
	skew(skewX, skewY)  # transform([1, tan(skewY), tan(-skewX), 1, 0, 0])
	translate(-tCenterX, -tCenterY)

The order of operations is significant.

Example Python code implementing this is included here: [compose_transform.py](compose_transform.py). The example code also includes a method for decomposing an Affine transform into decomposed parameters.

### Missing Axis values

_To be defined_

### Local Axes that redefine Global Axes

_To be defined_

---

## Relevant links

- [UFO component specification](https://unifiedfontobject.org/versions/ufo3/glyphs/glif/#component)
- [DesignSpace documentation](https://fonttools.readthedocs.io/en/latest/designspaceLib/index.html)
- [Variable Components in OpenType discussion](https://github.com/harfbuzz/boring-expansion-spec/issues/42)
- [Previous Variable Components in OpenType proposal](https://github.com/BlackFoundryCom/variable-components-spec)
- [RoboCJK RoboFont plug-in](https://github.com/BlackFoundryCom/robo-cjk)
- [rcjk-tools, RoboCJK file format tools](https://github.com/BlackFoundryCom/rcjk-tools)
- [Fontra font editor](https://github.com/BlackFoundryCom/fontra)
