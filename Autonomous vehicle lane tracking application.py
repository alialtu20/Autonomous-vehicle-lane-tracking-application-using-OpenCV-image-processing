import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


# videonun değişkene atanması
kamera=cv2.VideoCapture("C:/Users/alial/Desktop/odev/BlackVue DR400G-HD Vehicle Recorder - Highway (Night).mp4_2.mp4")  # videonun değişkene atanması

toprak=cv2.imread("C:/Users/alial/Desktop/odev/toprakyol.jpg")
toprak=toprak[:,1000:2000]
print(toprak.shape)
cv2.imshow("asds",toprak)

while True:

    
    ret,frame=kamera.read() # videonun okunup bir değişkene atanması 
    
    frame=frame[0:680,0:1280]
    
    gri=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  # BGR dan gri tona dönüştürme
    filtre=cv2.GaussianBlur(gri,(7,7),0)    # gaussian filtre uygulanması
    ret,thresh=cv2.threshold(filtre,160,255,cv2.THRESH_BINARY)  # thresholding uygulanması
    kenarlar=cv2.Canny(thresh,200,255)  # Canny kenar dedektörü uygulanması
   
    
    height, width = kenarlar.shape
    kesikmaske = np.array([[(200, height-200), (500, 300),(740,300) ,(width-60, height-200)]]) # amaçlanan görüntünün elde edilmesi
    
    maske = np.zeros_like(kenarlar) # kenarlar matrisi 0 yani siyahla kaplanır
    
    maske = cv2.fillPoly(maske, kesikmaske, 255)  # kesikmaske maske matrisine 
    maske = cv2.bitwise_and(kenarlar, maske) # and mantıksal operatörü uygulanır 
    
    # Aynı kesik görüntü  elde edilme işlemleri burada da sağlanıyor.
    maske2=maske[0:680,0:640]
    maske2=maske2[0:680,0:1280]
    siyah2=np.zeros_like(maske2)
    maske2=np.hstack((maske2,siyah2))
   
    maske=maske[0:680,640:1280]
    maske=np.hstack((siyah2,maske))

    #diktörtgen ve çizgiler oluşturulur
    cv2.rectangle(frame,(350,460),(960,300),(0,255,0),1)
    solciz=cv2.line(frame,(430,360),(530,360),(0,255,0),1)
    sagciz=cv2.line(frame,(780,360),(880,360),(0,255,0),1)
    solortciz=cv2.line(frame,(480,350),(480,370),(255,0,0),1)
    sagortciz=cv2.line(frame,(830,350),(830,370),(255,0,0),1)
    
    # çizgilerin houghline methoduyla belirlenmesi sağlanır
    solserit=cv2.HoughLinesP(maske2,3,np.pi/180,50,minLineLength=30,maxLineGap=500)
    sagserit=cv2.HoughLinesP(maske,3,np.pi/180,50,minLineLength=30,maxLineGap=500)

    cv2.putText(frame,"Direksiyon Derecesi:",(10,30),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,0,255),1) # ekrana yazı eklemesi
    
    dizi1=[]
    dizi2=[]
    dizi=[]
    
    #sol şeridin karakteristiğini çıkarma
    if solserit is not None:
        for cizgi1 in solserit:
            
            x1,y1,x2,y2=cizgi1[0]
            cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),1)
            
            

            if( (int((int(x2)+int(x1))/2))<420 ) :
                cv2.putText(frame,"sola git",(450,430),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                cv2.putText(frame,str(round(float((60/(830-480))*(-480+(int((int(x2)+int(x1))/2)))),2)),(300,30),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),1)

            elif( (int((int(x2)+int(x1))/2))>520 ):    
                cv2.putText(frame,"saga git",(750,430),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2) 
                cv2.putText(frame,str(round(float((60/(830-480))*(-480+(int((int(x2)+int(x1))/2)))),2)),(300,30),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),1)  

            elif((int((int(x2)+int(x1))/2))>475 and (int((int(x2)+int(x1))/2))<485 ):
                cv2.putText(frame,"Dengeli",(600,380),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)     

            dizi1=[np.array([[int(x1),int(y1)],[int(x2),int(y2)]],dtype=np.int32)]
            
    # sağ şeridin karakteristiğini çıkarma
    if sagserit is not None:
        for cizgi2 in sagserit:
            
            x1,y1,x2,y2=cizgi2[0]
            cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),1)
            dizi2=[np.array([[int(x1),int(y1)],[int(x2),int(y2)]],dtype=np.int32)]

    
    # şeritler üzerinin farklı renkle kaplanması
    cv2.polylines(frame,dizi2,True,(255,0,0),1)
    cv2.fillPoly(frame,dizi2,(255,0,0),offset=(10,0))
  
    # görüntünün aktif görünür hale getirilmesi
    cv2.imshow("maske",maske2)        
    cv2.imshow("kenar",kenarlar)       
    cv2.imshow("kamera",frame)
    
    # 25 mili saniye de bir çerçeve hızı ve q tuşu ile döngüden çıkılarak görüntünün kapatılması
    if cv2.waitKey(25) & 0xFF==ord("q"):
        break
# görüntüyü kapat
kamera.release()
cv2.destroyAllWindows()