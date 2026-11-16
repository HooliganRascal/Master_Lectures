# OpenFOAM.org Case Setup and Adjustment Workflow

## Scope and Distribution

This guide is for the OpenFOAM Foundation distribution from
[openfoam.org](https://openfoam.org/). The present case was configured and
validated with OpenFOAM 13. Do not assume that dictionary names, solver names,
boundary conditions, or utility syntax from OpenFOAM.com/ESI releases are
interchangeable with this distribution.

For OpenFOAM 13, many former standalone solvers are modules selected through
`foamRun`. This case therefore uses:

```foam
application     foamRun;
solver          fluid;
```

This is the OpenFOAM 13 replacement for running the former standalone
`rhoPimpleFoam` executable directly.

## Validated Case Summary

This folder contains a two-dimensional, compressible, turbulent
backward-facing-step case.

### Geometry and Mesh

- Flow direction: positive $x$ direction
- Empty direction: $z$
- Mesh size: 5,940 hexahedral cells
- Patches: `inlet`, `outlet`, `upperWall`, `lowerWall`, and `frontAndBack`
- `frontAndBack` is `empty`, so the solution directions are $(x,y)$ only
- `blockMeshDict` uses `convertToMeters 0.001`
- Mesh non-orthogonality is zero
- The full mesh check reports 44 highly graded cells with determinant below
  `0.001`; the minimum determinant is about `4.04e-5` and the maximum aspect
  ratio is about `499.5`

The mesh warning did not destabilize the completed run, but it remains a
quantitative-accuracy concern when interpreting wall gradients and turbulence
near the step.

### Physical Models

The case uses [thermophysicalProperties](constant/thermophysicalProperties)
with:

- `hePsiThermo`
- `perfectGas`
- `hConst`
- `sensibleInternalEnergy`
- Molecular weight `28.96`
- $C_{p}=1004.5\ \mathrm{J/(kg\,K)}$
- Dynamic viscosity $\mu=1.827\times10^{-5}\ \mathrm{Pa\,s}$
- Prandtl number $Pr=0.71$

The momentum model in [momentumTransport](constant/momentumTransport) is RAS
`kEpsilon` with Newtonian viscosity.

### Thermodynamically Consistent Initialization

For the configured perfect gas,

$$
R=\frac{8314.4626}{28.96}=287.1016\ \mathrm{J/(kg\,K)}
$$

Pressure, density, and temperature must satisfy

$$
p=\rho R T
$$

The corrected initialization in
[setFieldsDict](system/setFieldsDict) is:

| Region | $p$ (Pa) | $T$ (K) | $\rho$ ($\mathrm{kg/m^{3}}$) | $U$ ($\mathrm{m/s}$) |
| --- | ---: | ---: | ---: | --- |
| Upstream/left | 15,350 | 169.2 | 0.3159893 | $(651.9,0,0)$ |
| Downstream above step | 13,448.99 | 153 | 0.30617 | $(619.9,0,0)$ |
| Downstream behind step | 13,448.99 | 153 | 0.30617 | $(0,0,0)$ |

Two errors originally caused the solver to fail:

- The internal compressible pressure was `1e-5 Pa`, although $\rho R T$
  required approximately `13448.99 Pa`.
- Velocity was specified as $(0,0,U)$ even though $z$ is the empty direction.
  This produced no inlet-to-outlet mass flux. It must be $(U,0,0)$.

The inconsistent state produced large continuity errors, negative turbulent
kinetic energy, and finally `Negative initial temperature T0` at the second
pseudo-time step.

### Turbulence Fields

The inlet values are:

- $k=0.375\ \mathrm{m^{2}/s^{2}}$
- $\epsilon=14.855\ \mathrm{m^{2}/s^{3}}$

The configured boundary conditions are:

- `k`: fixed inlet value, `zeroGradient` outlet, `kqRWallFunction` on walls
- `epsilon`: fixed inlet value, `zeroGradient` outlet,
  `epsilonWallFunction` on walls
- `nut`: `calculated` at inlet/outlet and `nutkWallFunction` on walls
- `alphat`: `calculated` at inlet/outlet and
  `compressible::alphatWallFunction` on walls
- All four fields use `empty` on `frontAndBack`

When turbulence values are not prescribed by the problem, estimate them from
turbulence intensity $I$ and mixing length $\ell$:

$$
k=\frac{3}{2}(I|U|)^{2}
$$

$$
\epsilon=C_{\mu}^{3/4}\frac{k^{3/2}}{\ell}
$$

### Numerical Configuration

[fvSchemes](system/fvSchemes) uses local time stepping with conservative
upwind convection during robust startup. For OpenFOAM 13 compressible flow,
the viscous divergence scheme is keyed as:

```foam
div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;
```

[fvSolution](system/fvSolution) uses:

- `PBiCGStab` with `DILU` for pressure, velocity, energy, $k$, and $\epsilon$
- Pressure and transported-field absolute tolerance `1e-8`
- Two PIMPLE outer correctors and two pressure correctors
- Zero non-orthogonal correctors because the mesh is orthogonal
- Transonic pressure treatment
- `maxCo 0.5`
- Local-time-step smoothing `0.1` and damping `0.9`

`Tmin` and `Tmax` entries inside `PIMPLE` are not temperature constraints in
OpenFOAM 13. If deliberate hard limits are required, define a
`limitTemperature` constraint in `system/fvConstraints`. Do not use a limiter
to hide inconsistent initial thermodynamic data.

### Validated Result

The corrected case completed all 40,000 pseudo-time steps with exit code zero
in about 470 seconds. The log contains no fatal errors, negative-field
bounding, NaNs, or floating-point exceptions. Terminal residuals and local
continuity errors are approximately `1e-8`.

Selected final internal ranges are:

| Field | Minimum | Maximum |
| --- | ---: | ---: |
| $T$ (K) | 99.6884 | 380.684 |
| $p$ (Pa) | 562.873 | 15,786.3 |
| $\rho$ ($\mathrm{kg/m^{3}}$) | 0.00996182 | 0.31931 |
| $|U|$ ($\mathrm{m/s}$) | 0.492 | 749.887 |
| $k$ ($\mathrm{m^{2}/s^{2}}$) | 0.175451 | 38,986.4 |

Numerical completion does not by itself validate the physical model. Compare
pressure recovery, separation length, wall treatment, mesh sensitivity, and
turbulence quantities against the intended experiment or benchmark.

## Reusable OpenFOAM.org Workflow

### 1. Identify the Installation Before Editing

Confirm the Foundation distribution and version first:

```bash
foamVersion
echo "$WM_PROJECT_VERSION"
command -v blockMesh
command -v foamRun
```

If the environment is not loaded, a typical OpenFOAM 13 installation uses:

```bash
. /opt/openfoam13/etc/bashrc
```

Do not mix tutorials or syntax from another OpenFOAM distribution without
checking the version-specific implementation.

### 2. Define the Physics and Coordinate System

Before writing dictionaries, record:

- Compressible or incompressible formulation
- Steady, transient, or local-time-stepping solution
- Laminar, RAS, or LES turbulence model
- Energy and equation-of-state model
- SI units used by the solver
- Physical flow direction and mesh empty/wedge directions
- Inlet, outlet, wall, symmetry, cyclic, and empty patches
- Reference quantities such as $p_{\infty}$, $T_{\infty}$, and $U_{\infty}$

Check vector components against patch normals. A large velocity in an empty
direction is not a valid two-dimensional through-flow condition.

### 3. Create the Standard Case Structure

```text
case/
|-- 0/
|   |-- U
|   |-- p
|   `-- model-dependent fields
|-- constant/
|   |-- momentumTransport
|   |-- thermophysicalProperties
|   `-- physicalProperties as required
|-- system/
|   |-- blockMeshDict
|   |-- controlDict
|   |-- fvSchemes
|   |-- fvSolution
|   `-- setFieldsDict as required
`-- Allclean
```

Use the exact field names and dimensions expected by the selected OpenFOAM.org
solver module.

### 4. Build and Audit the Mesh

```bash
blockMesh
checkMesh
checkMesh -allGeometry -allTopology
```

Verify:

- Bounding box and unit conversion
- Cell count and region count
- Patch names and patch types
- Empty and active solution directions
- Cell volumes, openness, skewness, non-orthogonality, determinants, aspect
  ratios, interpolation weights, and volume ratios

`blockMesh` returning zero only confirms mesh construction. It does not mean
all geometry and quality checks passed.

### 5. Configure Initial and Boundary Fields

For every field:

- Confirm its dimensions
- Provide every mesh patch exactly once
- Use `empty` consistently on two-dimensional empty patches
- Use fixed inlet data when all characteristics enter the domain
- Use outlet conditions appropriate to subsonic or supersonic flow
- Apply turbulence and thermal wall functions consistently with wall patches

For compressible perfect-gas cases, calculate $p$, $\rho$, and $T$ together.
OpenFOAM compressible pressure is absolute thermodynamic pressure, not an
incompressible kinematic pressure or an arbitrary gauge-pressure placeholder.

### 6. Configure `constant/`

Ensure the turbulence model and required fields agree. For example, RAS
`kEpsilon` requires at least `k`, `epsilon`, and `nut`; compressible turbulent
heat transfer also requires `alphat`.

For thermodynamics, verify that the chosen combination of `type`, `transport`,
`thermo`, `equationOfState`, and `energy` is supported by the installed
OpenFOAM.org version.

### 7. Configure `system/`

In `controlDict`:

- Select the correct `foamRun` solver module
- Choose startup and restart behavior deliberately
- Set time-step or pseudo-time limits and write frequency
- Consider disk consumption from `writeInterval`, `purgeWrite`, compression,
  and ASCII/binary format

In `fvSchemes`:

- Start difficult compressible cases with bounded, conservative schemes
- Supply every divergence key requested by the solver and turbulence model
- Use higher-order schemes only after the baseline case is stable and verified

In `fvSolution`:

- Match solver entries to all solved fields and their `Final` variants
- Select symmetric or asymmetric linear solvers appropriately
- Set PIMPLE/SIMPLE correctors according to mesh quality and physics
- Configure local-time-step smoothing and damping when using `localEuler`
- Treat missing convergence criteria as an intentional fixed-iteration choice,
  not automatically as a fatal error

### 8. Initialize Structured Regions

OpenFOAM 13 `setFields` uses `defaultValues` and `zones`. Zone coordinates are
in the final mesh coordinate system. If `blockMeshDict` uses
`convertToMeters`, do not reuse unscaled millimetre coordinates in
`setFieldsDict`.

Run:

```bash
setFields
```

Then verify the number of cells and unique values assigned to each region.
Successful parsing does not prove that a box selected the intended cells.

`setFields` rewrites files in `0/`. Keep clean initial templates in `0.orig/`
or another deliberate source directory if repeated clean initialization is
required. A typical `cleanCase` call does not restore fields modified by
`setFields`.

### 9. Run in Diagnostic Stages

Use this order:

```bash
./Allclean
blockMesh
checkMesh -allGeometry -allTopology
setFields
foamRun > log.foamRun 2>&1
```

During startup, inspect the log for:

```bash
tail -f log.foamRun
rg "FOAM FATAL|FOAM Warning|bounding|Negative|nan|Floating point" log.foamRun
```

First establish that several steps complete with positive, finite fields.
Then run a meaningful convergence interval. Finally, inspect residual trends,
continuity errors, field extrema, conservation, and benchmark quantities.

### 10. Diagnose the First Cause, Not Only the Fatal Message

Common failure chains include:

- `Negative initial temperature`: first check absolute pressure, density,
  temperature, velocity direction, energy data, and the preceding residuals
- Negative or bounded $k$/$\epsilon$: check inlet values, wall functions,
  mesh resolution, time step, and convection schemes
- Missing discretization entry: copy the exact requested operator name from
  the fatal message and compare with a tutorial for the same OpenFOAM.org
  version
- Patch-field mismatch: compare `constant/polyMesh/boundary` against every
  file in `0/`
- Immediate pressure divergence: check reference pressure, compressibility,
  inlet/outlet characteristics, and thermodynamic consistency
- Stable residuals but implausible results: check units, coordinate direction,
  reference values, sampling location, mesh sensitivity, and physical boundary
  conditions

Change one causal group at a time and rerun from a known initial state. A
temperature or pressure limiter can prevent an abort while preserving a wrong
model, so it is not a substitute for diagnosis.

### 11. Post-Process Reproducibly

Create a ParaView marker with:

```bash
paraFoam -touch
```

For this case, [make_paraview_plots.py](make_paraview_plots.py) generates:

- [RPPF_visualization.pvsm](RPPF_visualization.pvsm)
- [velocity_vectors.png](velocity_vectors.png)
- [pressure_ratio_vs_x.png](pressure_ratio_vs_x.png)
- [pressure_ratio_vs_x.csv](pressure_ratio_vs_x.csv)

Run it with:

```bash
pvpython make_paraview_plots.py
```

The pressure plot currently samples the horizontal line at
$y=0.07375\ \mathrm{m}=2.9035\ \mathrm{in}$, uses
$p_{\infty}=15350\ \mathrm{Pa}$, and plots $x$ from `-4` to `12 in`. This is a
mid-channel trace, not a wall-pressure distribution. Change `SAMPLE_Y` and
`P_INFINITY` at the top of the script when the requested reference or sampling
location differs.

## Completion Checklist

- [ ] OpenFOAM Foundation/openfoam.org version identified
- [ ] Solver module and required fields confirmed for that version
- [ ] Mesh axes, units, patches, and quality checked
- [ ] Every boundary field matches the mesh patches
- [ ] Compressible $p$, $\rho$, and $T$ satisfy the equation of state
- [ ] Velocity components align with active mesh directions
- [ ] Turbulence inlet values and wall functions are physically justified
- [ ] `setFields` zones use mesh units and select the intended cells
- [ ] Conservative baseline schemes run without bounding or fatal errors
- [ ] Residuals, continuity, and field extrema are checked through convergence
- [ ] Results are compared with physical expectations or benchmark data
- [ ] ParaView state, plots, sampling definitions, and reference values are
  reproducible
