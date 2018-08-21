# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 21:30:46 2017

@author: user
"""

#請拉長output console 不然看可能不到全貌XD
from __future__ import print_function
from gurobipy import*
m=Model("Best_Protein_Week_Menu_Near_NCKU")
meal,type,prote,kcal,cost=multidict({#type:1=主餐 , 2=甜點 
       ('蝦餃'):[1,2.09,54,75],('紅燒花枝羹'):[1,26,480,65],
       ('紅燒土魠魚羹米粉'):[1,25,596,80],('蝦捲'):[1,30,260,50,],
       ('烤雞腿便當'):[1,40,985,85,],('碗粿'):[1,20,6,435,30],('肉粽'):[1,12.8,381,30],
       ('乾炒鱔魚意麵'):[1,40,640,180],('炒羊肉'):[1,47,680,110],('魚皮湯'):[1,21.8,135,60],
       ('黑蛋奶'):[2,8,653,50],('牛奶泡芙'):[2,4.4,344,50],('甜甜圈'):[2,4.9,452,20],
       ('紅豆餅'):[2,6.25,200,15],('奶油車輪餅'):[2,7,253,15],('豬腳飯'):[1,30,815,70],
       ('番茄麵'):[1,20,500,50],('鴛鴦奶茶'):[2,1,462,55],
       ('豬心冬粉'):[1,16,260,45],('壽喜燒拉麵'):[1,24,790,60],('雞排便當'):[1,35,1040,60],('鴨肉飯'):[1,40,900,55],
       ('蘿蔔糕加蛋'):[1,11.6,290,30],('炭烤雞排飯'):[1,46,1060,85],('碎雞鐵板麵'):[1,37.6,850,70],('泰式豬排飯'):[1,29,770,60],
    ('大麥克買一送一'):[1,27.1,1078,79],('義式香草紙包雞餐'):[1,45,832,129],('水餃(20個)'):[1,32,968,70],('鮪魚蛋誁'):[1,14,389,30],
    ('招牌鍋貼(10個)'):[1,50,640,60],('地瓜球'):[2,0.5,467,20],('鵝香飯(大)'):[1,26.5,653.5,35],
    ('牛肉湯麵'):[1,16.8,563.2,50],('皮蛋豆腐'):[1,10.5,199.5,30],('咖哩飯'):[1,28.5,644,50],('金萱茶+椰果(微糖)'):[2,0,145,30],
    ('阿薩姆紅茶'):[2,0,60,30],('四季春茶'):[2,0,80,30],('燒仙草'):[2,2.21,94,45],('叉燒飯'):[1,30,70,800],
('腿蒸蛋飯'):[1,45,65,308],
('肉燥飯'):[1,17,30,413],('麻將乾麵(大)'):[1,6.2,25,175],
('咖哩飯'):[1,13,70,415],('鮪魚蛋餅'):[1,19,25,384],
('玉米蛋餅'):[1,12,20,291],('豆漿'):[2,6,15,60],('蔥餅'):[1,7.2,15,240],('嫩骨飯'):[1,21.4,55,298],
('豬排飯'):[1,30,85,471],('牛肉湯麵'):[1,8.8,70,291.2],
('草莓大福'):[2,3.6,25,310],('日式熔岩蜂蜜蛋糕'):[2,6.25,60,320],('綠豆薏仁湯'):[2,3,35,182],('阿華田'):[2,2,30,60],
('奶茶'):[2,1.2,20,186],('麥香雞'):[1,14,49,380],('勁辣雞腿堡'):[1,27,69,560],('陽春麵(湯)'):[1,14,40,223.5]
       })

num_main=0 #主餐個數
num_dessert=0 #甜點個數
weekkcal=0
weekcost=0

x={}

#設定x[d]為d餐點有選或沒選
for d in meal:
    x[d]=m.addVar(vtype=GRB.BINARY,name="x_%s"%(d))
            
#目標函數
m.setObjective(quicksum(x[d]*prote[d] for d in meal),GRB.MAXIMIZE)

#算出主餐和甜點個數     
for d in meal:
    if type[d] == 1:
        num_main+=x[d]
    if type[d] == 2:
        num_dessert+=x[d]  
#算出本周花費及攝取熱量大卡
weekcost=(quicksum(x[d]*cost[d] for d in meal))                
weekkcal=(quicksum(x[d]*kcal[d] for d in meal))

#一周28餐(包括甜點)   
for d in meal:
    m.addConstr(quicksum(x[d] for d in meal)<=28)
#限制一周主餐21餐 甜點7餐
m.addConstr(num_main==21)                
m.addConstr(num_dessert==7)
#限制一周的花費<=1500
m.addConstr(weekcost<=1500)
#限制一周攝取熱量範圍
m.addConstr(weekkcal>=15000)
m.addConstr(weekkcal<=16000)
#最佳化並印出結果及菜單
m.optimize()
m.write("Best_Protein_Week_Menu_Near_NCKU.lp")

print ("本周最高蛋白質攝取: %g g"%(m.objVal))
print ("本周熱量攝取: %g 大卡"%(weekkcal.getValue()))
print("本周消費金額: %g 元"%(weekcost.getValue()))
print("")
print("本周菜單:")               
print("      一                二                 三                 四                 五                六              日")
count=0
cnt=0
if m.status == GRB.Status.OPTIMAL:
        solution = m.getAttr('x', x)
        print("早 ",end='') 
        for d in meal :
            if solution[d] == 1:
                if (type[d]) == 1:
                    course_type='主餐'
                    count+=1
                    print("%s " %d,end='')
                    if len(d)<27:
                        for k in range(0,(27-len(d))/3):
                            print("  ",end='')
                        if count==7:
                            print("")
                            print("")
                            print("中 ",end='') 
                        if count==14:
                            print("")
                            print("")
                            print("晚 ",end='')
        print("")
        print("")
        print("甜 ",end='')                       
        for d in meal :
            if solution[d] == 1:
                if (type[d]) == 2:
                    course_type='甜點'
                    print("%s " % (d),end='')
                    if len(d)<27:
                        for k in range(0,(27-len(d))/3):
                            print("  ",end='')
                                