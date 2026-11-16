#!/usr/bin/env pvpython

import csv
from pathlib import Path

from paraview import servermanager
from paraview.simple import Delete, OpenFOAMReader


P_INFINITY = 15350.0
STEP_X = 0.0
OUTLET_X = 0.3048

CASES = (
    ("case4_1_sonicFoam", "sonicFoam"),
    ("case4_1_rhoCentralFoam", "rhoCentralFoam"),
    ("case4_1_rhoPimpleFoam", "rhoPimpleFoam"),
)


def leaf_datasets(data_object):
    if data_object.IsA("vtkDataSet"):
        yield data_object
        return

    iterator = data_object.NewIterator()
    iterator.VisitOnlyLeavesOn()
    iterator.SkipEmptyNodesOn()
    iterator.InitTraversal()
    while not iterator.IsDoneWithTraversal():
        leaf = iterator.GetCurrentDataObject()
        if leaf is not None and leaf.IsA("vtkDataSet"):
            yield leaf
        iterator.GoToNextItem()


def cell_center(dataset, cell_id):
    cell = dataset.GetCell(cell_id)
    point_ids = cell.GetPointIds()
    count = point_ids.GetNumberOfIds()
    coordinates = [0.0, 0.0, 0.0]
    for index in range(count):
        point = dataset.GetPoint(point_ids.GetId(index))
        for component in range(3):
            coordinates[component] += point[component]
    return tuple(value / count for value in coordinates)


def extract_case(case_dir, output_path):
    marker = case_dir / "pressure-ratio.OpenFOAM"
    marker_created = not marker.exists()
    if marker_created:
        marker.touch()

    reader = None
    try:
        reader = OpenFOAMReader(FileName=str(marker))
        reader.UpdatePipelineInformation()
        reader.MeshRegions = ["internalMesh"]
        reader.CellArrays = ["p"]

        times = [float(value) for value in reader.TimestepValues]
        if not times:
            raise RuntimeError("No result time directories were found in {}".format(case_dir))
        latest_time = max(times)
        reader.UpdatePipeline(time=latest_time)

        fetched = servermanager.Fetch(reader)
        cells = []
        for dataset in leaf_datasets(fetched):
            pressure = dataset.GetCellData().GetArray("p")
            if pressure is None:
                continue
            for cell_id in range(dataset.GetNumberOfCells()):
                x, y, z = cell_center(dataset, cell_id)
                if STEP_X <= x <= OUTLET_X and y < 0.0:
                    cells.append((x, y, z, float(pressure.GetTuple1(cell_id))))

        if not cells:
            raise RuntimeError("No downstream cells below the step plane were found in {}".format(case_dir))

        sample_y = max(cell[1] for cell in cells)
        y_tolerance = max(1.0e-12, abs(sample_y) * 1.0e-6)
        samples = sorted(
            (cell for cell in cells if abs(cell[1] - sample_y) <= y_tolerance),
            key=lambda cell: cell[0],
        )
        if not samples:
            raise RuntimeError("The lower cell row could not be isolated in {}".format(case_dir))

        with output_path.open("w", newline="", encoding="ascii") as handle:
            writer = csv.writer(handle)
            writer.writerow(("x_m", "x_in", "y_m", "p_Pa", "p_over_p_infinity", "time_s"))
            for x, y, _z, pressure in samples:
                writer.writerow(
                    (
                        "{:.12g}".format(x - STEP_X),
                        "{:.12g}".format((x - STEP_X) / 0.0254),
                        "{:.12g}".format(y),
                        "{:.12g}".format(pressure),
                        "{:.12g}".format(pressure / P_INFINITY),
                        "{:.12g}".format(latest_time),
                    )
                )

        return latest_time, sample_y, len(samples)
    finally:
        if reader is not None:
            Delete(reader)
        if marker_created and marker.exists():
            marker.unlink()


def main():
    post_dir = Path(__file__).resolve().parent
    root_dir = post_dir.parent

    for case_name, output_name in CASES:
        case_dir = root_dir / case_name
        if not case_dir.is_dir():
            raise RuntimeError("Missing case directory: {}".format(case_dir))
        output_path = post_dir / "pressure_ratio_{}.csv".format(output_name)
        latest_time, sample_y, sample_count = extract_case(case_dir, output_path)
        print(
            "{}: wrote {} samples at t={:.7g} s and y={:.12g} m to {}".format(
                case_name, sample_count, latest_time, sample_y, output_path.name
            )
        )


if __name__ == "__main__":
    main()
