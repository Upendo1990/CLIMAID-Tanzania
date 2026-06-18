
// CLIMAID Tanzania District Climate Export
// Google Earth Engine script template

var districts = ee.FeatureCollection("FAO/GAUL/2015/level2")
  .filter(ee.Filter.eq("ADM0_NAME", "United Republic of Tanzania"));

var startYear = 2001;
var endYear = 2024;
var years = ee.List.sequence(startYear, endYear);

var chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY");
var ndviCol = ee.ImageCollection("MODIS/061/MOD13Q1").select("NDVI");
var lstCol = ee.ImageCollection("MODIS/061/MOD11A2").select("LST_Day_1km");

function scaleNDVI(img) {
  return img.multiply(0.0001).copyProperties(img, ["system:time_start"]);
}

function scaleLST(img) {
  return img.multiply(0.02).subtract(273.15).copyProperties(img, ["system:time_start"]);
}

ndviCol = ndviCol.map(scaleNDVI);
lstCol = lstCol.map(scaleLST);

var annual = ee.ImageCollection.fromImages(
  years.map(function(y) {
    y = ee.Number(y);
    var start = ee.Date.fromYMD(y, 1, 1);
    var end = ee.Date.fromYMD(y, 12, 31);

    var rainfall = chirps.filterDate(start, end).sum().rename("Rainfall");
    var ndvi = ndviCol.filterDate(start, end).mean().rename("NDVI");
    var temp = lstCol.filterDate(start, end).mean().rename("Temperature");

    return rainfall.addBands(temp).addBands(ndvi)
      .set("Year", y)
      .set("system:time_start", start.millis());
  })
);

var table = annual.map(function(img) {
  var year = img.get("Year");

  var stats = img.reduceRegions({
    collection: districts,
    reducer: ee.Reducer.mean(),
    scale: 5000,
    tileScale: 4
  });

  return stats.map(function(f) {
    return f.set("Year", year);
  });
}).flatten();

Export.table.toDrive({
  collection: table,
  description: "CLIMAID_Tanzania_District_Climate_2001_2024",
  fileFormat: "CSV"
});
