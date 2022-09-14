#include <stdio.h>
#include <stdlib.h>
//#include <stddef.h>
#include <unistd.h>
#include <string.h>

#include <net/if.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>

#include <linux/can.h>
#include <linux/can/raw.h>

int main(void)
{
    int s;
    int nbytes;
    struct sockaddr_can addr;
    struct can_frame frame;
    struct ifreq ifr;

    
    
    //Abrir Socket para la comunicación CAN
    s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    
    if (s  == -1){
        perror("Error while opening socket");
        
    }
    if (s  != -1){
        printf ("No error\n");
        
    } 
    
    strcpy (ifr.ifr_name, "can0"); //Copy SRC to DEST.
    ioctl (s, SIOCGIFINDEX, & ifr); //Dtermina el interface index 

    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;
    //Vincular socket a una interfaz CAN
    int b = bind(s, (struct sockaddr *) & addr, sizeof (addr));
    
    if (b==-1)
    {
        perror("Error in socket bind");
    }
    if (b==-0)
    {
        printf("No Error in socket bind");
    }


    nbytes = read(s, & frame, sizeof (struct can_frame));
    //printf ("CAN_FRAME2\n",nbytes);
    if (nbytes != 0 )
    {
        perror("can raw socket read:");
        printf ("0x% 03x [% d]",frame.can_id, frame.can_dlc);
        for ( int i = 0; i < frame.can_dlc; i++)
        {
            printf ("%02x", frame.data[i]);
        }
        printf("\r\n");
        
        return 1;
    }
    if (nbytes <0 )
    {
        perror("can raw socket read:");
        
        return 1;
    }
    if (nbytes < sizeof(struct can_frame))
    {
        fprintf(stderr,"read: incomplete CAN frame\n");
        //printf ("CAN_FRAME2\n",nbytes);
        //return 1;
    }
    
    /*for(;;)
    {
    /*frame.can_id=0x111;
    frame.can_dlc=2;
    frame.data[0]=0x02;
    frame.data[1]=0x31;*/

    /*nbytes = read(s, & frame, sizeof (struct can_frame));
     
    //nbytes = recvfrom (s,& frame, sizeof (struct can_frame), 0, (struct sockaddr *)& addr,& len);*/
        /*if (nbytes <0 )
        {
        perror("can raw socket read");
        printf ("CAN_FRAME\n",nbytes);
        //return 1;
        }
        if (nbytes < sizeof(struct can_frame))
        {
        fprintf(stderr,"read: incomplete CAN frame\n");
        //printf ("CAN_FRAME\n",nbytes);
        //return 1;
        }
    //printf ("CAN_FRAME\n",nbytes);
    }
    */
   //close(s);
    return 0;
    
    
    
}

