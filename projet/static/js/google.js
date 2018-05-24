var map;

function initialize() {

    var mapOptions = {
        center: new google.maps.LatLng(-34.397, 150.644),
        zoom: 8
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    var drawingManager = new google.maps.drawing.DrawingManager({

        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: [google.maps.drawing.OverlayType.POLYGON]
        },
        polygonOptions: {
            strokeWeight: 1,
            strokeColor: '#ff0000',
        }
    });

    drawingManager.setMap(map);

    google.maps.event.addListener(drawingManager, 'overlaycomplete', function (event) {

        // Get overlay paths
        var paths = event.overlay.getPaths();
        
        // Remove overlay from map
        event.overlay.setMap(null);
        
        // Disable drawingManager
        drawingManager.setDrawingMode(null);

        // Create Polygon
        createPolygon(paths);
    });
}

function createPolygon(paths) {
    
    var polygon = new google.maps.Polygon({
        fillColor: '#ffff00',
        fillOpacity: 1,
        strokeWeight: 1,
        strokeColor: '#0000ff',
        editable: true,
        draggable: true,
        paths: paths,
        map: map
    });
}
function importerPolygones() {
    var allVals = [];
    $.each($("input[name='checkbox']:checked"), function() {
        allVals.push($(this).val());
    });
    $.ajax({
        url: url_importer_polygone,
        type: "POST",
        data: {
            id: allVals,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(json) {
            json = JSON.parse(json);
            map.data.addGeoJson(json);
        },
        error: function(xhr, errmsg, err) {
            alert("Error: " + xhr.status + ": " + err);
        }
    });
}

google.maps.event.addDomListener(document.getElementById('supprimer'), 'click', deleteSelectedShape);
    google.maps.event.addDomListener(document.getElementById('suivant'), 'click', function() {});
initialize();

btnImporter=document.getElementById('importer-button');
if (btnImporter) {google.maps.event.addDomListener(btnImporter, 'click', importerPolygones);}
google.maps.Map.prototype.getGeoJson = function(callback) {

    var geo = {
                "type": "FeatureCollection",
                "features": []
            }
 fxShapes = function(vertices) {
                var that = [];
                for (var i = 0; i < vertices.getLength(); ++i) {
                    that.push([vertices.getAt(i).lng(), vertices.getAt(i).lat()]);
                }
                if (that[0] !== that[that.length - 1]) {
                    that.push([that[0][0], that[0][1]]);
                }
                return that;
            }
 fx = function(g, t) {

                var that = [],
                    arr,
                    f = {
                        MultiLineString: 'LineString',
                        LineString: 'Point',
                        MultiPolygon: 'Polygon',
                        Polygon: 'LinearRing',
                        LinearRing: 'Point',
                        MultiPoint: 'Point'
                    };

                switch (t) {
                    case 'Point':
                        g = (g.get) ? g.get() : g;
                        return ([g.lng(), g.lat()]);
                        break;
                    default:
                        arr = g.getArray();
                        for (var i = 0; i < arr.length; ++i) {
                            that.push(fx(arr[i], f[t]));
                        }
                        if (t == 'LinearRing' &&
                            that[0] !== that[that.length - 1]) {
                            that.push([that[0][0], that[0][1]]);
                        }
                        return that;
                }
            };
 this.data.forEach(function(feature) {
            var _feature = {
                type: 'Feature',
                properties: {}
            }
            _id = feature.getId(),
                _geometry = feature.getGeometry(),
                _type = _geometry.getType(),
                _coordinates = fx(_geometry, _type);

            _feature.geometry = {
                type: _type,
                coordinates: _coordinates
            };
            if (typeof _id === 'string') {
                _feature.id = _id;
            }

            geo.features.push(_feature);
            feature.forEachProperty(function(v, k) {
                _feature.properties[k] = v;
            });
        });

shapes.forEach(function(shape) {
            var _feature = {
                type: 'Feature',
                properties: {}
            }
            _geometry = shape.getPath(),
                _type = shape.type,
                _coordinates = fxShapes(_geometry, _type);

            _feature.geometry = {
                type: _type,
                coordinates: [_coordinates]
            };
            if (typeof _id === 'string') {
                _feature.id = _id;
            }
            geo.features.push(_feature);
        });
        if (typeof callback === 'function') {
            callback(geo);
        }
        return geo;
    

}
google.maps.event.addDomListener(document.getElementById('supprimer'), 'click', deleteSelectedShape);
google.maps.event.addDomListener(document.getElementById('suivant'), 'click', function() {
        map.getGeoJson(function(geo) {
            if (geo['features'].length!=0) {
                $.ajax({
                    url: url_sauvegarder_polygone,
                    type: "POST",
                    data: {
                        geojson: JSON.stringify(geo),
                        csrfmiddlewaretoken: csrf_token
                    },
                    success: function(reponse) {
                        window.location.href = reponse;
                    },
                    error: function(xhr, errmsg, err) {
                        alert("Error: " + xhr.status + ": " + err);
                    }
                });
            } else {alert('Selectionner votre parcelle!')}
        });
});
