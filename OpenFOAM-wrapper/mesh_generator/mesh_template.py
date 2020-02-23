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
    topSurface
    {
        type patch;
        faces
        (
            (3 7 6 2)
        );
    }

    bottomSurface
    {
        type patch;
        faces
        (
            (4 0 1 5)
        );
    }

    fixedEnd
    {
        type patch;
        faces
        (
            (0 4 7 3)
        );
    }

    tractionEnd
    {
        type patch;
        faces
        (
            (1 2 6 5)
        );
    }
);

mergePatchPairs
(
);

// ************************************************************************* //
"""