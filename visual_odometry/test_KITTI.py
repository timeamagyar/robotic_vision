import numpy as np
import cv2

from visual_odometry_KITTI import PinholeCamera, VisualOdometry

cam = PinholeCamera(1241.0,376.0,718.8560,718.8560,607.1928,185.2157)
vo = VisualOdometry(cam,'/media/jacob/Extra Space/KITTI/dataset/sequences/poses/00.txt')

traj = np.zeros((600,600,3),dtype=np.uint8)

for img_id in xrange(4541):
    img = cv2.imread('/media/jacob/Extra Space/KITTI/dataset/sequences/00/image_0/'+str(img_id).zfill(6)+'.png',0)

    vo.update(img, img_id)
    track_points = vo.px_ref
    cur_t = vo.cur_t
    if (img_id > 2):
        x,y,z = cur_t[0],cur_t[1],cur_t[2]
    else:
        x,y,z = 0.,0.,0.
    draw_x,draw_y = int(x)+200,int(z)+90
    true_x,true_y = int(vo.trueX)+200,int(vo.trueZ)+90

    cv2.circle(traj, (draw_x,draw_y),1,(img_id*255/4540,255-img_id*255/4540,0),1)
    cv2.circle(traj, (true_x,true_y),1,(0,0,255),2)
    cv2.rectangle(traj,(10,20),(600,60),(0,0,0),-1)
    text = "Coordinates: x=%2fm y=%2fm z=%2fm" %(x,y,z)
    cv2.putText(traj,text,(20,40),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1,0)
    # for (x,y) in track_points:
    #     cv2.circle(img,(x,y),1,(0,255,0),2)

    cv2.imshow("Road Facing Camera",img)
    cv2.imshow("Trajectory", traj)
    cv2.waitKey(1)

cv2.imwrite('map.png',traj)
