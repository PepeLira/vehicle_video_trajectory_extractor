from .aligner_strategy import AlignerStrategy
import cv2
import numpy as np

class OrbAligner(AlignerStrategy):
    def __init__(self):
        self.detector = None
        self.matcher = None
        self.filter = None
        self.nfeatures = 1000
        self.affine_transformations = None
        self.feature_rate = 1

        self.orb = cv2.ORB_create(nfeatures=self.nfeatures)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    
    def align(self, frame, frame_index, affine_transformations=None):
        # Input:
        # frame: frame a alinear
        # frame_index: el indice del frame a alinear (0 es el primer frame)
        # affine_transformations: lista de transformaciones afines para cada frame (ej: [theta, s, tx, ty])

        # puedes usar el metodo con nuevas transformaciones o con las que ya estan guardadas
        if self.affine_transformations is not None and affine_transformations is None:
            affine_transformations = self.affine_transformations

        # validamos que las transformaciones afines esten definidas
        if affine_transformations is None:
            raise Exception("The affine transformations must be set before aligning the frames")
        elif frame_index >= len(affine_transformations):
            raise Exception("The affine transformation for the frame {} cant be found".format(frame_index))
        
        affine_matrix = self.reformat(affine_transformations[frame_index])

        aligned_frame = cv2.warpAffine(frame, affine_matrix, (frame.shape[1], frame.shape[0]))

        return aligned_frame

    def update_affine_transformations(self, affine_transformations):
        self.affine_transformations = affine_transformations

    def set_affine_transformations(self, input_video):
        self.affine_transformations = [np.array([0, 1, 0, 0])] # the first frame stays still
        first_frame = True
        for current_frame in input_video.get_frames():
            if first_frame:
                reference_frame = current_frame
                rf_keypoints, rf_descriptor = self.extract_features(reference_frame)
                first_frame = False
            else:
                current_frame_keypoints, current_frame_descriptor = self.extract_features(current_frame)

                source_pts, destination_pts = self.match_features((current_frame_keypoints, current_frame_descriptor), 
                                                                  (rf_keypoints, rf_descriptor))
                affine_matrix, _ = cv2.estimateAffinePartial2D(source_pts, destination_pts, confidence= 0.9, method=cv2.RANSAC)
                affine_transformation = self.extract_affine_parameters(affine_matrix)

                self.affine_transformations.append(affine_transformation)
        
        return self.affine_transformations

    def extract_features(self, frame):
        keypoints, descriptor = self.orb.detectAndCompute(frame, mask = None)
        return keypoints, descriptor
    
    def match_features(self, feature_pair_1, feature_pair_2):
        matches = self.matcher.match(feature_pair_1[1], feature_pair_2[1])

        num_matches = int(len(matches) * self.feature_rate)
        matches = sorted(matches, key=lambda x: x.distance)[:num_matches]

        source_points = np.float32([feature_pair_1[0][m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        destination_points = np.float32([feature_pair_2[0][m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        return source_points, destination_points
    
    def extract_affine_parameters(self, matrix):
        s = np.sqrt(matrix[0, 0] ** 2 + matrix[1, 0] ** 2)
        theta = np.arctan2(matrix[1, 0], matrix[0, 0])
        tx = matrix[0, 2]
        ty = matrix[1, 2]
        
        transformed_array = np.array([theta, s, tx, ty])
        
        return transformed_array
    
    def reformat(self, parameters):
        theta = parameters[0]
        s = parameters[1]
        tx = parameters[2]
        ty = parameters[3]
        
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        matrix = np.array([
        [cos_theta * s, -sin_theta * s, tx],
        [sin_theta * s, cos_theta * s, ty]
        ])
        
        return matrix


    def __str__(self):
        return "ORB Aligner"

## For testing the class on console
if __name__ == "__main__":
    class InputVideo:
        def __init__(self, video_path):
            self.video_path = video_path

        def get_video_path(self):
            return self.video_path
        
        def get_frames(self):
            video = cv2.VideoCapture(self.video_path)
            while True:
                ret, frame = video.read()
                if ret:
                    yield frame
                else:
                    break
            video.release()

        def get_video_fps(self):
            video = cv2.VideoCapture(self.video_path)
            fps = video.get(cv2.CAP_PROP_FPS)
            video.release()
            return fps

        def display_frames(self, frame):
            for frame in self.get_frames():
                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        def __str__(self):
            return self.video_path

    input_video = InputVideo("../../../videos/video1_30s_sift_estabilizado_filtrado.mp4")
    aligner = OrbAligner()
    aligner.set_affine_transformations(input_video)
    print(aligner.affine_transformations)

