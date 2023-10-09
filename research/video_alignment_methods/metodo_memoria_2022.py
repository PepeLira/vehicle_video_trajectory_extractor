from ast import Break
import numpy as np
import cv2 
import os 
from PIL import Image
import matplotlib.pyplot as plt
from skimage.io import imread, imshow

INPUT_VIDEO_PATH = 'video_sim_30s_movement.mp4'
OUTPUT_VIDEO_PATH = 'video_sim_30s_movement_alejandra.mp4'

##############-------------------------------------definciones  ------------------------------------############################
def movingAverage(curve, radius):
    window_size = 2 * radius + 1
    # Define the filter
    f = np.ones(window_size)/window_size
    # Add padding to the boundaries
    curve_pad = np.lib.pad(curve, (radius, radius), 'edge')
    # Apply convolution
    curve_smoothed = np.convolve(curve_pad, f, mode='same')
    # Remove padding
    curve_smoothed = curve_smoothed[radius:-radius]
    # return smoothed curve
    return curve_smoothed
  

def smooth(trajectory):
    smoothed_trajectory = np.copy(trajectory)
    # Filter the x, y and angle curves
    for i in range(3):
        smoothed_trajectory[:,i] = movingAverage(trajectory[:,i], radius=10)
    return smoothed_trajectory


def fixBorder(frame):
    s = frame.shape
    T = cv2.getRotationMatrix2D((s[1]/2, s[0]/2), 0, 1.04)
    frame = cv2.warpAffine(frame, T, (s[1], s[0]))
    return frame

def kalmanFilter(scaleX, scaleY, theta, transX, transY):

    global errorScaleX
    global errorScaleY
    global errorTransX
    global errorTransY
    global errorTheta

    frame1ScaleX = scaleX
    frame1ScaleY = scaleY
    frame1Theta  = theta
    frame1TransX = transX
    frame1TransY = transY

    frame1ErrorScaleX = errorScaleX + QScaleX
    frame1ErrorScaleY = errorScaleY + QScaleY
    frame1ErrorTheta  = errorTheta + QTheta
    frame1ErrorTransX = errorTransX + QTransX
    frame1ErrorTransY = errorTransY + QTransY

    gainScaleX = frame1ErrorScaleX / (frame1ErrorScaleX + RscaleX)
    gainScaleY = frame1ErrorScaleY / (frame1ErrorScaleY + RscaleY)
    gainTheta  = frame1ErrorTheta / (frame1ErrorTheta + RTheta)
    gainTransX = frame1ErrorTransX / (frame1ErrorTransX + RscaleX)
    gainTransY = frame1ErrorTransX / (frame1ErrorTransY + RscaleX)

    scaleX = frame1ScaleX + gainScaleX * (sumScaleX - frame1ScaleX)
    scaleY = frame1ScaleY + gainScaleY * (sumScaleY - frame1ScaleY)
    theta  = frame1Theta + gainTheta   * (sumTheta - frame1Theta)
    transX = frame1TransX + gainTransX * (sumTransX - frame1TransX)
    transY = frame1TransY + gainTransY * (sumTransY - frame1TransY)

    errorScaleX = (1 - gainScaleX) * frame1ErrorScaleX
    errorScaleY = (1 - gainScaleY) * frame1ErrorScaleX
    errorTheta  =  (1 - gainTheta) * frame1ErrorTheta
    errorTransX = (1 - gainTransX) * frame1ErrorTransX
    errorTransY = (1 - gainTransY) * frame1ErrorTransY


#######---- fin de definiciones---------#######


#############################
### Global Kalman values ####
#############################
QScaleX = QScaleY = QTheta = QTransX = QTransY = 0.004
RscaleX = RscaleY = RTheta = RscaleX = RscaleX = 0.5
sumScaleX = sumScaleY = sumTransX = sumTransY = sumTheta = 0
errorScaleX = errorScaleY = errorTheta = errorTransX = errorTransY = 1
scaleX = scaleY = theta = transX = transY = 0


##### --- lista para guardar información------######
videoNames = [""]
puntosframe=[]
Desplazamiento= []
Puntos= []
Desframe=[]
errores=[]



######----- introducción del video-------------######
cap = cv2.VideoCapture(INPUT_VIDEO_PATH)
#cap = cv2.VideoCapture('kennedy_corto.mp4')
#cap = cv2.VideoCapture('video_ale.mp4')
#cap = cv2.VideoCapture('Kennedy.mp4')
#cap = cv2.VideoCapture('kennedy01.mp4')
#cap = cv2.VideoCapture('sc.mp4')



nFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))


#----atrapar error de captar video----
try:   
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print ('Error: Creating directory of data')



#############################-------------------ayuda para definiciones ---------------##########################

#----parametros Shi-Tomasi para deteccion de esquinas----
feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.005,
                       minDistance = 3,
                       blockSize = 5)
  
#----Parametros de Lucas kanade-----
lk_params = dict( winSize = (10, 10),
                  maxLevel = 3,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                              3, 0.08))
  
#----Crear colores al azar para los movimientos----
color = np.random.randint(0, 255, (100, 3))
  

#----selecciona 1er frame----
cap.set(cv2.CAP_PROP_POS_FRAMES, 0) ## This line was missing otherwise it takes the 2nd frame (it resets to the first)
ret, old_frame = cap.read()
frame = old_frame


#---- obtener dimensiones de frame----
try:
    ancho = int(old_frame.shape[1]/2) #columnas
    alto = int(old_frame.shape[0]/2) # filasv
except AttributeError:
    print("finalizado")


