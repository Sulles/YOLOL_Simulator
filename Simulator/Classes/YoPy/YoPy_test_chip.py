from time import sleep



def line_1(kwargs):  
    if kwargs['var'] == 0:  
        if kwargs['endres'] != 1:  
            kwargs['endres'] = 2    
    
    else: 	
        kwargs['endres'] = 1  
    kwargs['a'] = kwargs['GLOBAL_b']
    return kwargs, 1
    
