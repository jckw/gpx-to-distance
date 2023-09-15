from flask import Flask, request, render_template, redirect, url_for
import gpxpy
import gpxpy.gpx

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("upload_form.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    gpx = gpxpy.parse(file.read().decode("utf-8"))

    total_distance = 0
    total_elevation_gain = 0
    prev_point = None
    prev_elevation = None

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if prev_point is not None:
                    total_distance += point.distance_3d(prev_point)

                if prev_elevation is not None and point.elevation > prev_elevation:
                    total_elevation_gain += point.elevation - prev_elevation

                prev_point = point
                prev_elevation = point.elevation

    total_distance_km = total_distance / 1000
    total_elevation_gain_m = total_elevation_gain
    hiking_time_hours = total_distance_km / 5 + total_elevation_gain_m / 300

    return render_template(
        "results.html",
        distance=total_distance_km,
        elevation_gain=total_elevation_gain_m,
        hiking_time=hiking_time_hours,
    )
