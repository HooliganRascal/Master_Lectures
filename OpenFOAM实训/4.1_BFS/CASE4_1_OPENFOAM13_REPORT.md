# Case 4.1 OpenFOAM 13 Report

## Scope and source

This folder implements Case 4.1, the compressible backward-facing-step case in
`Homework.pdf` (printed pages 49-54, PDF pages 59-64). The implementation was
created and run with the OpenFOAM Foundation distribution from
[openfoam.org](https://openfoam.org/), version 13, build `13-18870c24d21c`.

The three requested legacy solver cases are:

| Case directory | Requested solver identity | OpenFOAM 13 command and module | Momentum model |
| --- | --- | --- | --- |
| `case4_1_sonicFoam/` | `sonicFoam` | `foamRun`, `solver fluid` | laminar |
| `case4_1_rhoCentralFoam/` | `rhoCentralFoam` | `foamRun`, `solver shockFluid` | RAS `kEpsilon` |
| `case4_1_rhoPimpleFoam/` | `rhoPimpleFoam` | `foamRun`, `solver fluid` | RAS `kEpsilon` |

OpenFOAM 13 no longer requires these solvers to exist as three independent
executables. The `fluid` and `shockFluid` modules provide the corresponding
algorithms through `foamRun`. The laminar and turbulent `fluid` cases remain
distinct because their momentum models, transported fields, and PIMPLE
settings differ.

## Shared physical setup

### Geometry and mesh

The mesh reproduces the three-block layout and cell counts specified in the
PDF:

| Quantity | Value |
| --- | ---: |
| Inlet to step | $0.1016\ \mathrm{m}$ |
| Step to outlet | $0.3048\ \mathrm{m}$ |
| Step to upper wall | $0.1475\ \mathrm{m}$ |
| Step height | $0.01125\ \mathrm{m}$ |
| Upstream block | $30\times40\times1$ cells |
| Lower downstream block | $60\times39\times1$ cells |
| Upper downstream block | $60\times40\times1$ cells |
| Total | 5,940 hexahedral cells |

The active directions are $x$ and $y$. The single-cell $z$ direction uses the
`empty` patch `frontAndBack`. All three generated `polyMesh` directories have
identical SHA-256 hashes for `points`, `faces`, `owner`, `neighbour`, and
`boundary`.

`checkMesh -allGeometry -allTopology` confirms one connected region, zero
non-orthogonality, negligible skewness, and correct two-dimensional patch
topology. It also reports one important quality warning:

- 44 cells have determinant below `0.001`
- Minimum determinant: `4.0421222e-05`
- Maximum aspect ratio: `499.48652`

This warning comes from the strong grading in the PDF mesh. It did not prevent
completion, but it limits confidence in near-step gradients, turbulence
quantities, and mesh-independent accuracy.

### Initial state

The initial fields follow the PDF while keeping the perfect-gas state
thermodynamically consistent:

| Region | $p$ (Pa) | $T$ (K) | $U$ ($\mathrm{m/s}$) |
| --- | ---: | ---: | --- |
| Upstream of step | 15,350 | 169.2 | $(651.9,0,0)$ |
| Downstream above step | 13,448.99 | 153 | $(619.9,0,0)$ |
| Downstream behind step | 13,448.99 | 153 | $(0,0,0)$ |

The initial velocity is in the positive $x$ direction. The $z$ component must
remain zero because $z$ is the empty direction. `setFields` writes these three
regions into `0/U`, `0/p`, and `0/T`; as a result, their current internal fields
are nonuniform lists.

For the turbulent cases, the initialized turbulence values are

$$
k=0.375\ \mathrm{m^{2}/s^{2}}
$$

$$
\epsilon=14.855\ \mathrm{m^{2}/s^{3}}
$$

### Boundary conditions

- `inlet`: fixed $U=(651.9,0,0)\ \mathrm{m/s}$, $p=15350\ \mathrm{Pa}$, and
  $T=169.2\ \mathrm{K}$
- `outlet`: zero gradient for $U$, $p$, $T$, $k$, and $\epsilon$
- `upperWall`: slip for $U$ and zero gradient for the scalar fields
- `lowerWall`: no slip for $U$, zero gradient for $p$ and $T$, and lower-wall
  functions for the turbulence fields
- `frontAndBack`: `empty` for every field

The turbulent inlet fixes $k$ and $\epsilon$. `nut` and `alphat` are calculated
fields; `nutkWallFunction` and `compressible::alphatWallFunction` are used on
the lower wall.

### Air model

Each `constant/physicalProperties` uses `hePsiThermo`, `perfectGas`, constant
enthalpy, constant transport, and sensible internal energy with:

| Property | Value |
| --- | ---: |
| Molecular weight | $28.96$ |
| $C_{p}$ | $1005\ \mathrm{J/(kg\,K)}$ |
| Heat of formation $h_{f}$ | $2.544\times10^{6}\ \mathrm{J/kg}$ |
| Dynamic viscosity $\mu$ | $1.827\times10^{-5}\ \mathrm{Pa\,s}$ |
| Prandtl number $Pr$ | $0.7$ |

Density is derived by the thermodynamic model; it is not a supplied field in
the `0/` directories.

## Case file reference

| Path | Purpose |
| --- | --- |
| `0/U` | Velocity initial and boundary conditions |
| `0/p` | Absolute thermodynamic pressure initial and boundary conditions |
| `0/T` | Temperature initial and boundary conditions |
| `0/k` | Turbulent kinetic energy; turbulent cases only |
| `0/epsilon` | Turbulent dissipation rate; turbulent cases only |
| `0/nut` | Turbulent kinematic viscosity; turbulent cases only |
| `0/alphat` | Turbulent thermal diffusivity; turbulent cases only |
| `0/backup/` | Pre-`setFields` copies of every supplied initial-condition file |
| `constant/physicalProperties` | Perfect-gas thermodynamics and air transport data |
| `constant/momentumTransport` | Laminar or RAS `kEpsilon` selection |
| `constant/polyMesh/` | Mesh generated by `blockMesh` |
| `system/blockMeshDict` | Geometry, cell counts, grading, and patch topology |
| `system/setFieldsDict` | Upstream, downstream, and wake initialization regions |
| `system/controlDict` | OpenFOAM 13 module, time controls, Courant limit, and writes |
| `system/fvSchemes` | Time, gradient, flux, divergence, interpolation, and diffusion schemes |
| `system/fvSolution` | Linear solvers and PIMPLE controls |
| `Allrun` | Runs `blockMesh`, full `checkMesh`, `setFields`, and `foamRun` |
| `Allclean` | Removes generated mesh, time directories, logs, and post-processing output |
| `log.foamRun` | Complete solver transcript for the final successful run |
| `0.0005` to `0.0035` | Written solution fields at 0.5 ms intervals |

### Initial-condition backups

The backups were made before `setFields` expanded the region data:

| Case | Files in `0/backup/` |
| --- | --- |
| `case4_1_sonicFoam` | `U.bak`, `p.bak`, `T.bak` |
| `case4_1_rhoCentralFoam` | `U.bak`, `p.bak`, `T.bak`, `k.bak`, `epsilon.bak`, `nut.bak`, `alphat.bak` |
| `case4_1_rhoPimpleFoam` | `U.bak`, `p.bak`, `T.bak`, `k.bak`, `epsilon.bak`, `nut.bak`, `alphat.bak` |

These lists contain every initial-condition file supplied to each case. No
`rho.bak` is needed because `rho` is generated by the compressible
thermodynamic model rather than supplied in `0/`.

## Numerical differences between cases

### sonicFoam identity

- `solver fluid`
- Laminar momentum transport
- Euler time integration
- Limited gradients and first-order upwind convection for robust compressible
  startup
- One PIMPLE outer corrector, two pressure correctors, and transonic pressure
  treatment

This comparison case does not model the turbulence that the PDF identifies as
important to backward-facing-step reattachment.

### rhoCentralFoam identity

- `solver shockFluid`
- RAS `kEpsilon`
- Kurganov central-upwind flux
- `vanAlbada` reconstruction for density and temperature and `vanAlbadaV` for
  velocity
- `smoothSolver` with `symGaussSeidel` for $U$, energy, $k$, and $\epsilon$

### rhoPimpleFoam identity

- `solver fluid`
- RAS `kEpsilon`
- Limited gradients and upwind transported-field convection
- Two PIMPLE outer correctors, two pressure correctors, and transonic pressure
  treatment
- `PBiCGStab` with `DILU` for pressure and transported fields

All three cases run from $t=0$ to $t=0.0035\ \mathrm{s}$ with an initial time
step of $10^{-8}\ \mathrm{s}$, adaptive time stepping, maximum Courant number
`0.4`, maximum time step $2\times10^{-7}\ \mathrm{s}$, and output every
$0.0005\ \mathrm{s}$.

## Run and validation record

The final runs completed as follows:

| Case | Final time | Clock time | Log termination |
| --- | ---: | ---: | --- |
| `case4_1_sonicFoam` | 3.5 ms | 176 s | `End`, exit 0 |
| `case4_1_rhoCentralFoam` | 3.5 ms | 310 s | `End`, exit 0 |
| `case4_1_rhoPimpleFoam` | 3.5 ms | 588 s | `End`, exit 0 |

The full logs contain no `FOAM FATAL`, negative-initial-temperature, bounding,
NaN, floating-point-exception, or segmentation-fault messages. Each log has
exactly one terminal `End` line. Final residuals are finite; the pressure-based
cases finish with small local continuity errors.

Latest-time internal-field diagnostics were:

| Case | $p$ (Pa) | $T$ (K) | $|U|$ ($\mathrm{m/s}$) |
| --- | --- | --- | --- |
| `sonicFoam` | 9,726.5 to 15,891.6 | 142.3 to 268.0 | 0.0059 to 675.7 |
| `rhoCentralFoam` | 354.9 to 15,673.4 | 31.6 to 393.4 | 0.146 to 818.9 |
| `rhoPimpleFoam` | 707.8 to 16,043.7 | 102.7 to 378.3 | 0.178 to 746.1 |

The very low local pressure and temperature and high local velocity in the
turbulent cases should not be hidden. They are consistent with the PDF's
warning that this strongly graded, coarse mesh has difficulty resolving the
recirculation and reattachment region. A completed run is not proof of mesh
independence or agreement with the Smith experiment.

## Pressure-ratio post-processing

All graphing code and outputs are outside the three case directories in
`case4_1_postProcessing/`.

The PDF samples pressure along the horizontal extension of the step. To avoid
mixing the upper downstream block into that trace, the extractor selects the
first lower-block cell row below the step plane:

| Sampling quantity | Definition |
| --- | --- |
| Physical time | latest common time, $t=0.0035\ \mathrm{s}$ |
| Streamwise interval | step at $x=0$ to outlet at $x=0.3048\ \mathrm{m}$ |
| Sample row | $y=-2.31233916566\times10^{-5}\ \mathrm{m}$ |
| Spanwise coordinate | $z=0$ |
| Horizontal graph coordinate | $(x-x_{\mathrm{step}})/0.0254$ inches |
| Vertical graph coordinate | $p/p_{\infty}$ |
| Reference pressure | $p_{\infty}=15350\ \mathrm{Pa}$ |
| Samples per case | 60 raw cell-centered values |

The graph axis begins at zero at the step and ends at the 12-inch outlet. The
first and last raw cell centers are at approximately `0.00455 in` and
`11.5453 in`; this offset is expected for cell-centered sampling on the
strongly graded 60-cell block. No interpolation or smoothing is applied.

The extracted line ranges are:

| Case | Minimum $p/p_{\infty}$ | Maximum $p/p_{\infty}$ |
| --- | ---: | ---: |
| `sonicFoam` | 0.66643 | 1.02837 |
| `rhoCentralFoam` | 0.24249 | 1.02067 |
| `rhoPimpleFoam` | 0.32266 | 1.02187 |

Files in the post-processing directory are:

| File | Purpose |
| --- | --- |
| `extract_pressure_ratio.py` | ParaView Python reader and lower-cell-row extractor |
| `plot_pressure_ratio.py` | Matplotlib comparison plot generator |
| `Allrun` | Runs extraction and plotting in sequence |
| `pressure_ratio_sonicFoam.csv` | Raw sonicFoam samples |
| `pressure_ratio_rhoCentralFoam.csv` | Raw rhoCentralFoam samples |
| `pressure_ratio_rhoPimpleFoam.csv` | Raw rhoPimpleFoam samples |
| `pressure_ratio_comparison.png` | Final three-case comparison figure |

The extractor creates a temporary `.OpenFOAM` marker inside each case only
while ParaView reads it and removes the marker afterward. To reproduce the
data and figure from this root directory:

```bash
./case4_1_postProcessing/Allrun
```

## Reproducing a solver case

Load the OpenFOAM Foundation 13 environment and run one case at a time:

```bash
. /opt/openfoam13/etc/bashrc
cd case4_1_rhoPimpleFoam
./Allrun
```

Do not run `Allclean` unless the generated mesh, logs, time directories, and
post-processing data are intentionally being removed. The initial-condition
files can be restored from `0/backup/` if a fresh pre-`setFields` state is
needed.
