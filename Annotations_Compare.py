import pandas as pd
from shapely.geometry import box
import json
from shapely.geometry import Point
from geopy.distance import geodesic


# Read a JSON file containing annotations and return a list of parsed JSON objects
def read_annotation_file(file_path):
    annotation_objects = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                obj = json.loads(line.strip())
                annotation_objects.append(obj)
            except json.JSONDecodeError:
                print(f"JSON decode error：{line}")
    return annotation_objects


# Compare location description annotations for the same message from two annotators to check if they are identical in position, text, category, and spatial footprint.
# Note one message may contain multiple annotations.
def compare_annotations(annotator1_annotations, annotator2_annotations):
    annotator1_sorted = sorted(annotator1_annotations, key=lambda x: x['startIdx'])
    annotator2_sorted = sorted(annotator2_annotations, key=lambda x: x['startIdx'])

    # If the two annotation lists have different lengths, they are not equal
    if len(annotator1_sorted) != len(annotator2_sorted):
        return False

    # Compare each pair of annotations for exact match in indices, text, category, and spatial footprint; return False if any differ.
    for ann1, ann2 in zip(annotator1_sorted, annotator2_sorted):
        if ann1['startIdx'] == ann2['startIdx'] and ann1['endIdx'] == ann2['endIdx'] and ann1['locationDesc'] == ann2[
            'locationDesc'] and ann1['locationCate'] == ann2['locationCate'] and comparingSpatialFootprint(ann1['spatialFootprint'], ann2['spatialFootprint']):
            pass
        else:
            return False

    return True


# Compare two spatial footprint arrays by type and geometry; return True if sufficiently the same.
# Each location can have multiple spatial footprints; thus, the input consists of a list of footprint objects.
def comparingSpatialFootprint(spatialFootprintArray1, spatialFootprintArray2):
    # Return False if the number of spatial footprints differs across the two arrays
    if len(spatialFootprintArray1) != len(spatialFootprintArray2):
        return False

    # Return False if the sets of spatial footprint types are different between the two arrays
    type_s1 = {sf['type'] for sf in spatialFootprintArray1}
    type_s2 = {sf['type'] for sf in spatialFootprintArray2}
    if type_s1 != type_s2:
        return False

    # Compare the spatial footprints based on geometry
    for element in type_s1:
        sFJsonArray1 = []
        sFJsonArray2 = []
        # Flatten the geometries of the current footprint type from both spatial footprint arrays
        for sf in spatialFootprintArray1:
            if sf['type'] == element:
                if isinstance(sf['geometry'], list):
                    sFJsonArray1.extend(sf['geometry'])
                else:
                    sFJsonArray1.append(sf['geometry'])

        for sf in spatialFootprintArray2:
            if sf['type'] == element:
                if isinstance(sf['geometry'], list):
                    sFJsonArray2.extend(sf['geometry'])
                else:
                    sFJsonArray2.append(sf['geometry'])

        # If the spatial footprint is a point, compute their distance
        if element == "Point":
            if len(sFJsonArray1) == 1 and len(sFJsonArray2) == 1:
                point1 = Point(sFJsonArray1[0]['coordinates'])
                point2 = Point(sFJsonArray2[0]['coordinates'])
                coords1 = (point1.y, point1.x)
                coords2 = (point2.y, point2.x)

                distance = geodesic(coords1, coords2).meters
                if distance > 1000:  # If the distance is larger than 1000 meters, they are considered different
                    return False
            elif (len(sFJsonArray1) == 1 or len(sFJsonArray2) == 1) and len(sFJsonArray1) != len(sFJsonArray2):
                return False
            else:
                # Compare the intersection ratio for points (if applicable)
                interRatio = compute_intersection_ratio(sFJsonArray1, sFJsonArray2)
                if interRatio < 0.8:
                    return False
        else:
            # If polyline or polygon, compute the intersection area ratio of their bounding boxes
            interRatio = compute_intersection_ratio(sFJsonArray1, sFJsonArray2)
            if interRatio < 0.8:
                return False

    return True


# Convert coordinates from a GeoJSON spatial footprint object into a list of coordinate tuples.
# Supports GeoJSON types: Point, Polygon, LineString, and MultiLineString.
def create_coordinates_from_geojson(spatial_footprint_obj):
    coordinates_array = []

    # Extract coordinates from GeoJSON object based on its geometry type (Point, Polygon, or others)
    if spatial_footprint_obj['type'] == 'Point':
        coordinates_object = spatial_footprint_obj['coordinates']
        if isinstance(coordinates_object, list):
            coordinates_array.append(coordinates_object)
    elif spatial_footprint_obj['type'] == 'Polygon':
        coordinates_object = spatial_footprint_obj['coordinates']
        if isinstance(coordinates_object, list):
            coordinates_array = coordinates_object[0]
    else:
        coordinates_object = spatial_footprint_obj['coordinates']
        if isinstance(coordinates_object, list):
            coordinates_array = coordinates_object

    coords = []
    for coord in coordinates_array:
        lon, lat = coord[0], coord[1]
        coords.append((lon, lat))

    return coords


