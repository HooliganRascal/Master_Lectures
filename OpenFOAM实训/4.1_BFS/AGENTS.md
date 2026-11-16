# AGENTS.md

## OpenFOAM Case Work

When asked to build, configure, adjust, diagnose, run, or post-process an
OpenFOAM case in this directory, read
[`OPENFOAM_CASE_WORKFLOW.md`](OPENFOAM_CASE_WORKFLOW.md) completely before
making changes.

Treat the case as OpenFOAM Foundation from openfoam.org unless the user clearly
specifies another distribution. Confirm the installed version before selecting
solver names, dictionary syntax, boundary conditions, or tutorial references;
do not silently mix OpenFOAM.org and OpenFOAM.com/ESI conventions.

Use the workflow document as guidance, then validate all values against the
specific geometry, physics, units, boundary conditions, and requested outputs
of the current case. Do not copy this case's numerical values into another case
without that validation.
