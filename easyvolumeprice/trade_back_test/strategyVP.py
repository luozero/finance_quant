# -*- coding: utf-8 -*-

import numpy as np

import matplotlib.pyplot as plt

def use(**kwargs):
        return strategyVolumePrice(**kwargs)

class strategyVolumePrice:
    def __init__(self,data):
        self.plot_flag = data
        
    def process_daily_limit(self, data, start_time, daily_limit_rate):
        price_today = data.iloc[start_time]
        price_yestoday = data.iloc[start_time-1]
        rate = (price_today - price_yestoday)*100/price_yestoday
        rate_flag = False
        if rate <= daily_limit_rate:
            rate_flag = True
        #rate_flag = rate <= self.daily_limit_rate
        return rate_flag
    
    def processing_edge(self, data, start_time, duration, coeff, pos_neg):
        if start_time<=duration:
            print('start_time=%d is smaller than duration=%d',start_time,duration) 
            exit()
        flag = False

        data_mean = np.mean(data.iloc[start_time-duration-1:start_time-1])
        data_var = np.std(data.iloc[start_time-duration-1:start_time-1])

        if pos_neg == 'POS':
            if data.iloc[start_time]>data_mean+data_var*coeff:
                flag = True
        elif pos_neg == 'NEG':
            if data.iloc[start_time]<data_mean-data_var*coeff:
                flag = True
        return flag
    
    def processing_edge_day_cnt(self, data, start_time, duration, coeff, pos_neg):
        if start_time<=duration:
            print('start_time=%d is smaller than duration=%d',start_time,duration) 
            exit()
        cntDay = 0

        data_mean = np.mean(data.iloc[start_time-duration-1:start_time])
        data_var = np.std(data.iloc[start_time-duration-1:start_time])

        for i in range(start_time-duration-1,start_time):
            if pos_neg == 'POS':
                if data.iloc[i]>data_mean+data_var*coeff:
                    cntDay = cntDay + 1
            elif pos_neg == 'NEG':
                if data.iloc[i]<data_mean-data_var*coeff:
                    cntDay = cntDay + 1
        return cntDay
    
    def processing_bottom_range_day_cnt(self, data, start_time, duration, coeff):
        if start_time<=duration:
            print('start_time=%d is smaller than duration=%d',start_time,duration) 
            exit()
        cntDay = 0

        data_mean = np.mean(data.iloc[start_time-duration-1:start_time-1])
        data_var = np.std(data.iloc[start_time-duration-1:start_time-1])

        for i in range(start_time-duration-1,start_time-1):
            if data.iloc[i]<data_mean+data_var*coeff and data.iloc[i]>data_mean-data_var*coeff:
                cntDay = cntDay + 1
        return cntDay
    
    def plotbottomData(self,data,start_time,duration,coeff):
        pltdata = data.iloc[start_time-duration-1:start_time-1]
        data_mean = np.mean(pltdata)
        data_var = np.std(pltdata)*coeff
        
        plt.plot([0,duration],[data_mean-data_var,data_mean-data_var])
        plt.plot([0,duration],[data_mean+data_var,data_mean+data_var])
        plt.plot([0,duration],[data_mean,data_mean])
        
        data_len = len(pltdata)
        index =np.linspace(0,data_len-1,data_len)
        index.astype(np.uint32)
        pltdata = pltdata.reset_index()
        select_pltdata = pltdata.iloc[:,1]
        plt.plot(select_pltdata,'-o')
        #plt.title(filename)
        #plt.show()
        
        #plt.savefig('./figure'+filename)
    
    def processingVP_bottom_within_range(self, date, start_day, volume, price, duration, volume_coeff, price_coeff, day_in_range):
        volume_day_cnt = self.processing_bottom_range_day_cnt(volume, start_day, duration, volume_coeff)
        price_day_cnt = self.processing_bottom_range_day_cnt(price, start_day, duration, price_coeff)
        if volume_day_cnt >= day_in_range and price_day_cnt >= day_in_range:
            #self.plotbottomData(volume,start_day,duration,date+'volumebottom.png',volume_coeff)
            #self.plotbottomData(price,start_day,duration,date+'pricebottom.png', price_coeff)
            if self.plot_flag :
                plt.figure()
                plt.subplot(211)
                self.plotbottomData(volume,start_day,duration,volume_coeff)
                plt.subplot(212)
                self.plotbottomData(price,start_day,duration, price_coeff)
                plt.savefig(date+'bottom.png')
            return True
            return True
        return False
    
    def processingVP_edge_outof_range(self, date, start_day, volume, price, duration, volume_coeff, price_coeff, day_in_range, pos_neg):
        volume_day_cnt = self.processing_edge_day_cnt(volume, start_day, duration, volume_coeff, pos_neg)
        price_day_cnt = self.processing_edge_day_cnt(price, start_day, duration, price_coeff, pos_neg)
        if volume_day_cnt >= day_in_range and price_day_cnt >= day_in_range:
            #self.plotbottomData(volume,start_day,duration,date+'volumeedge.png', volume_coeff)
            #self.plotbottomData(price,start_day,duration,date+'priceedge.png', price_coeff)
            if self.plot_flag :
                plt.figure()
                plt.subplot(211)
                self.plotbottomData(volume,start_day,duration, volume_coeff)
                plt.subplot(212)
                self.plotbottomData(price,start_day,duration, price_coeff)
                plt.savefig(date+'edge.png')
            return True
        return False
    
    def processingVP_edge_go_up(self, date, start_day, volume, price, duration, volume_coeff, price_coeff, day_in_range, pos_neg):
        volume_flag = self.processing_edge(volume, start_day, duration, volume_coeff, pos_neg)
        price_flag = self.processing_edge(price, start_day, duration, price_coeff, pos_neg)
        if volume_flag == True and price_flag== True:
            if self.plot_flag :
                plt.figure()
                plt.subplot(211)
                self.plotbottomData(volume,start_day,duration, volume_coeff)
                plt.subplot(212)
                self.plotbottomData(price,start_day,duration, price_coeff)
                plt.savefig(date+'edge.png')
            return True
        return False
    
    def processingVP_range_strategy(self, date, start_day, volume, price, volume_coeff, price_coeff,
                                        bottom_days, bottom_days_thres,edge_days,edge_days_thres,edge_coeffvol,edge_coeffpri, pos_neg):
        bottom_flag = self.processingVP_bottom_within_range(date, start_day-edge_days, volume, price, bottom_days, volume_coeff, price_coeff, bottom_days_thres)
        #edge_flag = self.processingVP_edge_outof_range(date, start_day, volume, price, edge_days, edge_coeffvol, edge_coeffpri, edge_days_thres, pos_neg)
        edge_flag = self.processingVP_edge_go_up(date, start_day, volume, price, edge_days, edge_coeffvol, edge_coeffpri, edge_days_thres, pos_neg)
        
        if bottom_flag == True and edge_flag== True:
            if self.plot_flag :
                plt.figure()
                plt.subplot(411)
                self.plotbottomData(volume,start_day-edge_days,bottom_days,volume_coeff)
                plt.subplot(412)
                self.plotbottomData(price,start_day-edge_days,bottom_days, price_coeff)
                plt.subplot(413)
                self.plotbottomData(volume,start_day,edge_days, edge_coeffvol)
                plt.subplot(414)
                self.plotbottomData(price,start_day,edge_days, edge_coeffpri)
                plt.savefig(date)
            return True
        return False

    def processingVP_top_strategy(self, start_day, volume, price, duration, volume_coeff, price_coeff,pos_neg):
        volume_flag = self.processing_edge(volume, start_day, duration, volume_coeff, pos_neg)
        price_flag = self.processing_edge(price, start_day, duration, price_coeff, pos_neg)
        
        if volume_flag == True and price_flag== True:
            return True
        return False












    def processingVP_Edge(self, start_day, volume, price, duration, volume_coeff, price_coeff, pos_neg):
        buy_volume_flag = self.processing_edge(volume, start_day, duration, volume_coeff, pos_neg)
        buy_price_flag = self.processing_edge(price, start_day, duration, price_coeff, pos_neg)
        if buy_volume_flag == True and buy_price_flag == True:
            return True
        return False
    
    def detect_between_value(self,data, mean, var):
        if data<mean+var and data>mean-var:
            return True
        else:
            return False
    
    def processingVP_withDurationBottomFixMeanVar(self, start_day, volume, price, duration, volume_coeff, price_coeff,
                                        bottom_days, bottom_days_thres,edge_days,edge_days_thres,edge_coeffvol,edge_coeffpri):
        bottom_day_cnt = 0
        edge_day_cnt = 0
        smooth_bottom_flag = False
        edge_bottom_flag = False
        vol_mean = np.mean(volume.iloc[start_day-duration-bottom_days-edge_days-1:start_day-bottom_days-edge_days-1])
        #vol_var = np.std(volume.iloc[start_day-duration-bottom_days-edge_days-1:start_day-bottom_days-edge_days-1])
        vol_var = vol_mean*volume_coeff
        price_mean = np.mean(price.iloc[start_day-duration-bottom_days-edge_days-1:start_day-bottom_days-edge_days-1])
        #price_var = np.std(price.iloc[start_day-duration-bottom_days-edge_days-1:start_day-bottom_days-edge_days-1])
        price_var = price_mean*price_coeff
        for i in range(start_day-bottom_days-edge_days,start_day-edge_days):
            buy_volume_flag = self.detect_between_value(volume[i], vol_mean, vol_var)
            buy_price_flag = self.detect_between_value(price[i], price_mean, price_var)
            if buy_volume_flag == True and buy_price_flag == True:
                bottom_day_cnt = bottom_day_cnt + 1
        if bottom_day_cnt >= bottom_days_thres:
            smooth_bottom_flag = True
            
        for i in range(start_day-edge_days,start_day):
            edge_volume_flag = self.processing_edge(volume, i, edge_days, edge_coeffvol, 'POS')
            edge_price_flag = self.processing_edge(price, i, edge_days, edge_coeffpri, 'POS')
            if edge_volume_flag == True and edge_price_flag == True:
                edge_day_cnt = edge_day_cnt + 1
            if edge_day_cnt >= edge_days_thres:
                edge_bottom_flag = True
        if smooth_bottom_flag == True and edge_bottom_flag == True:
            return True
        return False
    
        
    def processing_between_threshold(self, data, start_time, duration, coeff):
        if start_time<=duration:
            print('start_time=%d is smaller than duration=%d',start_time,duration) 
            exit()
        flag = False
        data_mean = np.mean(data.iloc[start_time-duration-1:start_time-1])
        data_var = np.std(data.iloc[start_time-duration-1:start_time-1])
        if data.iloc[start_time]<data_mean+data_var*coeff and data.iloc[start_time]>data_mean-data_var*coeff:
            flag = True
        return flag
    
    def processingVP_withDurationBottom(self, start_day, volume, price, duration, volume_coeff, price_coeff,
                                        bottom_days, bottom_days_thres,edge_days,edge_days_thres,edge_coeffvol,edge_coeffpri):
        bottom_day_cnt = 0
        edge_day_cnt = 0
        smooth_bottom_flag = False
        edge_bottom_flag = False
        for i in range(start_day-bottom_days-edge_days,start_day-edge_days):
            buy_volume_flag = self.processing_between_threshold(volume, i, duration, volume_coeff)
            buy_price_flag = self.processing_between_threshold(price, i, duration, price_coeff)
            if buy_volume_flag == True and buy_price_flag == True:
                bottom_day_cnt = bottom_day_cnt + 1
        if bottom_day_cnt >= bottom_days_thres:
            smooth_bottom_flag = True
            
        for i in range(start_day-edge_days,start_day):
            edge_volume_flag = self.processing_edge(volume, i, duration, edge_coeffvol, 'POS')
            edge_price_flag = self.processing_edge(price, i, duration, edge_coeffpri, 'POS')
            if edge_volume_flag == True and edge_price_flag == True:
                edge_day_cnt = edge_day_cnt + 1
            if edge_day_cnt >= edge_days_thres:
                edge_bottom_flag = True
        if smooth_bottom_flag == True and edge_bottom_flag == True:
            return True
        return False
        
        
        
                