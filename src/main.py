import pyautogui as pag
import time 

filePath = r'D:/Project/CloverRelic/src/'
global direction
direction = 0


def findImg(imgName, delayTime=0, count=40, intervalTime=0.5, validation=False, confidence=0.9, exit=True):
    ''' 查找某个图像在屏幕上的坐标
    
    :param imgName: 图像名
    :param delayTime: 延迟几秒才开始查找
    :param count: 尝试次数
    :param intervalTime: 尝试间隔时间
    :validation: 验证目标是否有效
    :return: 返回目标中心像素点坐标，若未找到则返回坐标(-1, -1)
    '''
    time.sleep(delayTime)
    target = pag.Point(-1, -1)
    while count>0 and target.x<0:
        try:
            imgs = pag.locateAllOnScreen(filePath+imgName+'.png', confidence=confidence)
            imgs = list(imgs)
            if validation is True:
                screenshot = pag.screenshot()
                for img in imgs:
                    point = pag.center(img)
                    pixel = screenshot.getpixel(point)
                    if pixel[0]>180:
                        target = point
                        break
            else:
                target = pag.center(imgs[0])
                break
        except:
            pass
        count = count-1
        if count>0:
            time.sleep(intervalTime)
    if exit is True and target.x<0:
        pag.alert(text='查找失败'+imgName, title='警告')
        exit()
    else:
        return target


def battle():
    findImg('victory', 0, 10, 1, False)
    target = findImg('exit')
    pag.leftClick(target)
    time.sleep(1)
    pag.leftClick(target)


def doEvent(count=10):
    time.sleep(1)
    global direction
    while count>0:
        p1 = findImg('elite', count=1, validation=True, exit=False)
        if p1.x>=0:
            print('精英战斗')
            pag.leftClick(p1)
            battle()
            direction=0
            return
        p2 = findImg('common', count=1, validation=True, exit=False)
        if p2.x>=0:
            print('普通战斗')
            pag.leftClick(p2)
            battle()
            direction=0
            return
        p3 = findImg('encounter', count=1, validation=True, exit=False)
        if p3.x>=0:
            print('事件')
            pag.leftClick(p3)
            pag.leftClick(findImg('select',2))
            target = findImg('battle_flag',count=1, delayTime=3, exit=False)
            if target.x>0:
                battle()
            target = findImg('select', count=1, delayTime=2, exit=False)
            if target.x>0:
                pag.leftClick(target)
            target = findImg('exit', count=1, delayTime=1, exit=False)
            if target.x>0:
                pag.leftClick(target)
            direction=0
            return
        drag()
    pag.alert(text='未找到目标，程序已停止运行', title='警告')
    exit()


def begin():
    pag.leftClick(findImg('relic'))
    pag.leftClick(findImg('start', delayTime=1))
    pag.leftClick(findImg('start_play', delayTime=3))
    pag.leftClick(findImg('OK'))
    pag.leftClick(findImg('skip'))


def end():
    pag.leftClick(findImg('exit'))
    target = findImg('end')
    pag.leftClick(target.x-450, target.y+200)
    pag.leftClick(findImg('exit'))


def doBoss(i,count=10):
    time.sleep(1)
    print('第'+str(i)+'天王')
    global direction
    while count>0:
        target = findImg('enemy', count=1, validation=True, exit=False)
        if target.x>=0:
            direction=0
            break
        else:
            drag()
            count=count-1
    if target.x>=0:
        pag.leftClick(target)
    else:
        pag.alert(text='找不到目标，已退出程序', title='警告')
        exit()
    pag.leftClick(findImg('select'))
    battle()
    pag.leftClick(findImg('select'))
    if i==3:
        battle()
        pag.leftClick(findImg('select'))


def drag():
    global direction
    target=findImg('end')
    leftPoint = pag.Point(target.x-1260+400, target.y-466+680)
    rightPoint = pag.Point(target.x-1260+860, target.y-466+900)
    if direction == 0:
        screenshot = pag.screenshot()
        leftPixel = screenshot.getpixel(leftPoint)
        rightPixel = screenshot.getpixel(rightPoint)
        if leftPixel[0]>rightPixel[0]:
            direction=1
        else:
            direction=2
    if direction==1 :
        pag.moveTo(leftPoint)
        pag.mouseDown()
        pag.moveTo(leftPoint.x+500, leftPoint.y+250, duration=0.5)
        pag.mouseUp()
    else:
        pag.moveTo(rightPoint)
        pag.mouseDown()
        pag.moveTo(rightPoint.x-500, rightPoint.y-250, duration=0.5)
        pag.mouseUp()


cnt = 1
while True:
    time.sleep(5)
    print('==='+str(cnt)+'===')
    begin()
    time.sleep(1)
    for i in range(1,5):
        doBoss(i)
        doEvent()
    doBoss(5)
    end()
    cnt = cnt + 1
