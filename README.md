# Storing Variable Components in UFO files

## Introduction

### What are Variable Components?

In font tech, a "component" is generally understood to be a reference to another glyph, optionally applying a transformation. A glyph made exclusively of components is often called a "composite glyph".

In the UFO font storage format, [component references are described](https://unifiedfontobject.org/versions/ufo3/glyphs/glif/#component) with the `<component>` tag in `*.glif` files.

A Variable Component is like a "regular" component, but it adds the designspace location of the referenced glyph.

In Glyphs, a very similar contruct is known as “Smart Components”.

### Better interpolatable transformations

Components in UFO can be transformed with an 2D Affine transformation matrix. This covers many useful transformations, but is not great for interpolation. For example, if a component is rotated by 20 degrees in one instance, and 40 degrees in another, it is not immediately obvious how to “interpolate” an Affine matrix so the intermediate will be rotated by 30 degrees.

To overcome this, we will define separate transformation parameters such as “rotation angle” and “scale factor”, instead of using the more compact Affine matrix.

### Variable Glyphs

To use variable components, we need the referenced glyphs to be variable.

In the source data for a variable font, glyphs generally implement variations for one or more global variation axes, such as "weight" or "width".

However, it is useful for individual glyphs to implement variations along axes that are unique to the glyph. To achieve this, we can define a glyph-local designspace that _augments_ the global design space. A glyph-local designspace can define _additional_ variation axes and _additional_ source glyphs at locations anywhere in the augmented design space.

## Variable Components in UFO

Instead of extending the existing `<component>` mechanism in UFO, we define an additional set of components that will have the desired properties.

Variable Components are glyph elements in *addition* to regular components. They can co-exist with outlines and regular components.

With the mechanisms of this document in place, a glyph shape can be composed of three types of elements:

1. Outlines (standard UFO glyph)
2. Components (standard UFO glyph)
3. Variable Components (`glyph.lib` additions)

We use UFO's glyph "lib" mechanism to store Variable Component data.

The Variable Components for a glyph will be stored as a non-empty list in the `glyph.lib`, under this key:

- `com.black-foundry.variable-components`

The list contains one or more dictionaries, each of which describes a variable component. Such a dictionary has at most three keys: `base`, `transformation` and `location`, each of the latter two being optional.

If there are no variable components, the list should *not* be written to `glyph.lib`.

### Base name

The value for the `base` key is the glyph name of the referenced glyph. The name for this key is chosen for symmetry with the `<component>` element in UFO glyphs, which has a `base` attribute with the same function.

### Component Transformation

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

### Component Design Space Location

The value for the `location` key is a dictionary, with axis names as keys, and axis values as values. Axis names are strings, axis values are numbers. If the `location` dictionary is empty, it should be omitted entirely.

## Variable Glyphs in UFO

In the UFO world, `.designspace` files are used to describe the axes and source locations for a variable font system. A source location links to a UFO layer. The `.designspace` file defines the "global" design space. 

> For simplicity, we consider a single UFO that is not part of a `.designspace` system equavalent to a `.designspace` system that has zero axes and defines a single source (the default UFO layer). Storing variable components in UFO does not _require_ the use of a `.designspace` file.

We use UFO's `glyph.lib` mechanism to store the glyph-specific design space additions for Variable Glyphs.

A glyph-level design space addition can be defined as a dictionary value under the `com.black-foundry.glyph-designspace` key in the `glyph.lib`, in the default UFO layer for the glyph.

The dictionary must have an `axes` key, and may have a `sources` key.

### Axes

The value for the `axes` key is a non-empty list of axis descriptions, each of which is a dictionary with the following items:

| key | value |
|-|-|
| `name` | The `name` of the axis |
| `minimum` | The `minimum` value for the axis |
| `default` | The `default` value for the axis |
| `maximum` | The `maximum` value for the axis |

These items correspond to the same-named `.designspace` `<axis>` attributes. All field are mandatory.

### Variation sources

Each variation source defines a location in the augmented design space. The _location_ implicitly determines in which UFO the glyph source data is stored. The UFO _layer_ is defined explicitly.

The value for the `sources` key is list of source descriptions, each of which is a dictionary with the following fields:

| key | value | optional? |
|-|-|-|
| `name` | The UI name for the source | mandatory -- it has no significance for the data, but it is helpful for designers to identify the source |
| `location` | The design space `location` of the source, as a dictionary of axis name / axis value pairs. Each axis name must either be a global axis name, or a local axis name defined for this glyph. If an axis is omitted, the default value for that axis is implied. | mandatory |
| `layername` | The UFO layer containing the source glyph data | optional: if not given, the default layer is used |

### Which UFO?

The UFO in which the source data is stored is _implied by the global portion of the source location_, via the `.designspace` document.

For example, if a source location is at `Weight=800, Width=30, LocalAxis=23`, where "Weight" and "Width" are global axes, and "LocalAxis" is a local axis, the source UFO will be the one associated with `Weight=800, Width=30`. There _must_ be a source defined in the `.designspace` document for the global portion of the location.

If a variable glyph defines a local axis with the _same name_ as a global axis, the local axis has precedence over the global axis. An axis value for such an axis in a source location belongs to the _local portion_ of the location, and therefore does _not_ participate in deciding which UFO the source data is stored in.

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

### Axis values and nested components

Each glyph's rendered location is determined by its parent composite. If there is no parent, the global design space location is used.

Axis values are passed down the component hierarchy, and can per component be overwritten by an axis value in the component's location. Another way of describing this is this: component locations may be sparse, which allows parent locations to be passed down the component hierarchy.

For example, we have a glyph `/A`, which has a component referencing a glyph `/B`, which in turn references a glyph `/C`. `/C` responds to the global "Weight" axis (meaning it has source locations that include "Weight" variations), but `/B` does not. When we render glyph `/A` at `Weight=234`, that location is passed to `/B`, but `/B` doesn't specify "Weight" in its location for `/C`. `Weight=234` is passed to `/C` in addition to the axis values that `/B` _does_ specify for `/C`.

### Missing axis values in source locations

If a source location does not contain a value for a locally defined axis, the axis' default value is implied.

### Local Axes that use the same name as Global Axes

The behavior for this is a bit of an open question.

Fontra does have a defined behavior in the case, which I will try to describe below. But I am not convinced this is generally useful behavior, and it complicates things and is hard to explain.

When rendering a glyph with a local axis that has the same name as a global axis, the global axis value is remapped from `.designspace` "design space coordinates" to the local axis range. A glyph can therefore effectively override the global axis range value with its own. Note that this breaks down if in one coordinate space the default axis value is the same as a minimum or maximum value, but the other coordinate space it is not, or vice versa.

## Examples

This repository contains a small example project in the
[ExampleVariableComponent](ExampleVariableComponent) folder.

---

## Relevant links

- [UFO component specification](https://unifiedfontobject.org/versions/ufo3/glyphs/glif/#component)
- [DesignSpace documentation](https://fonttools.readthedocs.io/en/latest/designspaceLib/index.html)
- [Variable Components in OpenType discussion](https://github.com/harfbuzz/boring-expansion-spec/issues/42)
- [Previous Variable Components in OpenType proposal](https://github.com/googlefonts/variable-components-spec)
- [RoboCJK RoboFont plug-in](https://github.com/BlackFoundryCom/robo-cjk)
- [rcjk-tools, RoboCJK file format tools](https://github.com/googlefonts/rcjk-tools)
- [Fontra font editor](https://github.com/googlefonts/fontra)