#----transformar a escala de grises----
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
old_gray1 = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)



#---- separar frame en 4 fragmentos----
#old_gray1 =old_gray[0:int(alto*1.5),0:int(ancho*1.5)]
#old_gray2 = old_gray[int(alto*0.5):int(alto*3),0:int(ancho*1.5)]
#old_gray3 = old_gray[0:int(alto*1.5),int(ancho*0.5):int(ancho*3)]
#old_gray4 = old_gray[int(alto*0.5):int(alto*3),int(ancho*0.5):int(ancho*3)]



#---- encontrar esquinas de cada fragmento con shitomasi----
p0 = cv2.goodFeaturesToTrack(old_gray1, mask = None,**feature_params)
#p02= cv2.goodFeaturesToTrack(old_gray2, mask = None, **feature_params)
#p03= cv2.goodFeaturesToTrack(old_gray3, mask = None, **feature_params)
#p04= cv2.goodFeaturesToTrack(old_gray4, mask = None, **feature_params)


#----poner en cuadrante correcto-----
#for i in p02:
#    i[0][0]+=alto*0.5

#for i in p03:
#    i[0][1]+=ancho*0.5

#for i in p04:
#    i[0][0]+=alto*0.5
#    i[0][1]+=ancho*0.5


#----unir puntos en una lista----
#p0=np.concatenate((p0,p02), axis=0)
#p0=np.concatenate((p0,p03), axis=0)
#p0=np.concatenate((p0,p04), axis=0)
mask = np.zeros_like(old_frame)


########################################################################################################################################
#-------------------------------------------------------------ciclo de análisis--------------------------------------------
########################################################################################################################################
prevGray = old_gray

##----Grab the middle frame as reference-----
cap.set(1, int(nFrames/2))
ret, midFrame = cap.read()

##----return to the first frame----
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


#----- Prepare video writer-----
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, fps, (w, h))

##--- ajustar transformaciones----
transforms = np.zeros((nFrames - 1, 3), np.float32)
x = []
y = []


####################################################################################################################3
#-----------------------------------
for i in range(nFrames - 2):

    #####----Read next frame-----#####
    read, currentFrame = cap.read()
    if not read:
        break
    
    ####----Transform currentFrame to grayscale and add blur-----#####
    currentGray = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2GRAY)
    currentGray= cv2.GaussianBlur(currentGray, (9, 9),cv2.BORDER_DEFAULT)


    #####-----Calculate optical flow--------########
    currentPoints, status, errors = cv2.calcOpticalFlowPyrLK(prevGray, currentGray, p0, None,**lk_params)

    assert p0.shape == currentPoints.shape

    idx = np.where(status==1)[0]
    p0 = p0[idx]
    currentPoints= currentPoints[idx]

    ######-----Calcular transformacion afin matriz-----#####

    homoMatrix, statusH = cv2.estimateAffine2D(p0, currentPoints, method= cv2.RANSAC, ransacReprojThreshold=3.0, maxIters=200 ,confidence=0.95, refineIters=50)
    dx = homoMatrix[0][2]
    dy = homoMatrix[1][2]
    dTheta = np.arctan2(homoMatrix[1][0], homoMatrix[0][0])
    dsX = homoMatrix[0][0]/np.cos(dTheta)
    dsY = homoMatrix[1][1]/np.cos(dTheta)
    #transforms[i] = [dx, dy, dTheta]
    sx = dsX
    sy = dsY
    sumTransX += dx
    sumTransY += dy
    sumTheta  += dTheta
    sumScaleX += dsX
    sumScaleY += dsY




    ######-----Kalman application-----######
    if (i > 0):
        kalmanFilter(scaleX , scaleY , theta , transX , transY)

    diffScaleX = scaleX - sumScaleX
    diffScaleY = scaleY - sumScaleY
    diffTransX = transX - sumTransX
    diffTransY = transY - sumTransY
    diffTheta  = theta  - sumTheta
    dsX = dsX + diffScaleX
    dsY = dsY + diffScaleY
    dx = dx + diffTransX
    dy = dy + diffTransY
    dTheta = dTheta + diffTheta


    #####----reconstruct the affine matrix with the values obtained from the filter----######
    KalmanSmoothedMatrix = np.zeros((2,3), np.float32)
    KalmanSmoothedMatrix[0][0] = sx * np.cos(dTheta)
    KalmanSmoothedMatrix[0][1] = sx * -1 * np.sin(dTheta)
    KalmanSmoothedMatrix[1][0] = sy * np.sin(dTheta)
    KalmanSmoothedMatrix[1][1] = sy * np.cos(dTheta)
    KalmanSmoothedMatrix[0][2] = dx
    KalmanSmoothedMatrix[1][2] = dy

    #####----Transform the current frame----#####
    outFrame = cv2.warpAffine(currentFrame, KalmanSmoothedMatrix, (w, h))
    outFrame = fixBorder(outFrame)
    writer.write(outFrame)


    ##--- mostrar diferencia entrre videos------#####
    currentFrameRSZ = cv2.resize(currentFrame, (int(currentFrame.shape[0]/2), int(currentFrame.shape[1]/4)))
    outFrameRSZ = cv2.resize(outFrame, (int(outFrame.shape[0]/2), int(outFrame.shape[1]/4)))
    frame_out = cv2.hconcat([currentFrameRSZ, outFrameRSZ])
    cv2.imshow("Before and After", frame_out)
    cv2.waitKey(10)


    #----actualizacion de variables-----####
    prevGray = currentGray
    p0 =  currentPoints

writer.release()
print("El fin")
cv2.destroyAllWindows()
