#import the task from celery

from celery.utils.log import get_task_logger
from celery import shared_task 
from goldenland.settings import EMAIL_RECEIVER

from time import sleep
from .mail import send_mail_to 


logger = get_task_logger(__name__)

 
     
@shared_task(name='contactus_task')
def contactus_task(subject,message,receiver):

   is_task_completed= False   
   error=''   
   try:       
      sleep(5)       
      is_task_completed= True   
   except Exception as err:       
      error= str(err)       
      logger.error(error)   
   if is_task_completed:       
       send_mail_to(subject,message,receiver)
       print("Sent")
   else:
        print(error)       
    #   send_mail_to(subject,error,receiver)   
        return('contactus_task_done')