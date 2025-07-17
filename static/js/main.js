document.addEventListener("DOMContentLoaded", function(){
    var countryElement = document.getElementById("latlng_country");
    var countryData = countryElement ? JSON.parse(countryElement.textContent) : null;
    
    var countriesElement = document.getElementById("countries");
    var visitedCountries = countriesElement ? JSON.parse(countriesElement.textContent) : null;

    // Single country page
    if(countryData){
        var country_map = L.map('country-map').setView([countryData.capitalInfo.latlng[0], countryData.capitalInfo.latlng[1]], 7);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(country_map);

        // Añadir marcador
        L.marker([countryData.capitalInfo.latlng[0], countryData.capitalInfo.latlng[1]]).addTo(country_map)
            .bindPopup('<b>' + countryData.name.common + '</b><br>Capital: ' + countryData.capital)
            .openPopup();
    }

    // Visualize page
    if(visitedCountries){
        var world_map = L.map('visualize-map').setView([20, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(world_map);

        fetch(geojson_url)
            .then(response => response.json())
            .then(geoData => {
                L.geoJSON(geoData, {
                    filter: function(feature) {
                        return visitedCountries.includes(feature.properties.iso_a3);
                    },
                    style: {
                        fillColor: "green",
                        weight: 1,
                        opacity: 1,
                        color: "white",
                        fillOpacity: 0.7
                    },
                    onEachFeature: function (feature, layer) {
                        layer.on('click', function () {
                            layer.bindPopup("<strong>" + feature.properties.name + "</strong>").openPopup();
                        });
                    }
                }).addTo(world_map);
            })
            .catch(error => console.error("Error cargando el GeoJSON:", error));
    }
})