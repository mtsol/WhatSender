import time
import sys
import os
import os.path
import mmap
import warnings
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import urllib.parse
import random

warnings.filterwarnings("ignore", category=DeprecationWarning)

cmd = 'mode 60,28'
os.system(cmd)

start = time.time()
#scriptdir="D:\\Softwares\\WhatsApp-Bulk-Message-Sender-main"
link1="https://web.whatsapp.com/send?phone=92"
link2="&text="
img=[]
clear = lambda: os.system('cls')
min_time = sys.argv[1]
max_time = sys.argv[2]
print(min_time)
print(max_time)


wait_time = 5
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir="+os.path.join(sys.path[0])+"/wbms/User Data") 
#options.add_argument("window-size=1080x720")
options.add_argument('log-level=3')
options.add_argument('disable-gpu')
options.add_argument('disable-infobars')
options.add_argument('disable-extensions')
options.add_argument('disable-dev-shm-usage')
if (len(sys.argv) > 2) and (sys.argv[2] == '--incognito'):
	options.add_argument('--incognito')
#options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

dir_path=os.path.join(sys.path[0])+"/PUT EVERYTHING HERE/"
print(dir_path)
time.sleep(10)
msg_path=dir_path+"msg.txt"
num_path=dir_path+"num.txt"
log_path=os.path.join(sys.path[0])+"/failed.log"
img_path=dir_path+"Images"
clear()

isExist = os.path.exists(dir_path)
if not isExist:
    os.makedirs(dir_path)
    print("PLEASE PUT DATA IN '"'PUT EVERYTHING HERE'"' FOLDER")
    print('Exiting')
    cmd = 'color 0c'  
    os.system(cmd)  
    file = open(msg_path,'a+')
    file.close()
    file = open(num_path,'a+')
    file.close()
    isExist = os.path.exists(img_path)
    if not isExist:
        os.makedirs(img_path)
    time.sleep(10)
    sys.exit()
else:
    cmd = 'color 0a'  
    os.system(cmd)  
    print('*')


print("\n - - - - - - - - - - - - -STARTING - - - - - - - - - - - - -")
print(" - - - -Reading Numbers, Message and Images to send - - - - ")


wait_in_case_of_video = 0
for root, subdirs, files in os.walk(img_path):
    for file in files:
        if os.path.splitext(file)[1].lower() in ('.jpg', '.png'):
             img.append(file)
        elif os.path.splitext(file)[1].lower() in ('.mp4'):
             img.append(file)
             wait_in_case_of_video = (os.path.getsize(img_path+'/'+file)/1000000)*2
             print(wait_in_case_of_video)
             break
#print(img)


#sys.exit()
with open(msg_path,"r+") as file:
    msg = file.read()

send_msg=urllib.parse.quote_plus(msg)
#send_msg = msg.replace('\n', '%0A').replace('\r', '%0A')

if os.stat(num_path).st_size == 0 or os.stat(msg_path).st_size == 0:
    cmd = 'color 0c'  
    os.system(cmd) 
    print('\n - - - - - -num.txt or msg.txt is empty, Exiting - - - - - -')
    time.sleep(10)
    sys.exit()

if len(img) > 3:
    cmd = 'color 0c'  
    os.system(cmd) 
    print('\n - - - - - - Maximum 3 images allowed, Exiting - - - - - - -')
    time.sleep(10)
    sys.exit()
elif len(img) == 0:
    print('\n - - - - - - - - - - -No images found - - - - - - - - - - - ')
elif len(img):
    print(' - - - - - - - - - - - '+str(len(img))+' Images found - - - - - - - - - - - ')

f = open(num_path, "r+")
nums = f.readlines()
nums=  lines = [line.rstrip() for line in nums]
buf = mmap.mmap(f.fileno(), 0)
lines = 0
readline = buf.readline
while readline():
    lines += 1
print('\n - - - - - - '+str(lines)+' numbers found in num.txt, Starting- - - - - -')
print("\n - - - - - - - - - - - -Your Message - - - - - - - - - - - -")
print('"'+msg+'"')
print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

