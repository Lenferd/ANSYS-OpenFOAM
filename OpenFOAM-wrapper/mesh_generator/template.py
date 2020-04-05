MESH_FILE_TEMPLATE = \
r"""/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  7
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

convertToMeters    0.001;

vertices
(

$points

);

blocks
(
$fragmentation
);

edges
(
);

boundary
(
$boundary
);

mergePatchPairs
(
);

// ************************************************************************* //
"""

BOUNDARY_TEMPLATE = \
    r"""    $name
    {
        type patch;
        faces
        (
$faces
        );
    }"""
