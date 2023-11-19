
from pyproj import Proj
import cv2
import numpy as np

class ControllerHelper:
    @staticmethod
    def gps_2_utm(latitude, longitude):
        zone = int((longitude + 180) / 6) + 1
        proj = Proj(proj='utm', zone=zone, ellps='WGS84', south=True)
        x, y = proj(longitude, latitude)

        return x, y

    @staticmethod
    def transform_pixel_2_gps_cords(reference_cords, input_coord):
        """
        Transforms a pixel coordinate to GPS coordinate using an affine transformation.

        Parameters:
        - pixel_coords: List of at least 3 pixel coordinates [[x1, y1], [x2, y2], ...]
        - gps_coords: Corresponding list of GPS coordinates [[x1, y1], [x2, y2], ...]
        - input_coord: The pixel coordinate to transform [x, y]

        Returns:
        Transformed GPS coordinate [x, y]
        """
        pixel_coords = list(reference_cords.keys())
        gps_coords = list(reference_cords.values())
        
        transformation_m = cv2.getAffineTransform(np.array(pixel_coords[:3], dtype=np.float32),
                                np.array(gps_coords[:3], dtype=np.float32))
        
        # Transform the input coordinate
        augmented_coord = np.array([[input_coord[0], input_coord[1], 1]])
        transformed_coord = np.dot(augmented_coord, transformation_m.T)[0]

        return transformed_coord[0], transformed_coord[1]
    
    @staticmethod
    def add_meters_2_trajectory(reference_points, trajectories):

        for vehicle_id, data in trajectories.items():
            x_trajectory = data['x_trajectory']
            y_trajectory = data['y_trajectory']
            frames = data['frames']
            data['x_m_trajectory'] = []
            data['y_m_trajectory'] = []
            data['speed_x'] = []
            data['speed_y'] = []

            for i, (x, y, frame) in enumerate(zip(x_trajectory, y_trajectory, frames)):
                gps_coords_x, gps_coords_y = ControllerHelper.transform_pixel_2_gps_cords(reference_points, [x, y])
                m_coords_x, m_coords_y = ControllerHelper.gps_2_utm(gps_coords_x, gps_coords_y)
                data['x_m_trajectory'].append(m_coords_x)
                data['y_m_trajectory'].append(m_coords_y)
                if i == 0:
                    data['speed_x'].append(0)
                    data['speed_y'].append(0)
                else:
                    data['speed_x'].append((m_coords_x - data['x_m_trajectory'][i-1]) / (data['time'][i] - data['time'][i-1]))
                    data['speed_y'].append((m_coords_y - data['y_m_trajectory'][i-1]) / (data['time'][i] - data['time'][i-1]))

            trajectories[vehicle_id] = data

        return trajectories