f = open(log_path, "a")
f.write('\nEdited on '+datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime("%d %B %I:%M %p")+'\n')
f.close()


def send():
    count=0
    sent=0
    fail=0
    loadtime=00.00
    looood = 0
    w = webdriver.Chrome(options=options)
    #delta1 = datetime.timedelta.total_seconds()#
    while (count < lines): 
        tosend = nums[count]
        if (count % 9 == 8):
            print("if successful")
            time.sleep(random.randint(int(50), int(70)))
            print("1 minute wait over")
        wait_time = random.randint(int(min_time), int(max_time))
        print("waiting " + str(wait_time) + " sec.")
        time.sleep(wait_time)
        print("wait complete")
        if len(tosend) != 10:
            count = count + 1
            f = open(log_path, "a")
            f.write('\n'+tosend+' - '+str(len(tosend))+' digit number\n')
            f.close()
            fail=fail+1
            cmd = 'color 0c'  
            os.system(cmd) 
            print('\n - - Number '+tosend+' is not a 10 digit number, skipping - - ')
            cmd = 'color 0a'  
            os.system(cmd) 
            linkk='about:blank'
            continue
        else:
            linkk=link1+tosend+link2+send_msg#+'%F0%9F%98%80'
        befload = time.time()
        w.get(linkk)
        try:
            w.find_element_by_class_name("_2UwZ_")#.click()
        except NoSuchElementException:
            print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        else:
            cmd = 'color 0c'  
            os.system(cmd) 
            print(" - - -RE-LOGIN NEEDED, Scan QR code and restart script - - -")
            cmd = 'color 0a'  
            os.system(cmd) 
        #print(" - - - - - - - - - -WhatsApp Web loaded - - - - - - - - - - ")
        search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
        try:
            WebDriverWait(w, 120).until(EC.presence_of_element_located((By.XPATH, search_xpath)))
        except TimeoutException:
            print("WhatsApp could'nt load in 2 minutes")
            print(tosend)
        afload = time.time()
        totalload = afload-befload
        #print("%0.2f" % totalload)
        looood = totalload+looood
        #lod = "%0.2f" % looood
        #print("LOAD: "+lod+"\n\n\n\n")
        '''
        now = time.time()
        noww = "%0.2f" % now
        print("NOW: "+noww)
        pr1 = "%0.2f" % loadtime
        print("prev load: "+pr1)
        nss = now-start
        ns = "%0.2f" % nss
        print("Now-Start: "+ns)
        loadtime = nss - loadtime
        pr = "%0.2f" % loadtime
        print("Curr load: "+pr)
        '''
        time.sleep(2)
        try:
            #element = w.find_element_by_class_name("_2Nr6U").text
            w.find_element_by_class_name("IVxyB")
            w.find_element_by_class_name("_2Nr6U")
            #msg_box = WebDriverWait(w, 100).until(EC.presence_of_element_located((By.XPATH, msg_xpath)))
        except NoSuchElementException:
            msg_xpath = '//div[@contenteditable="true"][@data-tab="9"]'
            WebDriverWait(w, 30).until(EC.presence_of_element_located((By.XPATH, msg_xpath))).send_keys(Keys.ENTER)
           # msg_box.click()
           # pyperclip.copy(msg)
           # msg_box.send_keys(Keys.SHIFT, Keys.INSERT)
           # msg_box.send_keys(Keys.ENTER)
            sent = sent + 1
          #  w.get_screenshot_as_file(os.path.join(sys.path[0])+"\\ss\\"+tosend+"_msg.png")
            #print('\n - - - - - ['+str(sent)+'] - - - - Message sent to '+tosend+' - - - - - ')
            print('\n - - - - - - - - - Message sent to '+tosend+' - - - - - ['+str(sent)+']')
            for imgs in img:
                #print(imgs)
                tosend_img=img_path+'/'+imgs
                #print(tosend_img)
                #sys.exit()
                attach_xpath='//div[@title="Attach"]'
                WebDriverWait(w, 10).until(EC.presence_of_element_located((By.XPATH, attach_xpath))).click()
                #print("Attach Found")
                #attach_btn.click()
                time.sleep(1)
                doc_xpath = '//span[@data-icon="attach-document"]'
                img_xpath = '//span[@data-icon="attach-image"]'
                send_xpath = '//span[@data-icon="send"]'
                #doc_btn = WebDriverWait(w, 2000).until(EC.presence_of_element_located((By.XPATH, doc_xpath)))
                #print("Doc Found")
                #doc_btn.click()
                #self.send_attachment()
                WebDriverWait(w, 10).until(EC.presence_of_element_located((By.XPATH, img_xpath)))
                #img_btn = w.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]')
                #img_btn.click()
                w.find_element_by_tag_name('input').send_keys(tosend_img)
               # img_btn = w.find_element_by_tag_name('input')
              #  img_btn.send_keys(tosend_img)
                WebDriverWait(w, 10).until(EC.presence_of_element_located((By.XPATH, send_xpath))).click()
                #send_btn.click()
                print(' - - - - - - - - - Image sent '+imgs+' - - - - - - - - - -')
                time.sleep(wait_in_case_of_video)
               # if imgs == img[-1]:
                  #  w.get_screenshot_as_file(os.path.join(sys.path[0])+"\\ss\\"+tosend+"_img.png")
                #time.sleep(2)
            wait_time = random.randint(int(min_time), int(max_time))
            time.sleep(wait_time)
            w.execute_script("window.close();")
            time.sleep(2)
            
            try:
                WebDriverWait(w, 1).until(EC.alert_is_present())
                alert = w.switch_to.alert
                alert.accept()
                print("alert accepted")
            except TimeoutException:
                print("no alert")
            count = count + 1
        else:
            f = open(log_path, "a")
            f.write('\n'+tosend+' - Not on whatsapp\n')
            f.close()
            time.sleep(1)
          #  w.get_screenshot_as_file(os.path.join(sys.path[0])+"\\ss\\"+tosend+"_fail.png")
            fail=fail+1
            cmd = 'color 0c'  
            os.system(cmd) 
            print('\n - - - Number '+tosend+' is not on WhatsApp, skipping - - - ')
            cmd = 'color 0a'  
            os.system(cmd) 
            count = count + 1
            
    else:
        #w.close()
        w.quit()
        time.sleep(5)
        clear()
        cmd = 'color 09'  
        os.system(cmd) 
        print('\n - - - - - - - - - Report:  '+str(sent)+'/'+str(lines)+' successful - - - - - - - - ')
        exect = time.time()-start
        
        '''
        timee=time.time()-start
        timeee = "%0.2f" % timee
        print(timeee)
        '''
        actual_exec=exect-looood

        exectime="%0.2f" % exect
        ldtime="%0.2f" % looood
        act_exec = "%0.2f" % actual_exec
        #print(' - - - - - - - Task finished in '+exectime+' seconds - - - - - - - ')
        print(' - - - - - - - -WhatsApp Web load time: '+ldtime+' s- - - - - - - ')
        #print(' - - - - - - - - - - - - - - - - - - -  + ')
        print(' - - - - - - - -Actual execution time: '+act_exec+' s- - - - - - - -')
        print(' - - - - - - - -Total execution time: '+exectime+' s- - - - - - - -')
       #print('\n - - - - - - - - - - - - - Bye :) - - - - - - - - - - - - - ')
        
        #if fail!=0:
            #os.startfile(log_path)
        print("\n - - - - - - WBMS - WhatsApp Bulk Message Sender - - - - - -")
        print(" - - - - - - - - - Github.com/AkshayCraZzY - - - - - - - - -")
        time.sleep(20)
       # sys.exit()
    #delta2 =  datetime.timedelta.total_seconds()
    #minutes = (delta1 - delta2) / 60
    #if (minutes > 5):
    #    time.sleep(random.randint(int(50), int(70)))
        



send()