# Compute the intersection ratio of bounding boxes enclosing two sets of spatial footprints.
def compute_intersection_ratio(geo_json_array1, geo_json_array2):
    # Create bounding box for the first set of spatial footprints
    combined_coords1 = []
    for sFJsonObject1 in geo_json_array1:
        coords1 = create_coordinates_from_geojson(sFJsonObject1)
        combined_coords1.extend(coords1)

    minX1 = min([coord[0] for coord in combined_coords1])
    minY1 = min([coord[1] for coord in combined_coords1])
    maxX1 = max([coord[0] for coord in combined_coords1])
    maxY1 = max([coord[1] for coord in combined_coords1])

    bounding_box1 = box(minX1, minY1, maxX1, maxY1)
    area1 = bounding_box1.area

    # Create bounding box for the second set of spatial footprints
    combined_coords2 = []
    for sFJsonObject2 in geo_json_array2:
        coords2 = create_coordinates_from_geojson(sFJsonObject2)
        combined_coords2.extend(coords2)

    minX2 = min([coord[0] for coord in combined_coords2])
    minY2 = min([coord[1] for coord in combined_coords2])
    maxX2 = max([coord[0] for coord in combined_coords2])
    maxY2 = max([coord[1] for coord in combined_coords2])

    bounding_box2 = box(minX2, minY2, maxX2, maxY2)
    area2 = bounding_box2.area

    # Calculate the intersection ratio relative to the smaller bounding box area
    intersection = bounding_box1.intersection(bounding_box2)
    area_intersection = intersection.area
    min_area = min(area1, area2)
    inter_ratio = area_intersection / min_area if min_area != 0 else 0

    return inter_ratio


# Compare annotations from two annotators and return only those that differ
def compare_anno_across_annotators(annotation_data, annotator1, annotator2):
    # Group annotation data by tweet ID and annotator, then convert to a DataFrame indexed by tweet ID
    data_dict = {}
    for obj in annotation_data:
        twitter_id = obj.get("id")
        annotator = obj.get("Annotator", "unknown")

        if twitter_id not in data_dict:
            data_dict[twitter_id] = {}  # 初始化内部字典

        data_dict[twitter_id][annotator] = {
            "id": obj.get("id", None),
            "Annotation": obj.get("Annotation", None),
            "text": obj.get("text", None)
        }
    df = pd.DataFrame.from_dict(data_dict, orient="index")
    df.index.name = "id"

    # For each tweet, compare annotations from both annotators and collect those with differences into a new DataFrame.
    filtered_rows = []
    for index, row in df.iterrows():
        new_row = row.copy()
        annotator1_annotations = new_row[annotator1]["Annotation"]
        annotator2_annotations = new_row[annotator2]["Annotation"]

        # Compare annotations from both annotators
        annotation_same = compare_annotations(annotator1_annotations, annotator2_annotations)

        # If annotations differ, filter each annotator’s spatial footprints to keep only 'Point' types, update annotations, and add the row to results
        if not annotation_same:
            updated_annotator1_annotations = []
            updated_annotator2_annotations = []

            for annotator1_annotation in annotator1_annotations:
                spatial_footprints = annotator1_annotation.get("spatialFootprint", [])
                filtered_spatial_footprints = [sf for sf in spatial_footprints if sf.get("type") == "Point"]
                if len(filtered_spatial_footprints) == len(spatial_footprints):
                    annotator1_annotation["spatialFootprint"] = filtered_spatial_footprints
                else:
                    annotator1_annotation.pop("spatialFootprint", None)
                updated_annotator1_annotations.append(annotator1_annotation)

            for annotator2_annotation in annotator2_annotations:
                spatial_footprints = annotator2_annotation.get("spatialFootprint", [])
                filtered_spatial_footprints = [sf for sf in spatial_footprints if sf.get("type") == "Point"]
                if len(filtered_spatial_footprints) == len(spatial_footprints):
                    annotator2_annotation["spatialFootprint"] = filtered_spatial_footprints
                else:
                    annotator2_annotation.pop("spatialFootprint", None)
                updated_annotator2_annotations.append(annotator2_annotation)

            new_row[annotator1]["Annotation"] = updated_annotator1_annotations
            new_row[annotator2]["Annotation"] = updated_annotator2_annotations

            new_row = new_row[[annotator1, annotator2]]
            filtered_rows.append(new_row)

    filtered_df = pd.DataFrame(filtered_rows)

    return filtered_df


def main():
    file_path = ""  # Path to the annotation file downloaded from GALLOC
    annotation_data = read_annotation_file(file_path)
    annotator1 = ""  # Name or identifier for the first annotator
    annotator2 = ""  # Name or identifier for the second annotator
    identified_diff_df = compare_anno_across_annotators(annotation_data, annotator1, annotator2)
    identified_diff_df.to_csv("identified_diff_annotations.csv", index=False)


if __name__ == "__main__":
    main()


