# Storing Variable Components in UFO files

## Introduction

### What are Variable Components?

In font tech, a "component" is generally understood to be a reference to another glyph, optionally applying a transformation. A glyph made exclusively of components is often called a "composite glyph".

In the UFO font storage format, [component references are described](https://unifiedfontobject.org/versions/ufo3/glyphs/glif/#component) with the `<component>` tag in `*.glif` files.

A Variable Component is like a "regular" component, but it adds the designspace location of the referenced glyph.

In Glyphs, a very similar contruct is known as “Smart Components”.

### What are Variable Glyphs?

In an interpolatable font family setup, glyphs generally interpolate, and therefore are variable. This variability is generally seen from a global designspace perspective. For example: the font has a Weight axis, therefore the glyphs are variable along the Weight axis.

In the context of Variable Components, however, it is often useful for glyphs to have their own local designspace, that implements features that are specific to the glyph, and are specific to Variable Component use.

### Better interpolatable transformations

Components in UFO can be transformed with an 2D Affine transformation matrix. This covers many useful transformations, but is not great for interpolation. For example, if a component is rotated by 20 degrees in one instance, and 40 degrees in another, it is not immediately obvious how to “interpolate” an Affine matrix so the intermediate will be rotated by 30 degrees.

To overcome this, we will define separate transformation parameters such as “rotation angle” and “scale factor”, instead of using the more compact Affine matrix.

## Variable Components in UFO

### Variable Component references

`com.black-foundry.variable-components`

List of dictionaries

#### Base name

`base` key

#### Transformation

`transformation`

#### Designspace Location

`location`

### Glyph-level designspace

`com.black-foundry.glyph-designspace`

#### Axes

`axes`

#### Variation sources

`sources`



---

References:

- [UFO component specification](https://unifiedfontobject.org/versions/ufo3/glyphs/glif/#component)
- [DesignSpace documentation](https://fonttools.readthedocs.io/en/latest/designspaceLib/index.html)
- [Variable Components in OpenType proposal](https://github.com/BlackFoundryCom/variable-components-spec)
- [rcjktools](https://github.com/BlackFoundryCom/rcjk-tools)
