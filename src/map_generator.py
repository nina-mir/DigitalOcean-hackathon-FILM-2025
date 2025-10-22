# src/map_generator.py
import folium
import pandas as pd
from typing import List, Dict, Any


class MapGenerator:
    """
    Simple point map generator for SF film locations.
    Only creates maps - doesn't analyze or interpret data.
    """
    
    def __init__(self):
        self.default_center = [37.7749, -122.4194]  # SF coordinates
    
    def create_point_map(self, location_data: List[Dict], 
                     title: str = "SF Film Locations") -> folium.Map:
        """Create point map, combining duplicate locations"""
        if not location_data:
            return self._create_empty_map(title)
        
        sf_center = [37.7749, -122.4194]
        m = folium.Map(location=sf_center, zoom_start=13)
        
        # 🔧 GROUP by location name to handle duplicates
        from collections import defaultdict
        grouped_locations = defaultdict(list)
        
        for loc_data in location_data:
            loc_name = loc_data['location_name']
            grouped_locations[loc_name].append(loc_data)
        
        # Add markers (one per unique location)
        for loc_name, loc_list in grouped_locations.items():
            # Use first entry's geometry (they should all be the same)
            geom = loc_list[0]['geometry']
            
            # Build popup with ALL films at this location
            popup_html = f"<b>{loc_name}</b><br><br>"
            
            if len(loc_list) > 1:
                popup_html += f"<b>🎬 Featured in {len(loc_list)} films:</b><br><br>"
            
            for i, loc_data in enumerate(loc_list, 1):
                metadata = loc_data.get('metadata', {})
                
                # Add film info
                if len(loc_list) > 1:
                    popup_html += f"<b>Film {i}:</b> "
                
                film = metadata.get('Film', 'Unknown')
                popup_html += f"{film}<br>"
                
                # Add other metadata (excluding Locations to avoid redundancy)
                for key, val in metadata.items():
                    if key == 'Film' or key == 'Locations':
                        continue
                    if val is None or (not isinstance(val, list) and pd.isna(val)):
                        continue
                        
                    if isinstance(val, list):
                        if val:
                            display_val = ', '.join(str(v) for v in val)
                            display_key = key.replace('_', ' ').title()
                            popup_html += f"<b>{display_key}:</b> {display_val}<br>"
                    elif val != '' and val != 'None':
                        display_key = key.replace('_', ' ').title()
                        popup_html += f"<b>{display_key}:</b> {val}<br>"
                
                if i < len(loc_list):
                    popup_html += "<br>"  # Space between films
            
            # Choose icon color based on number of films
            if len(loc_list) > 1:
                icon_color = 'blue'  # Multiple films = blue
            else:
                icon_color = 'red'   # Single film = red
            
            folium.Marker(
                location=[geom.y, geom.x],
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=f"{loc_name} ({len(loc_list)} film{'s' if len(loc_list) > 1 else ''})",
                icon=folium.Icon(color=icon_color, icon='film', prefix='fa')
            ).add_to(m)
        
        # Update title to show unique locations
        title_html = f'''
        <div style="position: fixed; 
                    top: 10px; left: 50px; right: 50px; 
                    z-index:9999; 
                    background-color:white;
                    border:2px solid grey;
                    border-radius: 5px;
                    padding: 10px;
                    text-align: center;">
            <h3 style="margin:0;">{title}</h3>
            <p style="margin:5px 0 0 0; font-size:14px; color:#666;">
                {len(grouped_locations)} unique location{'' if len(grouped_locations) == 1 else 's'} 
                • {len(location_data)} total appearance{'' if len(location_data) == 1 else 's'}
            </p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        return m
        
    def _create_empty_map(self, title: str) -> folium.Map:
        """Create fallback map when no locations found"""
        m = folium.Map(location=self.default_center, zoom_start=12)
        
        title_html = f'''
        <div style="position: fixed; 
                    top: 10px; left: 50px; right: 50px; 
                    z-index:9999; 
                    background-color:#fff3cd;
                    border:2px solid #ffc107;
                    border-radius: 5px;
                    padding: 10px;
                    text-align: center;">
            <h3 style="margin:0; color:#856404;">{title}</h3>
            <p style="margin:5px 0 0 0; color:#856404;">No locations found to display</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        return m