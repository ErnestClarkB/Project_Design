
from keras.models import load_model
import numpy as np
from function import *
import matplotlib.pyplot as plt



def detect_disease(image,model):

  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
  #image = Image.open(path).convert('RGB')
  size = (224, 224)
  #image = ImageOps.fit(image, size, Image.ANTIALIAS)
  
  image_array = image
  print("Image Type: ",type(image_array))
  normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
  data[0] = normalized_image_array
  prediction = model.predict(data)
  enumerate_object = enumerate(prediction[0])
  temp = 0
  highest = 0
  names = []
  percentages = []
  for i in range(len(prediction[0])):
      iteration = next(enumerate_object) 
      temp = iteration[1]
      name,percentage = iteration
      names.append(name)
      percentages.append(percentage)
      #print("Prediction : ", prediction)

      """
  for i in range(len(percentages)):
    if percentages[i]>highest:
      highest = percentages[i]
      name = names[i]
  categories = ['anthracnose','black_spot','phytophthora','powdery_mildew','ring_spot']


  for i in range(len(categories)):
      prediction = categories[names[i]], percentages[i]*100
      print("Predictions" , prediction)


  print('\nPrediction: ',categories[name],'\nPercentage: ', highest)
  """
  z = 0
  disease_index = 5

  for i in range(len(percentages)):
    if percentages[i]>highest:
      highest=percentages[i]
      index = i
      
  if highest > .7:
    nd = index
  else:
    nd = 5


    

    """
    for i in range(len(percentages)):
      if percentages[i]>z:
        z = percentages[i]
        disease_index = i

    
    if highest > .7:
        z="None"
        disease_index = 5
  """
  return highest,nd

def detect_papaya(image,model_detect):
    model = model_detect

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    #image = Image.open(path).convert('RGB')
    size = (224, 224)
    #image = ImageOps.fit(image, size, Image.ANTIALIAS)
    
    image_array = image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    enumerate_object = enumerate(prediction[0])
    index = 0
    for i in range(len(prediction[0])):
        
        if (prediction[0][i]*100) >= 90:
            if i == 0:
                predictions = 'None'
                index = i
                
            if i == 1:
                predictions = 'Papaya'
                index = i
    print('*************************************************************************')
    print('Papaya Detection Prediction: ', predictions)
    print("PREDICTIONS: ",prediction)
    print('*************************************************************************')
    return prediction

def detect_maturity(img):

    maturity_results = ()
    Green_HSV = (33,0,0,90,255,255)#0,179,0,255,0,98 #32 104 0 123 7 219
    Yellow_HSV = (1,0,0,32,255,255)
    default_HSV = (1,43,0,70,255,255)

    Original_images = process_image(default_HSV,img) #img,imgresult,imgContour,imgCanny,imgDialation,mask
    imgStack = results(Original_images)
    #x = find_area(Original_images[4],Original_images[2])
    #getContours(Original_images[4],Original_images[2])
    imgStack = results(Original_images)

    color1 = 'green'
    Green_area,Green_result,Green_img = findColor(Original_images[1],Green_HSV,color1)

    color2 = 'yellow'
    Yellow_area,Yellow_result,Yellow_img = findColor(Original_images[1],Yellow_HSV,color2)

    maturity_results = img, Original_images[1],Yellow_img ,Green_img
    resultStack = result_stack(maturity_results)

    Original_nonzero = np.nonzero(Original_images[1])
    Original_nonzero = len(Original_nonzero[1])+len(Original_nonzero[2])+len(Original_nonzero[0])
    Green_nonzero = np.nonzero(Green_img)
    Green_nonzero = len(Green_nonzero[1])+len(Green_nonzero[2])+len(Green_nonzero[0])
    Yellow_nonzero = np.nonzero(Yellow_img)
    Yellow_nonzero = len(Yellow_nonzero[1])+len(Yellow_nonzero[2])+len(Yellow_nonzero[0])

    #print("Total Non-zerofor Original pixels = ",Original_nonzero)
    #print("Total Non-zero for %s pixels = %f" %(color1,Green_nonzero))
    #print("Total Non-zerofor %s pixels = %f "%(color2,Yellow_nonzero))
    green=Green_nonzero/Original_nonzero*100
    yellow=Yellow_nonzero/Original_nonzero*100
    #print(color1,' is ',green,' percent of papaya' )
    #print(color2,' is ',yellow,' percent of papaya' )

    return green, yellow

def output(img1,img2,model_disease):
    categories = ['anthracnose','black_spot','phytophthora','powdery_mildew','ring_spot','None']
    
    percentage, index = detect_disease(img2,model_disease)
    percentage = percentage*100 
    percentage = "{:.2f}".format(percentage)
    disease = categories[index]
    green, yellow = detect_maturity(img1)

    print("Type: ", type(percentage))
    print('Prediction: ',disease, '\nPercentage: ',percentage)

    
    if (green > 84) & (yellow <16):
        Maturity = "green"
    elif (green > 68) & (yellow < 32):
        Maturity = "breaker"
    elif (green > 52) & (yellow < 48):
        Maturity = "1/3 ripe"
    elif (green > 36) & (yellow < 64):
        Maturity ="half ripe"
    elif (green > 20) & (yellow < 80):
        Maturity = "ripe"
    else:
        Maturity =  "table ripe"

    
    
    print("Maturity : ", Maturity)
    print('Green Percentage: ',green,'%')
    print('Yellow Percentage: ',yellow,'%')
    
    return disease, percentage, Maturity

def show(frame1 ,disease, percentage, maturity):
    plt.title("Papaya Image " , loc = 'left')
    plt.imshow(frame1)
    
    if disease != 'None':

        font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 8}

        plt.rc('font', **font)   

        plt.rcParams['text.color'] = 'white'
        plt.text(10, 210,  disease + " : " + str(percentage),bbox=dict(boxstyle="square"))
        #plt.text(214, 210, maturity, ha = 'right' , bbox=dict(boxstyle="square"))
        #plt.text(10, 210, str(percentage), bbox=dict(boxstyle="square"))

        font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

        plt.rc('font', **font)   
    else: 
        plt.text(10, 210,  "No Disease detected ",bbox=dict(boxstyle="square"))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 8}

    plt.rc('font', **font)   

    plt.rcParams['text.color'] = 'white'
    plt.text(214, 210, maturity, ha = 'right' , bbox=dict(boxstyle="square"))


    

    
    plt.show()



