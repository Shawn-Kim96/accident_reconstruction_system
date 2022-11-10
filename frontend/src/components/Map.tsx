import React, { useEffect, useRef } from 'react';

import { Map as Mapbox } from 'react-map-gl';
import type { MapRef } from 'react-map-gl';

const MAPBOX_TOKEN = 'pk.eyJ1IjoibXllb25na29va2tpbSIsImEiOiJjbDVxYW4zc2QweTE4M2pwY2ZxMjYxMDE5In0.l7Ji8j6Yvl80Y_OYHNgOng';

type Props = {}

// eslint-disable-next-line no-empty-pattern
const Map: React.FC<Props> = ({}) => {
  const mapContainer = useRef<MapRef>(null);

  useEffect(() => {
    // map.current.on('idle',function(){
    //   map.current.resize()
    // })
  }, []);

  return (
    <Mapbox
      initialViewState={{
        latitude: 40.67,
        longitude: -103.59,
        zoom: 3,
      }}
      mapStyle='mapbox://styles/mapbox/dark-v9'
      mapboxAccessToken={MAPBOX_TOKEN}
      ref={mapContainer}
    />
  // <div ref={mapContainer} className='map-container' style={{ width: '100%', height: '100%' }} />
  );
};

export default Map;
