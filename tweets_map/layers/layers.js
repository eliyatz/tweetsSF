var wms_layers = [];

        var lyr_WikimediaMap_0 = new ol.layer.Tile({
            'title': 'Wikimedia Map',
            'type': 'base',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
    attributions: '<a href=""></a>',
                url: 'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png'
            })
        });var format_my_tweets21_1 = new ol.format.GeoJSON();
var features_my_tweets21_1 = format_my_tweets21_1.readFeatures(json_my_tweets21_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_my_tweets21_1 = new ol.source.Vector({
    attributions: '<a href=""></a>',
});
jsonSource_my_tweets21_1.addFeatures(features_my_tweets21_1);var lyr_my_tweets21_1 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_my_tweets21_1, 
                style: style_my_tweets21_1,
    title: 'my_tweets2 (1)<br />\
    <img src="styles/legend/my_tweets21_1_0.png" /> negative<br />\
    <img src="styles/legend/my_tweets21_1_1.png" /> neutral<br />\
    <img src="styles/legend/my_tweets21_1_2.png" /> positive<br />\
    <img src="styles/legend/my_tweets21_1_3.png" /> <br />'
        });

lyr_WikimediaMap_0.setVisible(true);lyr_my_tweets21_1.setVisible(true);
var layersList = [lyr_WikimediaMap_0,lyr_my_tweets21_1];
lyr_my_tweets21_1.set('fieldAliases', {'id': 'id', 'text': 'text', 'RT': 'RT', 'geotag': 'geotag', 'time': 'time', 'TextBlob - certainty': 'TextBlob - certainty', 'TextBlob - decision': 'TextBlob - decision', 'lat': 'lat', 'lon': 'lon', });
lyr_my_tweets21_1.set('fieldImages', {'id': 'TextEdit', 'text': 'TextEdit', 'RT': 'TextEdit', 'geotag': 'TextEdit', 'time': 'TextEdit', 'TextBlob - certainty': 'TextEdit', 'TextBlob - decision': 'TextEdit', 'lat': 'TextEdit', 'lon': 'TextEdit', });
lyr_my_tweets21_1.set('fieldLabels', {'id': 'no label', 'text': 'header label', 'RT': 'no label', 'geotag': 'no label', 'time': 'header label', 'TextBlob - certainty': 'header label', 'TextBlob - decision': 'header label', 'lat': 'no label', 'lon': 'no label', });
lyr_my_tweets21_1.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});