# src/map_generator.py
import folium
import pandas as pd
from typing import List, Dict, Any
from collections import defaultdict


class MapGenerator:
    """
    Simple point map generator for SF film locations.
    Only creates maps - doesn't analyze or interpret data.
    """
    
    def __init__(self):
        self.default_center = [37.7749, -122.4194]  # SF coordinates
    
    def _get_case_insensitive(self, metadata: dict, *keys) -> Any:
        """
        Get value from metadata dict with case-insensitive key matching.
        Tries each provided key in order, checking both as-is and lowercase.
        
        Args:
            metadata: Dictionary to search
            *keys: Key names to try (in order of preference)
            
        Returns:
            First matching value found, or None
        """
        for key in keys:
            # Try exact match first
            if key in metadata:
                return metadata[key]
            # Try lowercase match
            for meta_key, meta_val in metadata.items():
                if meta_key.lower() == key.lower():
                    return meta_val
        return None
    
    def create_point_map(self, location_data: List[Dict], 
                         title: str = "SF Film Locations") -> folium.Map:
        """
        Create a point map from standardized location data.
        Automatically groups duplicate locations and shows all films.
        
        Args:
            location_data: List of dicts with 'location_name', 'geometry', 'metadata'
            title: Map title
            
        Returns:
            folium.Map object
        """
        if not location_data:
            return self._create_empty_map(title)
        
        # Force SF center
        sf_center = [37.7749, -122.4194]
        m = folium.Map(location=sf_center, zoom_start=13)
        
        # 🔧 GROUP by location name to handle duplicates
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
                
                # 🔧 ROBUST: Get title using case-insensitive search
                title_text = self._get_case_insensitive(metadata, 'Title', 'title', 'Film', 'film')
                
                # 🔧 ROBUST: Get year using case-insensitive search
                year = self._get_case_insensitive(metadata, 'Year', 'year')
                
                # Skip this entry if no title found
                if not title_text:
                    # Fallback: if still no title, skip this entry
                    continue
                
                # Format as "Film #: Title (Year)" or just "Title (Year)" for single film
                if len(loc_list) > 1:
                    if year:
                        popup_html += f"<b>Film {i}:</b> {title_text} ({year})<br>"
                    else:
                        popup_html += f"<b>Film {i}:</b> {title_text}<br>"
                else:
                    # Single film - show title directly
                    if year:
                        popup_html += f"<b>Film:</b> {title_text} ({year})<br>"
                    else:
                        popup_html += f"<b>Film:</b> {title_text}<br>"
                
                # Add other metadata (EXCLUDE title/year/film/locations - case insensitive)
                # Build set of keys to exclude by checking case-insensitively
                exclude_patterns = ['title', 'film', 'year', 'locations']
                
                for key, val in metadata.items():
                    # Skip if key matches any exclude pattern (case-insensitive)
                    if key.lower() in exclude_patterns:
                        continue
                        
                    if val is None or (not isinstance(val, list) and pd.isna(val)):
                        continue
                        
                    # Handle lists (like multiple locations)
                    if isinstance(val, list):
                        # Convert list to comma-separated string for display
                        if val:  # Only if list is not empty
                            display_val = ', '.join(str(v) for v in val)
                            display_key = key.replace('_', ' ').title()
                            popup_html += f"<b>{display_key}:</b> {display_val}<br>"
                    # Handle scalar values
                    elif val != '' and val != 'None':
                        display_key = key.replace('_', ' ').title()
                        popup_html += f"<b>{display_key}:</b> {val}<br>"
                
                # Add spacing between films (but not after the last one)
                if i < len(loc_list):
                    popup_html += "<br>"
            
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
        
        # Update title to show unique locations vs total appearances
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
                {len(grouped_locations)} unique location{'' if len(grouped_locations) == 1 else 's'} • 
                {len(location_data)} total appearance{'' if len(location_data) == 1 else 's'}
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